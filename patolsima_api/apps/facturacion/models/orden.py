from django.db import models
from decimal import Decimal
from simple_history.models import HistoricalRecords
from patolsima_api.utils.models import AuditableMixin, TelefonoMixin, DireccionMixin
from patolsima_api.apps.core.models import Estudio
from patolsima_api.apps.s3_management.models import S3File
from .cliente import Cliente


class Orden(AuditableMixin):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    confirmada = models.BooleanField(default=False)
    history = HistoricalRecords()


class ItemOrden(AuditableMixin):
    estudio = models.OneToOneField(
        Estudio, on_delete=models.CASCADE, related_name="item_orden"
    )
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    monto_usd = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    history = HistoricalRecords()
