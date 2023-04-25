from django.db import models
from django.db.models import functions as model_functions
from django.db.models.signals import pre_save, post_save
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

    @classmethod
    def pre_save(cls, sender, instance, *args, **kwargs):
        orden = instance.orden

        if orden.pagada and instance.monto_usd >= Decimal("0.0"):
            raise Exception("Esta orden ya esta pagada")

        total_orden = orden.items_orden.aggregate(
            sum_costo=model_functions.Coalesce(models.Sum("monto_usd"), Decimal("0.00"))
        )["sum_costo"]
        print(f"total_orden={total_orden}")
        qs = orden.pagos
        if instance.id:
            qs = qs.exclude(id=instance.id)
        suma_pagos = qs.aggregate(
            sum_total=model_functions.Coalesce(models.Sum("monto_usd"), Decimal("0.00"))
        )["sum_total"]
        print(f"suma_pagos={suma_pagos}")
        if (suma_pagos + instance.monto_usd) > total_orden:
            raise Exception(
                "El monto a guardar excederia lo que debe pagarse por la orden"
            )
        elif (suma_pagos + instance.monto_usd) < Decimal("0.0"):
            raise Exception(
                "El monto a guardar hace que el total pagado sea menor a 0."
            )

        instance.pendiente_por_pagar_usd = total_orden - (
            suma_pagos + instance.monto_usd
        )
        instance.total_usd = total_orden

        from patolsima_api.apps.facturacion.utils.cambios import (
            obtener_cambio_usd_bs_mas_reciente,
        )

        cambio_actual = obtener_cambio_usd_bs_mas_reciente()
        instance.monto_bs = instance.monto_usd * cambio_actual
        instance.pendiente_por_pagar_bs = (
            instance.pendiente_por_pagar_usd * cambio_actual
        )
        instance.total_bs = instance.total_usd * cambio_actual

    @classmethod
    def post_save(cls, sender, instance, created, *args, **kwargs):
        orden = instance.orden
        total_orden = orden.items_orden.aggregate(sum_costo=models.Sum("monto_usd"))[
            "sum_costo"
        ]
        suma_pagos = orden.pagos.aggregate(sum_total=models.Sum("monto_usd"))[
            "sum_total"
        ]
        print("Luego de guardar--------------------")
        print(f"total_orden={total_orden}")
        print(f"suma_pagos={suma_pagos}")
        if total_orden == suma_pagos:
            orden.pagada = True
        else:
            orden.pagada = False
        orden.save()


pre_save.connect(Pago.pre_save, sender=Pago)
post_save.connect(Pago.post_save, sender=Pago)


class NotaPago(AuditableMixin):
    pago = models.OneToOneField(
        Pago, on_delete=models.CASCADE, related_name="nota_de_pago"
    )
    s3_file = models.OneToOneField(
        S3File, on_delete=models.CASCADE, null=True, blank=True
    )
    history = HistoricalRecords()
