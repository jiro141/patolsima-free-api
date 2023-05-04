from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from patolsima_api.apps.facturacion.models import Pago, NotaPago
from patolsima_api.apps.facturacion.serializers import (
    PagoSerializer,
    NotaPagoSerializer,
)
from patolsima_api.apps.facturacion.utils.pago import generar_nota_de_pago


class PagoViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions & DjangoObjectPermissions]
    queryset = Pago.objects.order_by("created_at")
    serializer_class = PagoSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("orden_id",)

    @action(detail=True, methods=["GET"])
    def nota_de_pago(self, request, pk=None):
        return Response(
            status=200,
            data=NotaPagoSerializer(generar_nota_de_pago(self.get_object())).data,
        )
