from patolsima_api.apps.facturacion.serializers.recibo_y_factura import NotaDebitoSerializer
from patolsima_api.apps.facturacion.utils.pago import generar_notacredito, generar_notadebito
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from patolsima_api.apps.facturacion.models import Orden, ItemOrden
from patolsima_api.apps.facturacion.serializers import (
    OrdenSerializer,
    OrdenCreateSerializer,
    OrdenUpdateSerializer,
    OrdenListSerializer,
    ItemOrdenSerializer,
    ItemOrdenUpdateSerializer,
    FacturaCreateSerializer,
    ReciboSerializer,
    FacturaSerializer,
)
from patolsima_api.apps.facturacion.utils.orden import (
    confirm_orden,
    generar_recibo_o_factura,
    archivar_orden,
)
from patolsima_api.utils.responses import method_not_allowed


class OrdenViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Orden.objects.order_by("-created_at")
    serializer_class = OrdenSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ("cliente__razon_social", "cliente__ci_rif")
    filterset_fields = ("confirmada", "pagada", "archived")

    def list(self, request: Request, *args, **kwargs):
        self.serializer_class = OrdenListSerializer
        self.queryset = Orden.lista_ordenes.order_by("-created_at")
        return super().list(request, *args, **kwargs)

    def create(self, request: Request, *args, **kwargs):
        self.serializer_class = OrdenCreateSerializer
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.serializer_class = OrdenUpdateSerializer
        return super().update(request, *args, *kwargs)

    @action(detail=True, methods=["post"])
    def confirmar(self, request: Request, pk=None):
        return Response(status=200, data={"confirm": confirm_orden(self.get_object())})

    @action(detail=True, methods=["post"])
    def archivar(self, request: Request, pk=None):
        return Response(status=200, data={"confirm": archivar_orden(self.get_object())})

    @action(detail=True, methods=["post"])
    def recibo(self, request: Request, pk=None):
        return Response(
            status=200,
            data={
                "confirm": ReciboSerializer(
                    generar_recibo_o_factura(self.get_object(), "recibo")
                ).data
            },
        )

    @action(detail=True, methods=["post"])
    def factura(self, request: Request, pk=None):
        request_data = FacturaCreateSerializer(request.data).data
        return Response(
            status=200,
            data={
                "confirm": FacturaSerializer(
                    generar_recibo_o_factura(
                        self.get_object(),
                        "factura",
                        n_factura=request_data.get("n_factura"),
                    )
                ).data
            },
        )
    
    @action(detail=True, methods=["post"])
    def notadebito(self, request: Request, pk=None):
        request_data = NotaDebitoSerializer(request.data).data
        return Response(
            status=200,
            data={
                "confirm": FacturaSerializer(
                    generar_notadebito(
                        self.get_object(),
                        "factura",
                        n_factura=request_data.get("n_factura"),
                    )
                ).data
            },
        )
    
    @action(detail=True, methods=["post"])
    def notacredito(self, request: Request, pk=None):
        request_data = FacturaCreateSerializer(request.data).data
        return Response(
            status=200,
            data={
                "confirm": FacturaSerializer(
                    generar_notacredito(
                        self.get_object(),
                        "factura",
                        n_factura=request_data.get("n_factura"),
                    )
                ).data
            },
        )


class ItemOrdenViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = ItemOrden.objects.order_by("-orden_id", "-created_at")
    serializer_class = ItemOrdenSerializer

    def list(self, request, *args, **kwargs):
        return method_not_allowed()

    def update(self, request, *args, **kwargs):
        self.serializer_class = ItemOrdenUpdateSerializer
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return method_not_allowed()
