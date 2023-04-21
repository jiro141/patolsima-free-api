from patolsima_api.apps.facturacion.models import Pago, NotaPago
from typing import Dict, Any
from django.db import transaction


def generar_nota_de_pago(pago: Pago) -> NotaPago:
    if hasattr(pago, "nota_de_pago"):
        return pago.nota_de_pago

    with transaction.atomic() as current_transaction:
        nota_pago = NotaPago.objects.create(pago=pago)
        # Do current S3 File generation here

    return nota_pago
