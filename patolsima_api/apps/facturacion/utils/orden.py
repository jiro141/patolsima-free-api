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

    estudios_id = [item.estudio_id for item in orden.items_orden.all()]
    estudios = Estudio.objects.select_for_update().filter(id__in=estudios_id)
    for estudio in estudios:
        estudio.confirmado = True
        estudio.save()

    orden.confirmada = True
    orden.save()
    return True


@transaction.atomic
def generar_recibo_o_factura(orden: Orden, tipo_documento: str, **kwargs) -> Recibo:
    if not orden.pagada:
        raise ValidationError("La orden no ha sido pagada todavia.")

    if hasattr(orden, tipo_documento):
        return getattr(orden, tipo_documento)

    intancia_de_documento = (
        Recibo if tipo_documento == "recibo" else Factura
    ).objects.create(orden=orden, **kwargs)
    intancia_de_documento.s3_file = upload_from_local_filesystem(
        render_recibo_factura(intancia_de_documento)
    )
    intancia_de_documento.save()


def render_recibo_factura(registro: Union[Factura, Recibo]) -> str:
    pass