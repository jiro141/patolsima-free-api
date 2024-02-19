import datetime
from django.utils import timezone
from django.db import transaction
from patolsima_api.apps import facturacion
from patolsima_api.apps.facturacion.models import Pago, NotaPago
from patolsima_api.apps.facturacion.models.cliente import Cliente
from patolsima_api.apps.facturacion.models.orden import Orden
from patolsima_api.apps.facturacion.models.recibo_y_factura import NotaCreditoOffset, NotaDebitoOffset, NotasCredito, NotasDebito, Factura
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


def generar_notacredito(orden:Orden,monto) -> NotasCredito:

    factura = Factura.objects.get(orden=orden)
    monto = monto
    n_factura = factura.n_factura
    s3_file = UploadedFile.objects.get(file_name=factura.s3_file.file_name)
    
    with transaction.atomic() as current_transaction:
        latest_notacredito = NotasCredito.objects.order_by().last()

        if latest_notacredito and latest_notacredito.n_notacredito is not None:
            latest_frecord = latest_notacredito.n_notacredito
        else:
            latest_frecord = 1
        latest_offset = NotaCreditoOffset.objects.order_by('notacredito_offset').last()
        if latest_offset and latest_offset.notacredito_offset is not None:
            latest_ofrecord = latest_offset.notacredito_offset
        else:
            latest_ofrecord = 1

        if latest_frecord > latest_ofrecord:
            n_notacredito = latest_frecord + 1
        else:
            n_notacredito = latest_ofrecord + 1

        f_transaccion = Transaccion.objects.filter(tipo="NOTA CREDITO").order_by("n_control").last()


        if f_transaccion!=None:
             if f_transaccion.n_control >= n_notacredito:
                n_notacredito=f_transaccion.n_documento + 1

        nota_credito, created = NotasCredito.objects.get_or_create(n_notacredito=n_notacredito,orden=orden,n_factura=n_factura, monto=monto, defaults={})
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
    Factura.objects.filter(orden=orden).update(orden=None)
    Factura.objects.filter(orden=orden).update(s3_file=None)


    return nota_credito


def generar_notadebito(orden:Orden,monto,**kwargs) -> NotasDebito:  

    factura=Factura.objects.get(orden=orden)
    
    latest_notadebito = NotasDebito.objects.order_by('id').last()

    if latest_notadebito and latest_notadebito.n_notadebito is not None:
        latest_frecord = latest_notadebito.n_notadebito
    else:
        latest_frecord = 1
    latest_offset = NotaDebitoOffset.objects.order_by('notadebito_offset').last()
    if latest_offset and latest_offset.notadebito_offset is not None:
        latest_ofrecord = latest_offset.notadebito_offset
    else:
        latest_ofrecord = 1

    if latest_frecord > latest_ofrecord:
        n_notadebito = latest_frecord + 1
    else:
        n_notadebito = latest_ofrecord + 1

    f_transaccion = Transaccion.objects.filter(tipo="NOTA DEBITO").order_by("n_control").last()


    if f_transaccion!=None:
        if f_transaccion.n_control >= n_notadebito:
            n_notadebito=f_transaccion.n_documento + 1


    with transaction.atomic() as current_transaction:
        nota_debito, created = NotasDebito.objects.get_or_create(orden=orden, monto=monto,n_factura = factura.n_factura,n_notadebito=n_notadebito, defaults={})
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

