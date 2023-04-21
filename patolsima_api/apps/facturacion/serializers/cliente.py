from rest_framework import serializers
from patolsima_api.apps.facturacion.models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = "__all__"


class ClienteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            "id",
            "razon_social",
            "ci_rif",
            "email",
            "telefono_celular",
        ]
