from patolsima_api.apps.facturacion.utils.pago import generar_notacredito, generar_notadebito
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import DjangoModelPermissions
from django_filters.rest_framework import DjangoFilterBackend
from patolsima_api.apps.facturacion.serializers import FacturaSerializer
from patolsima_api.apps.facturacion.models import Factura, NotaPago
from patolsima_api.apps.facturacion.models.recibo_y_factura import NotaCredito, NotaDebito
from patolsima_api.apps.facturacion.serializers.recibo_y_factura import NotaCreditoSerializer, NotaDebitoSerializer, FacturaOffsetSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from patolsima_api.apps.facturacion.models.recibo_y_factura import FacturaOffset


class FacturaViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Factura.objects.order_by("n_factura")
    serializer_class = FacturaSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ("n_factura", "fecha_generacion")
    filterset_fields = ("n_factura",)

class FacturaOffsetViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = FacturaOffset.objects.order_by("factura_offset").latest
    # queryset2 = FacturaOffset.objects.order_by("n_factura").latest
    # queryset = queryset1 if queryset1 > queryset2 else queryset2
    serializer_class = FacturaOffsetSerializer



class NotaCreditoViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = NotaCredito.objects.order_by("n_notacredito")
    serializer_class = NotaCreditoSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ("n_notacredito", "fecha_generacion")
    filterset_fields = ("n_notacredito",)


    @action(detail=True, methods = ["GET"])
    def nota_credito(self, request, pk=None):
        return Response(
            status=200,
            data=NotaCreditoSerializer(generar_notacredito(self.get_object())).data,
        )
    

class NotaDebitoViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = NotaDebito.objects.order_by("n_notadebito")
    serializer_class = NotaDebitoSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ("n_notadebito", "fecha_generacion")
    filterset_fields = ("n_notadebito",)


    @action(detail=True, methods = ["GET"])
    def nota_credito(self, request, pk=None):
        return Response(
            status=200,
            data=NotaCreditoSerializer(generar_notadebito(self.get_object())).data,
        )
    
    

