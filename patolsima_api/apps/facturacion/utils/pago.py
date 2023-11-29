import datetime
from django.utils import timezone
from django.db import transaction
from patolsima_api.apps import facturacion
from patolsima_api.apps.facturacion.models import Pago, NotaPago
from patolsima_api.apps.facturacion.models.cliente import Cliente
from patolsima_api.apps.facturacion.models.orden import Orden
from patolsima_api.apps.facturacion.models.recibo_y_factura import NotasCredito, NotasDebito, Factura
from patolsima_api.apps.uploaded_file_management.models import UploadedFile
from patolsima_api.apps.uploaded_file_management.utils.upload import (
    upload_from_local_filesystem,
)
from patolsima_api.apps.facturacion.utils.render import render_nota_de_pago, render_notadebito, render_notacredito
from patolsima_api.apps.facturacion.models.transaccion import Transaccion
from simple_history.models import HistoricalRecords



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


def generar_notacredito(orden:Orden) -> NotasCredito:

    factura = Factura.objects.get(orden=orden)
    monto = factura.monto
    n_factura = factura.n_factura
    s3_file = UploadedFile.objects.get(file_name=factura.s3_file.file_name)
    
    with transaction.atomic() as current_transaction:
        nota_credito, created = NotasCredito.objects.get_or_create(orden=orden,n_factura=n_factura, monto=monto, defaults={})
        nota_credito.fecha_generacion = timezone.now()
        nota_credito.s3_file = upload_from_local_filesystem(
            render_notacredito(nota_credito,"Nota Credito"),
            path_prefix=f"ordenes/{orden.id}/notas_de_credito",
            delete_original_after_upload=True,
        )
        nota_credito.save()
        n_controlobject = Transaccion.objects.last()
        n_control = n_controlobject.n_control + 1
        transaccion, created = Transaccion.objects.get_or_create(
            rifci = nota_credito.orden.cliente.ci_rif,
            cliente=nota_credito.orden.cliente.razon_social,
            tipo = "NOTA CREDITO",
            monto = nota_credito.monto*-1,
            n_control = n_control,
            n_documento = nota_credito.n_notacredito
            )
    Factura.objects.filter(orden=orden).delete(force=True)
    factura.delete(force=True)
    history_manager = HistoricalRecords.objects.filter(history_type=type(orden), object_id=orden.pk)
    history_manager.delete()

    return nota_credito


def generar_notadebito(orden:Orden,monto,**kwargs) -> NotasDebito:  

    factura=Factura.objects.get(orden=orden)
    
    lastest_notadebito = NotasDebito.objects.order_by('id').last()
    if lastest_notadebito and lastest_notadebito.n_notadebito is not None:
        lastest_nrecord = lastest_notadebito.n_notadebito + 1
    else:
        lastest_nrecord = 1


    with transaction.atomic() as current_transaction:
        nota_debito, created = NotasDebito.objects.get_or_create(orden=orden, monto=monto,n_factura = factura.n_factura,n_notadebito=lastest_nrecord, defaults={})
        nota_debito.fecha_generacion = timezone.now()
        nota_debito.s3_file = upload_from_local_filesystem(
            render_notadebito(nota_debito,"Nota Debito"),
            path_prefix=f"ordenes/{orden.id}/notas_de_debito",
            delete_original_after_upload=True,
        )
        nota_debito.save()
        n_controlobject = Transaccion.objects.last()
        n_control = n_controlobject.n_control + 1
        transaccion, created = Transaccion.objects.get_or_create(
            rifci = nota_debito.orden.cliente.ci_rif,
            cliente=nota_debito.orden.cliente.razon_social,
            tipo = "NOTA DEBITO",
            monto = nota_debito.monto,
            n_control = n_control,
            n_documento = nota_debito.n_notadebito
            )

    return nota_debito

