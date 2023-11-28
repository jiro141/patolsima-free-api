from django.db import models, transaction
from django.db.models import F, Sum, Value
from django.db.models.functions import Coalesce
from django.db.models.signals import pre_save
from decimal import Decimal
from simple_history.models import HistoricalRecords
from softdelete.models import SoftDeleteManager
from patolsima_api.utils.models import AuditableMixin, ArchivableMixing
from patolsima_api.utils.quantize import round_2_decimals
from patolsima_api.apps.core.models import Estudio
from .cliente import Cliente


class OrdenListManager(SoftDeleteManager):
    def get_queryset(self):
        from patolsima_api.apps.facturacion.utils.cambios import (
            obtener_cambio_usd_bs_mas_reciente,
        )

        cambio = obtener_cambio_usd_bs_mas_reciente()
        return (
            super()
            .get_queryset()
            .annotate(
                fecha_recepcion=F("created_at"),
                fecha_impresion=Coalesce(
                    F("factura__fecha_generacion"),
                    F("recibo__fecha_generacion"),
                ),
                total_usd=Sum("items_orden__monto_usd"),
                total_bs=(Sum("items_orden__monto_usd") * Value(cambio)),
            )
        )


class Orden(AuditableMixin, ArchivableMixing):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    confirmada = models.BooleanField(default=False)
    pagada = models.BooleanField(default=False)

    lista_ordenes = OrdenListManager()

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
            "total_bs": round_2_decimals(importe_orden_usd * cambio),
            "pagado_usd": importe_pagado_usd,
            "pagado_bs": round_2_decimals(importe_pagado_usd * cambio),
            "por_pagar_usd": (importe_orden_usd - importe_pagado_usd),
            "por_pagar_bs": round_2_decimals(
                (importe_orden_usd - importe_pagado_usd) * cambio
            ),
        }

    @transaction.atomic
    def archive(self, save_=True):
        for item in self.items_orden.all():
            item.archive(save_=save_)

        super().archive(save_=save_)


class ItemOrden(AuditableMixin, ArchivableMixing):
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

    @property
    def monto_bs(self):
        from patolsima_api.apps.facturacion.utils.cambios import (
            obtener_cambio_usd_bs_mas_reciente,
        )

        return round_2_decimals(self.monto_usd * obtener_cambio_usd_bs_mas_reciente())

    @transaction.atomic
    def archive(self, save_=True):
        if hasattr(self, "estudio"):
            self.estudio.archive(save_=save_)
        super().archive(save_=save_)


pre_save.connect(ItemOrden.pre_save, ItemOrden)
