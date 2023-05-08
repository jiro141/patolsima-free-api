import time
from django.http import FileResponse
from rest_framework.exceptions import ValidationError
from typing import Dict, Any, Generator
from patolsima_api.apps.core.models import Informe, Estudio
from patolsima_api.apps.core.serializers import InformeSerializer
from patolsima_api.apps.core.utils.jinja_templates import informe_body_template
from patolsima_api.utils.render_pdf import render_pdf
from patolsima_api.utils.file import FileResponseWithTemporalFileDeletion
from patolsima_api.apps.uploaded_file_management.utils.upload import (
    upload_from_local_filesystem,
)


INFORME_REGULAR_TEMPLATES = {
    "body": {
        "template_obj": informe_body_template,
        "pre_render": True,
    }
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

    templates = (
        INFORME_INMUNOSTOQUIMICA_TEMPLATES
        if informe.estudio.tipo == Estudio.TipoEstudio.INMUNOSTOQUIMICA
        else INFORME_REGULAR_TEMPLATES
    )
    return render_pdf(context={}, templates=templates, destination=filename)


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
    # TO COMPLETE


def generar_y_guardar_informe(informe: Informe) -> Dict[str, Any]:
    filepath = render_informe(informe)
    upload_from_local_filesystem(file_path=filepath, path_prefix="informes")
    return InformeSerializer(
        informe
    ).data  # Maybe I can change this to only the S3 link to the file uploaded
