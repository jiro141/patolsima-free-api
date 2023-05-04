import time
from django.db import transaction
from rest_framework.exceptions import ValidationError
from patolsima_api.apps.core.models import Informe, Estudio
from patolsima_api.apps.core.utils.jinja_templates import informe_body_template
from patolsima_api.utils.render_pdf import render_pdf
from patolsima_api.apps.s3_management.utils.upload import upload_from_local_filesystem


INFORME_TEMPLATES = {
    "body": {
        "template_obj": informe_body_template,
        "pre_render": True,
    }
}


def _check_errors_before_generar_informe(informe: Informe):
    estudio = informe
    if not estudio.confirmado:
        raise ValidationError("El Estudio necesita estar confirmado.")

    if estudio.items_orden.orden.pagada:
        raise ValidationError("La Orden a la que pertenece el Estudio no esta pagada.")

    if informe.completado:
        raise ValidationError("El Informe no se ha completado.")

    if informe.aprobado:
        raise ValidationError("El Informe debe estar aprobado por el patologo.")


def generar_informe(informe: Informe) -> Informe:
    _check_errors_before_generar_informe(informe)
    filename = f"informe_{informe.id}_{int(time.time())}"

    file_path = render_pdf(
        context={}, templates=INFORME_TEMPLATES, destination=filename
    )

    return informe
