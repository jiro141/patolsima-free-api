from datetime import datetime
from django.db import transaction
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

    instancia_de_documento, created = (
        Recibo if tipo_documento == "recibo" else Factura
    ).objects.get_or_create(orden=orden, defaults=kwargs)

    instancia_de_documento.fecha_generacion = datetime.now()

    instancia_de_documento.s3_file = upload_from_local_filesystem(
        render_recibo_factura(instancia_de_documento, tipo_documento),
        path_prefix=f"ordenes/{orden.id}",
        delete_original_after_upload=True,
    )
    instancia_de_documento.save()
    return instancia_de_documento
