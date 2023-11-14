import datetime
from django.db import transaction
from patolsima_api.apps import facturacion
from patolsima_api.apps.facturacion.models import Pago, NotaPago
from patolsima_api.apps.facturacion.models.recibo_y_factura import NotaCredito, NotaDebito, Factura
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


def generar_notacredito(factura:Factura) -> NotaCredito:
    
    with transaction.atomic() as current_transaction:
        nota_credito, created = NotaCredito.objects.get_or_create(orden=Factura.orden,factura=factura, monto=factura.monto, defaults={})
        nota_credito.s3_file = upload_from_local_filesystem(
            render_nota_de_pago(nota_credito),
            path_prefix=f"ordenes/{factura.orden.id}/notas_de_credito",
            delete_original_after_upload=True,
        )
        nota_credito.fecha_generacion = datetime.now()
        nota_credito.save()
        transaccion, created = Transaccion.objects.create(
            rifci = nota_credito.orden.cliente.ci_rif,
            cliente=nota_credito.orden.cliente.razon_social,
            tipo = "NOTA CREDITO",
            monto = nota_credito.monto
            )
        transaccion.save()

    return nota_credito


def generar_notadebito(n_factura,monto) -> NotaDebito:  

    factura=Factura.objects.get(n_factura=n_factura)
    
    with transaction.atomic() as current_transaction:
        nota_debito, created = NotaDebito.objects.get_or_create(factura=factura, monto=monto, defaults={})
        nota_debito.s3_file = upload_from_local_filesystem(
            render_nota_de_pago(nota_debito),
            path_prefix=f"ordenes/{factura.orden.id}/notas_de_debito",
            delete_original_after_upload=True,
        )
        nota_debito.fecha_generacion = datetime.now()
        nota_debito.save()
        transaccion, created = Transaccion.objects.create(
            rifci = nota_debito.orden.cliente.ci_rif,
            cliente=nota_debito.orden.cliente.razon_social,
            tipo = "NOTA DEBITO",
            monto = nota_debito.monto
            )
        transaccion.save()
    return nota_debito

