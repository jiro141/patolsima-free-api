from rest_framework import serializers
from patolsima_api.apps.facturacion.models import Pago, NotaPago
from patolsima_api.apps.uploaded_file_management.serializers import (
    UploadedFileSerializer,
)


class NotaPagoSerializer(serializers.ModelSerializer):
    s3_file = UploadedFileSerializer(read_only=True)

    class Meta:
        model = NotaPago
        fields = "__all__"


class PagoSerializer(serializers.ModelSerializer):
    nota_de_pago = NotaPagoSerializer(read_only=True)
    total_usd = serializers.ReadOnlyField()
    pendiente_por_pagar_usd = serializers.ReadOnlyField()
    monto_bs = serializers.ReadOnlyField()
    total_bs = serializers.ReadOnlyField()
    pendiente_por_pagar_bs = serializers.ReadOnlyField()

    class Meta:
        model = Pago
        fields = "__all__"
