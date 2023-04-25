from django.db import models
from django.db.models.signals import pre_save
from decimal import Decimal
from simple_history.models import HistoricalRecords
from patolsima_api.utils.models import AuditableMixin, TelefonoMixin, DireccionMixin
from patolsima_api.apps.core.models import Estudio
from patolsima_api.apps.s3_management.models import S3File
from .cliente import Cliente


class Orden(AuditableMixin):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    confirmada = models.BooleanField(default=False)
    pagada = models.BooleanField(default=False)
    history = HistoricalRecords()


class ItemOrden(AuditableMixin):
    estudio = models.OneToOneField(
        Estudio, on_delete=models.CASCADE, related_name="items_orden"
    )
    orden = models.ForeignKey(
        Orden, on_delete=models.CASCADE, related_name="items_orden"
    )
    monto_usd = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    history = HistoricalRecords()

    @classmethod
    def pre_save(cls, sender, instance, *args, **kwargs):
        if not instance.orden:
            raise Exception("ItemOrden must contain relationship with Orden")

        if instance.orden.pagada:
            raise Exception(
                "No se puede cambiar el ItemOrden de una Orden luego de estar pagada."
            )


pre_save.connect(ItemOrden.pre_save, ItemOrden)
