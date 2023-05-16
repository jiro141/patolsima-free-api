from django.db import transaction
from patolsima_api.apps.facturacion.models import Pago, NotaPago
from patolsima_api.apps.uploaded_file_management.utils.upload import (
    upload_from_local_filesystem,
)
from patolsima_api.apps.facturacion.utils.render import render_nota_de_pago


def generar_nota_de_pago(pago: Pago) -> NotaPago:
    if hasattr(pago, "nota_de_pago") and pago.nota_de_pago.s3_file:
        return pago.nota_de_pago

    with transaction.atomic() as current_transaction:
        nota_pago, created = NotaPago.objects.get_or_create(pago=pago, defaults={})
        nota_pago.s3_file = upload_from_local_filesystem(
            render_nota_de_pago(nota_pago),
            path_prefix=f"ordenes/{pago.orden.id}/notas_de_pago",
        )
        nota_pago.save()

    return nota_pago
