from django.db import transaction
from rest_framework.serializers import ValidationError
from typing import Union
from patolsima_api.apps.facturacion.models import Orden, Factura, Recibo
from patolsima_api.apps.core.models import Estudio
from patolsima_api.apps.s3_management.utils import upload_from_local_filesystem


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

    estudios_id = [item.estudio_id for item in orden.items_orden]
    estudios = Estudio.objects.select_for_update().filter(id__in=estudios_id)
    for estudio in estudios:
        estudio.confirmado = True
        estudio.save()

    orden.confirmada = True
    orden.save()


@transaction.atomic
def generar_recibo(orden: Orden) -> Recibo:
    if hasattr(orden, "recibo"):
        return orden.recibo
    recibo = Recibo.objects.create(orden=orden)
    recibo.s3_file = upload_from_local_filesystem(render_recibo_factura(recibo))
    recibo.save()


@transaction.atomic
def generar_factura(orden: Orden, n_factura: int = None) -> Factura:
    if hasattr(orden, "factura"):
        return orden.factura
    factura = Factura.objects.create(orden=orden, n_factura=n_factura)
    factura.s3_file = upload_from_local_filesystem(render_recibo_factura(factura))
    factura.save()


def render_recibo_factura(registro: Union[Factura, Recibo]) -> str:
    pass
