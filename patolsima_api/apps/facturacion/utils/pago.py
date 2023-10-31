from django.db import transaction
from patolsima_api.apps import facturacion
from patolsima_api.apps.facturacion.models import Pago, NotaPago
from patolsima_api.apps.facturacion.models.recibo_y_factura import NotaCredito, NotaDebito
from patolsima_api.apps.uploaded_file_management.utils.upload import (
    upload_from_local_filesystem,
)
from patolsima_api.apps.facturacion.utils.render import render_nota_de_pago
from patolsima_api.apps.facturacion.models.transaccion import Transaccion


def generar_nota_de_pago(pago: Pago) -> NotaPago:
    if hasattr(pago, "nota_de_pago") and pago.nota_de_pago.s3_file:
        return pago.nota_de_pago

    with transaction.atomic() as current_transaction:
        nota_pago, created = NotaPago.objects.get_or_create(pago=pago, defaults={})
        nota_pago.s3_file = upload_from_local_filesystem(
            render_nota_de_pago(nota_pago),
            path_prefix=f"ordenes/{pago.orden.id}/notas_de_pago",
            delete_original_after_upload=True,
        )
        nota_pago.save()

    return nota_pago


def generar_notacredito(pago:Pago, factura:facturacion) -> NotaCredito:
    if hasattr(pago, "nota_de_credito") and pago.nota_de_credito.s3_file:
        return pago.nota_de_credito
    
    with transaction.atomic() as current_transaction:
        nota_credito, created = NotaCredito.objects.get_or_create(pago=pago,factura=factura, monto=pago.total_usd, defaults={})
        nota_credito.s3_file = upload_from_local_filesystem(
            render_nota_de_pago(nota_credito),
            path_prefix=f"ordenes/{pago.orden.id}/notas_de_credito",
            delete_original_after_upload=True,
        )
        nota_credito.save()
        transaccion, created = Transaccion.objects.create(
            rifci = nota_credito.orden.cliente.ci_rif,
            cliente=nota_credito.orden.cliente.razon_social,
            tipo = "NOTA CREDITO",
            monto = nota_credito.monto
            )
        transaccion.save()

    return nota_credito


def generar_notadebito(pago:Pago, factura:facturacion,monto) -> NotaDebito:
    if hasattr(pago, "nota_de_debito") and pago.nota_de_debito.s3_file:
        return pago.nota_de_debito
    
    #revisar la factura
    
    
    with transaction.atomic() as current_transaction:
        nota_debito, created = NotaDebito.objects.get_or_create(pago=pago,factura=factura, monto=monto, defaults={})
        nota_debito.s3_file = upload_from_local_filesystem(
            render_nota_de_pago(nota_debito),
            path_prefix=f"ordenes/{pago.orden.id}/notas_de_debito",
            delete_original_after_upload=True,
        )
        nota_debito.save()
        transaccion, created = Transaccion.objects.create(
            rifci = nota_debito.orden.cliente.ci_rif,
            cliente=nota_debito.orden.cliente.razon_social,
            tipo = "NOTA DEBITO",
            monto = nota_debito.monto
            )
        transaccion.save()
    return nota_debito

