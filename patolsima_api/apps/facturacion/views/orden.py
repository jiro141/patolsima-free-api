from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from patolsima_api.apps.facturacion.models import Orden, ItemOrden
from patolsima_api.apps.facturacion.serializers import (
    OrdenSerializer,
    OrdenCreateSerializer,
    ItemOrdenSerializer,
    ItemOrdenUpdateSerializer,
)
from patolsima_api.apps.facturacion.utils.orden import confirm_orden
from patolsima_api.utils.responses import method_not_allowed


class OrdenViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions & DjangoObjectPermissions]
    queryset = Orden.objects.order_by("-created_at")
    serializer_class = OrdenSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ("cliente__razon_social", "cliente__ci_rif")
    filterset_fields = ("confirmada", "pagada")

    def create(self, request, *args, **kwargs):
        self.serializer_class = OrdenCreateSerializer
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return method_not_allowed()

    @action(detail=True, methods=["post"])
    def confirmar(self, request, pk=None):
        return Response(status=200, data={"confirm": confirm_orden(self.get_object())})


class ItemOrdenViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions & DjangoObjectPermissions]
    queryset = ItemOrden.objects.order_by("-order_id", "-creation_date")
    serializer_class = ItemOrdenSerializer

    def list(self, request, *args, **kwargs):
        return method_not_allowed()

    def update(self, request, *args, **kwargs):
        self.serializer_class = ItemOrdenUpdateSerializer
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return method_not_allowed()
