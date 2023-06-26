import os
import time
from datetime import datetime
from django.http import FileResponse
from django.db import transaction
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
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
)
from patolsima_api.apps.uploaded_file_management.serializers import (
    UploadedFileSerializer,
)
from patolsima_api.utils.users import check_user_is_in_groups


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

    if estudio.items_orden.orden.pagada:
        raise ValidationError("La Orden a la que pertenece el Estudio no esta pagada.")

    if informe.completado:
        raise ValidationError("El Informe no se ha completado.")

    if informe.aprobado:
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

    filename = f"informe_{informe.estudio.id}_{int(time.time())}"

    return render_pdf(
        context={
            "current_work_path_python": os.getcwd(),
            "tipo_estudio_titulo": "Inmunostoquimica",
            "estudio": informe.estudio,
            "informe": informe,
            "paciente": informe.estudio.paciente,
            "medico": informe.estudio.medico_tratante,
            "fecha_ingreso": informe.estudio.created_at.date().isoformat(),
            "today": datetime.now().date().isoformat(),
            "resultados_inmunostoquimica": informe.resultados_inmunostoquimica.all(),
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
    filepath = render_informe(informe)
    informe.informes_generado = upload_from_local_filesystem(
        file_path=filepath, path_prefix="informes", delete_original_after_upload=True
    )
    informe.save()
    return UploadedFileSerializer(informe.informes_generado).data


def completar_informe(informe: Informe, user: User) -> bool:
    if not check_user_is_in_groups(user, ["patologo", "administracion"]):
        raise ValidationError("User can not perform this action")
    informe.completado = True
    return True


def aprobar_informe(informe: Informe, user: User) -> bool:
    patologo = check_user_is_patologo(user)
    if patologo.id != informe.estudio.patologo.id:
        raise ValidationError(
            "The pathologist who is approving the report is not the same pathologist assigned to the study"
        )
    informe.aprobado = True
    return True
