from django.db import transaction
from rest_framework.serializers import ValidationError
from patolsima_api.apps.facturacion.models import Orden
from patolsima_api.apps.core.models import Estudio


@transaction.atomic
def confirm_orden(orden: Orden):
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
