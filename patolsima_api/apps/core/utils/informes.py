import os
import time
# from PIL import Image
import io
from datetime import datetime
from django.http import FileResponse
from django.db import transaction
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.exceptions import ValidationError
from simple_history.utils import update_change_reason
from typing import Dict, Any, Generator
from patolsima_api.apps.core.models import Informe, Estudio
from patolsima_api.apps.core.serializers import InformeSerializer
from patolsima_api.apps.core.utils.patologo import check_user_is_patologo
from patolsima_api.apps.core.utils.jinja_templates import (
    informe_body_template,
    informe_footer_template,
    informe_header_template,
)
from patolsima_api.utils.render_pdf import render_pdf
from patolsima_api.utils.file import FileResponseWithTemporalFileDeletion
from patolsima_api.apps.uploaded_file_management.utils.upload import (
    upload_from_local_filesystem,
    upload_from_request,
)
from patolsima_api.apps.uploaded_file_management.serializers import (
    UploadedFileSerializer,
)
from patolsima_api.utils.users import check_user_is_in_any_group


INFORME_REGULAR_TEMPLATES = {
    "body": {
        "template_obj": informe_body_template,
        "pre_render": True,
    },
    "footer": {
        "template_obj": informe_footer_template,
        "pre_render": True,
    },
    "header": {"template_obj": informe_header_template, "pre_render": True},
}

INFORME_INMUNOSTOQUIMICA_TEMPLATES = {
    "body": {
        "template_obj": informe_body_template,
        "pre_render": True,
    }
}


def _check_errors_before_generar_informe(informe: Informe):
    estudio = informe.estudio
    if not estudio.confirmado:
        raise ValidationError("El Estudio necesita estar confirmado.")

    if not estudio.items_orden.orden.pagada:
        raise ValidationError("La Orden a la que pertenece el Estudio no esta pagada.")

    if not informe.completado:
        raise ValidationError("El Informe no se ha completado.")

    if not informe.aprobado:
        raise ValidationError("El Informe debe estar aprobado por el patologo.")


def render_informe(informe: Informe, preview_only: bool = False) -> str:
    """
    Renders the Informe into a PDF
    :param informe: Informe instance to be rendered
    :param preview_only: helps to identify if the validation for definitive generation of the PDF shall be evaluated.
    :return: File path to the PDF file into the filesystem.
    """

    if not preview_only:
        _check_errors_before_generar_informe(informe)

    estudio = informe.estudio
    filename = f"informe_{estudio.id}_{int(time.time())}"
    tipo_estudio_titulo = estudio.tipo.replace("_", " ").title()
    if estudio.tipo == Estudio.TipoEstudio.INMUNOSTOQUIMICA:
        # El nombre originalmente era este pero hubo un error en la documentación y ahora todo el proyecto dice inmunostoquimica en vez de inmunohistoquimica
        tipo_estudio_titulo = "Inmunohistoquímica"

    return render_pdf(
        context={
            "current_work_path_python": os.getcwd(),
            "tipo_estudio_titulo": tipo_estudio_titulo,
            "estudio": estudio,
            "informe": informe,
            "paciente": estudio.paciente,
            "medico": estudio.medico_tratante,
            "fecha_ingreso": estudio.created_at.date().isoformat(),
            "today": datetime.now().date().isoformat(),
            "resultados_inmunostoquimica": informe.resultados_inmunostoquimica.all(),
            "patologo": estudio.patologo,
            "tipo_de_muestra": " / ".join(
                [
                    muestra.tipo_de_muestra
                    for muestra in estudio.muestras.all()
                    if muestra.tipo_de_muestra
                ]
            ),
        },
        templates=INFORME_REGULAR_TEMPLATES,
        destination=filename,
        extra_args={
            "wkhtmltopdf_options": {
                "--page-size": "A4",
                # "--orientation": "Landscape",
                "--header-right": "[page]/[topage]",
                "--header-spacing": "5",
                "--footer-spacing": "5",
                "--margin-left": "50px",
                "--margin-right": "50px",
                "--margin-top": "200px",
                "--margin-bottom": "130px",
            }
        },
    )


def generar_informe_preview(
    informe: Informe,
) -> FileResponse:
    """
    Generates a PDF file for an Informe instance.
    :param informe: the Informe instance to translate to PDF
    :return: FileResponse containing the PDF file as a binary attachment
    """

    filepath = render_informe(informe, preview_only=True)
    return FileResponseWithTemporalFileDeletion(
        open(filepath, "rb"), as_attachment=True, temporal_file_path=filepath
    )


@transaction.atomic
def generar_y_guardar_informe(informe: Informe) -> Dict[str, Any]:
    """
    Generates the definitive PDF for Informe instance (or returns a previous generated one)
    :param informe: instance for what the PDF is going to ve generated.
    :return: representation of the uploaded PDF file (S3).
    """
    if informe.informes_generado:
        return UploadedFileSerializer(informe.informes_generado).data

    filepath = render_informe(informe)
    informe.informes_generado = upload_from_local_filesystem(
        file_path=filepath, path_prefix="informes", delete_original_after_upload=True
    )
    informe.save()
    update_change_reason(informe, "PDF generado")
    return UploadedFileSerializer(informe.informes_generado).data


def completar_informe(informe: Informe, user: User) -> bool:
    if informe.completado:
        return True

    if not check_user_is_in_any_group(user, ["patologo", "administracion"]):
        raise ValidationError("User can not perform this action")
    informe.completado = True
    informe.save()
    update_change_reason(informe, "Informe marcado como completado")
    return True


def aprobar_informe(informe: Informe, user: User) -> bool:
    if informe.aprobado:
        return True

    patologo = check_user_is_patologo(user)
    # if patologo.id != informe.estudio.patologo.id:
    #     raise ValidationError(
    #         "The pathologist who is approving the report is not the same pathologist assigned to the study"
    #     )
    informe.aprobado = True
    informe.save()
    update_change_reason(informe, "Informe marcado como aprobado para impresion.")
    return True


def agregar_imagen_al_informe(
    informe: Informe, file: InMemoryUploadedFile
) -> Dict[str, Any]:
    """
    Uploads an image to S3 and returns its URL to add the image to any field that uses CKEditor rich text editor.
    :param informe: Informe that owns the image that's being uploaded
    :param file: Memory representation of the file that is being uploaded.
    :return: The URL to access the image file in S3.
    """

    # max_size = (300, 300)
    # image = Image.open(file)
    # image.thumbnail(max_size)
    # output = io.BytesIO()
    # image.save(output, format='JPEG')
    # resized_image_data = output.getvalue()


    # uploaded_file = upload_from_request(
    #     resized_image_data, path_prefix=f"informes/{informe.estudio.id}/images"
    # )
    uploaded_file = upload_from_request(
        file, path_prefix=f"informes/{informe.estudio.id}/images"
    )
    informe.images_for_rich_text.add(uploaded_file)
    informe.save()
    update_change_reason(informe, "Nueva imagen añadida al informe")
    return UploadedFileSerializer(uploaded_file).data
