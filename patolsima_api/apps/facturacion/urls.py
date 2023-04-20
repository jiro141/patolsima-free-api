from rest_framework import routers

from patolsima_api.apps.facturacion.views import (
    ClienteViewSet,
    OrdenViewSet,
)

router = routers.DefaultRouter()
router.register(r"clientes", ClienteViewSet, basename="cliente")
router.register(r"ordenes", OrdenViewSet, basename="orden")

urlpatterns = router.urls

# from pprint import pprint

# pprint(urlpatterns)
