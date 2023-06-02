from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import DjangoObjectPermissions
from django_filters.rest_framework import DjangoFilterBackend
from patolsima_api.apps.facturacion.serializers import ClienteSerializer
from patolsima_api.apps.facturacion.models import Cliente


class ClienteViewSet(ModelViewSet):
    permission_classes = [DjangoObjectPermissions]
    queryset = Cliente.objects.order_by("-created_at")
    serializer_class = ClienteSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ("ci_rif", "razon_social")
    filterset_fields = ("ci_rif",)
