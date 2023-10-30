from rest_framework import serializers
from patolsima_api.apps.facturacion.models import transaccion


class TransaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = transaccion.Transaccion
        fields = "__all__"