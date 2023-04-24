from datetime import datetime, timedelta
from decimal import Decimal
from django.conf import settings
from django.utils.timezone import make_aware
from patolsima_api.apps.facturacion.models import CambioUSDBS


def actualizar_cambio_usd_bs() -> CambioUSDBS:
    return CambioUSDBS.objects.create(bs_e=Decimal("25.00"))


def obtener_cambio_usd_bs_mas_reciente() -> Decimal:
    ultimo_cambio_creado = CambioUSDBS.objects.order_by("-created_at").first()

    if not ultimo_cambio_creado or (
        make_aware(datetime.now() - timedelta(hours=6))
        >= ultimo_cambio_creado.created_at
    ):
        ultimo_cambio_creado = actualizar_cambio_usd_bs()

    return getattr(ultimo_cambio_creado, settings.CAMBIO_USD_BS_PROPERTY_NAME)
