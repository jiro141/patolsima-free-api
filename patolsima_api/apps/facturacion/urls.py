from patolsima_api.apps.facturacion.views.transaccion import TransaccionesViewSet
from rest_framework import routers
from django.urls import include, path

from patolsima_api.apps.facturacion.views import (
    ClienteViewSet,
    OrdenViewSet,
    ItemOrdenViewSet,
    PagoViewSet,
    CambioDelDiaView,

)

from patolsima_api.apps.facturacion.views.recibo_y_factura import FacturaViewSet, FacturaOffsetViewSet, NotaCreditoViewSet, NotaDebitoViewSet


router = routers.DefaultRouter()
router.register(r"clientes", ClienteViewSet, basename="cliente")
router.register(r"facturas", FacturaViewSet, basename="factura")
router.register(r"notacredito", NotaCreditoViewSet, basename="notacredito")
router.register(r"notadebito", NotaDebitoViewSet, basename="notadebito")
router.register(r"offsetfactura", FacturaOffsetViewSet, basename="offsetfactura")
router.register(r"reporte", TransaccionesViewSet, basename="transacciones")
router.register(r"ordenes", OrdenViewSet, basename="orden")
router.register(r"itemsorden", ItemOrdenViewSet, basename="item-orden")
router.register(r"pagos", PagoViewSet, basename="pago")
urlpatterns = [path(r"cambiodeldia", CambioDelDiaView.as_view()), *router.urls]
 