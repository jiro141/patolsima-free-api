from django.db import models
from decimal import Decimal
from simple_history.models import HistoricalRecords
from patolsima_api.apps.s3_management.models import S3File
from patolsima_api.utils.models import AuditableMixin
from .orden import Orden


class Pago(AuditableMixin):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name="pagos")

    # Esta configuracion permite maximo montos de 99M USD
    monto_usd = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    total_usd = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    pendiente_por_pagar_usd = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )

    # Esta configuracion permite maximo montos de 999B  Bs
    monto_bs = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00")
    )
    total_bs = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00")
    )
    pendiente_por_pagar_bs = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00")
    )

    detalle = models.TextField(max_length=2048, null=True, blank=True)
    history = HistoricalRecords()


class NotaPago(AuditableMixin):
    pago = models.OneToOneField(
        Pago, on_delete=models.CASCADE, related_name="nota_de_pago"
    )
    s3_file = models.OneToOneField(
        S3File, on_delete=models.CASCADE, null=True, blank=True
    )
    history = HistoricalRecords()
