from django.db import models
from django.db.models.signals import pre_save
from decimal import Decimal
from simple_history.models import HistoricalRecords
from patolsima_api.utils.models import AuditableMixin, TelefonoMixin, DireccionMixin
from patolsima_api.apps.core.models import Estudio
from patolsima_api.apps.uploaded_file_management.models import UploadedFile
from .cliente import Cliente


class Orden(AuditableMixin):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    confirmada = models.BooleanField(default=False)
    pagada = models.BooleanField(default=False)
    history = HistoricalRecords()

    @property
    def importe_orden_usd(self) -> Decimal:
        return self.balance["total_usd"]

    @property
    def importe_pagado_usd(self) -> Decimal:
        return self.balance["pagado_usd"]

    @property
    def importe_orden_bs(self) -> Decimal:
        return self.balance["total_bs"]

    @property
    def importe_pagado_bs(self) -> Decimal:
        return self.balance["pagado_bs"]

    @property
    def balance(self) -> dict:
        from patolsima_api.apps.facturacion.utils.cambios import (
            obtener_cambio_usd_bs_mas_reciente,
        )

        importe_orden_usd = self.items_orden.aggregate(
            sum_costo=models.Sum("monto_usd")
        )["sum_costo"] or Decimal("0.00")
        importe_pagado_usd = self.pagos.aggregate(sum_total=models.Sum("monto_usd"))[
            "sum_total"
        ] or Decimal("0.00")
        cambio = obtener_cambio_usd_bs_mas_reciente()
        return {
            "total_usd": importe_orden_usd,
            "total_bs": importe_orden_usd * cambio,
            "pagado_usd": importe_pagado_usd,
            "pagado_bs": importe_pagado_usd * cambio,
            "por_pagar_usd": (importe_orden_usd - importe_pagado_usd),
            "por_pagar_bs": (importe_orden_usd - importe_pagado_usd) * cambio,
        }


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
