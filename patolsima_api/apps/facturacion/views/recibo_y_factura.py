from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import DjangoModelPermissions
from django_filters.rest_framework import DjangoFilterBackend
from patolsima_api.apps.facturacion.serializers import FacturaSerializer
from patolsima_api.apps.facturacion.models import Factura


class FacturaViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Factura.objects.order_by("n_factura")
    serializer_class = FacturaSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ("n_factura", "fecha_generacion")
    filterset_fields = ("n_factura",) 
