from datetime import datetime
from django.db import transaction
from patolsima_api.apps.facturacion.models.recibo_y_factura import FacturaOffset
from patolsima_api.apps.facturacion.models.transaccion import Transaccion
from rest_framework.serializers import ValidationError
from patolsima_api.apps.facturacion.models import Orden, Factura, Recibo
from patolsima_api.apps.core.models import Estudio
from patolsima_api.apps.uploaded_file_management.utils import (
    upload_from_local_filesystem,
)
from .render import render_recibo_factura


@transaction.atomic
def confirm_orden(orden: Orden):
    if orden.confirmada:
        raise ValidationError("Orden is already confirmed")

    if (
        orden.items_orden.filter(estudio__confirmado=False).count()
        < orden.items_orden.count()
    ):
        raise ValidationError(
            "There is at least 1 Estudio confirmed for this Orden. Please check"
        )

    estudios_id = [item.estudio_id for item in orden.items_orden.all()]
    Estudio.objects.filter(id__in=estudios_id).update(confirmado=True)
    orden.confirmada = True
    orden.save()
    return True


@transaction.atomic
def archivar_orden(orden: Orden):
    """
    Modifies Orden.archivada to True. This operation is applicable to non payed orders or non desired orders.
    :param orden: Order instance to be archived
    :return: None
    """
    orden.archive()
    return True


@transaction.atomic
def generar_recibo_o_factura(orden: Orden, tipo_documento: str, **kwargs) -> Recibo:
    if not orden.pagada:
        raise ValidationError("La orden no ha sido pagada todavia.")

    if hasattr(orden, tipo_documento) and getattr(orden, tipo_documento).s3_file:
        return getattr(orden, tipo_documento)

    if tipo_documento == "recibo":
        instancia_de_documento, created = (Recibo).objects.get_or_create(orden=orden, defaults=kwargs)

    if tipo_documento !="recibo":
        latest_factura = Factura.objects.order_by('id').last()

        if latest_factura and latest_factura.n_factura is not None:
            latest_frecord = latest_factura.n_factura
        else:
            latest_frecord = 1
        latest_offset = FacturaOffset.objects.order_by('factura_offset').last()
        if latest_offset and latest_offset.factura_offset is not None:
            latest_ofrecord = latest_offset.factura_offset
        else:
            latest_ofrecord = 1

        if latest_frecord > latest_ofrecord:
            n_factura = latest_frecord + 1
        else:
            n_factura = latest_ofrecord + 1

        f_transaccion = Transaccion.objects.filter(tipo="FACTURA").order_by("n_control").last()


        if f_transaccion!=None:
             if f_transaccion.n_control >= n_factura:
                n_factura=f_transaccion.n_control + 1
        instancia_de_documento, created = (Factura).objects.get_or_create(orden=orden,n_factura=n_factura, defaults=kwargs)
        instancia_de_documento.monto = orden.importe_orden_bs
        n_controlobject = Transaccion.objects.last()
        n_control = n_controlobject.n_control + 1
  
        transaccion, created = Transaccion.objects.get_or_create(
            rifci = instancia_de_documento.orden.cliente.ci_rif,
            cliente=instancia_de_documento.orden.cliente.razon_social,
            tipo = "FACTURA",
            monto = instancia_de_documento.monto,
            n_control = n_control,
            n_documento = instancia_de_documento.n_factura
            )
        
        instancia_de_documento.fecha_generacion = datetime.now()


        instancia_de_documento.s3_file = upload_from_local_filesystem(
            render_recibo_factura(instancia_de_documento, tipo_documento),
            path_prefix=f"ordenes/{orden.id}",
            delete_original_after_upload=True,
        )
        instancia_de_documento.save()
        return instancia_de_documento
        
        

    instancia_de_documento.fecha_generacion = datetime.now()

    instancia_de_documento.s3_file = upload_from_local_filesystem(
        render_recibo_factura(instancia_de_documento, tipo_documento),
        path_prefix=f"ordenes/{orden.id}",
        delete_original_after_upload=True,
    )
    instancia_de_documento.save()
    return instancia_de_documento
