from typing import Dict, Any
import time
from django.db import transaction
from patolsima_api.apps.facturacion.models import Pago, NotaPago
from patolsima_api.apps.facturacion.utils.jinja import nota_de_pago_body_template
from patolsima_api.apps.s3_management.utils.upload import upload_from_local_filesystem
from patolsima_api.utils.render_pdf import render_pdf


def generar_nota_de_pago(pago: Pago) -> NotaPago:
    if hasattr(pago, "nota_de_pago") and pago.nota_de_pago.s3_file:
        return pago.nota_de_pago

    with transaction.atomic() as current_transaction:
        nota_pago, created = NotaPago.objects.get_or_create(pago=pago, defaults={})
        filename = f"nota_de_pago_{nota_pago.id}_{int(time.time())}"
        nota_pago.s3_file = upload_from_local_filesystem(
            render_pdf(
                context={"nota_de_pago": nota_pago, "pago": nota_pago.pago},
                templates={
                    "body": {
                        "template_obj": nota_de_pago_body_template,
                        "pre_render": True,
                    }
                },
                destination=filename,
            )
        )

    return nota_pago
