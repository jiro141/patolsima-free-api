from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from patolsima_api.apps.facturacion.models import Orden
from patolsima_api.apps.facturacion.serializers import (
    OrdenSerializer,
    OrdenCreateSerializer,
)
from patolsima_api.utils.responses import method_not_allowed


class OrdenViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions & DjangoObjectPermissions]
    queryset = Orden.objects.order_by("-created_by")
    serializer_class = OrdenSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ("cliente__razon_social", "cliente__ci_rif")
    filterset_fields = ("confirmada", "pagada")

    def create(self, request, *args, **kwargs):
        self.serializer_class = OrdenCreateSerializer
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return method_not_allowed()
