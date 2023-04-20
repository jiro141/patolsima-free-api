from django.db import models
from decimal import Decimal
from simple_history.models import HistoricalRecords
from patolsima_api.utils.models import AuditableMixin, TelefonoMixin, DireccionMixin
from patolsima_api.apps.core.models import Estudio
from patolsima_api.apps.s3_management.models import S3File


class Cliente(AuditableMixin, TelefonoMixin, DireccionMixin):
    razon_social = models.CharField(max_length=255)
    ci_rif = models.CharField(max_length=32)

    history = HistoricalRecords()


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


class Pago(AuditableMixin):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)

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
    pago = models.OneToOneField(Pago, on_delete=models.CASCADE)
    s3_file = models.OneToOneField(S3File, on_delete=models.CASCADE)
    history = HistoricalRecords()


class Recibo(AuditableMixin):
    orden = models.OneToOneField(Orden, on_delete=models.CASCADE)
    s3_file = models.OneToOneField(S3File, on_delete=models.CASCADE)
    fecha_generacion = models.DateTimeField(null=True, blank=True)
    history = HistoricalRecords()


class Factura(Recibo):
    n_factura = models.PositiveIntegerField(unique=True, db_index=True)

    history = HistoricalRecords()
