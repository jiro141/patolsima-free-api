from rest_framework import routers
from django.urls import include, path

from patolsima_api.apps.facturacion.views import (
    ClienteViewSet,
    OrdenViewSet,
    ItemOrdenViewSet,
    PagoViewSet,
    CambioDelDiaView,
)

router = routers.DefaultRouter()
router.register(r"clientes", ClienteViewSet, basename="cliente")
router.register(r"ordenes", OrdenViewSet, basename="orden")
router.register(r"itemsorden", ItemOrdenViewSet, basename="item-orden")
router.register(r"pagos", PagoViewSet, basename="pago")
urlpatterns = [path(r"cambiodeldia", CambioDelDiaView.as_view()), *router.urls]
