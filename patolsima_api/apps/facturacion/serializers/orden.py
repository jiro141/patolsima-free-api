from rest_framework import serializers
from patolsima_api.apps.facturacion.models import Orden, ItemOrden
from .pago import PagoSerializer


class ItemOrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOrden
        fields = "__all__"


class OrdenSerializer(serializers.ModelSerializer):
    items_orden = ItemOrdenSerializer(many=True, read_only=True)
    pagos = PagoSerializer(many=True, read_only=True)

    class Meta:
        model = Orden
        fields = "__all__"
