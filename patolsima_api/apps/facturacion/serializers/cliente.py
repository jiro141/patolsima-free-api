from rest_framework import serializers
from patolsima_api.apps.facturacion.models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = "__all__"
