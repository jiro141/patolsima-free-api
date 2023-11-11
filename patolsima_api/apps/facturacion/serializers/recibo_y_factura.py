from rest_framework import serializers
from patolsima_api.apps.facturacion.models import Factura, Recibo
from patolsima_api.apps.uploaded_file_management.serializers import (
    UploadedFileSerializer,
)

from patolsima_api.apps.facturacion.models.recibo_y_factura import NotaCredito, NotaDebito, FacturaOffset


class ReciboSerializer(serializers.ModelSerializer):
    s3_file = UploadedFileSerializer(read_only=True)

    class Meta:
        model = Recibo
        fields = "__all__"


class FacturaSerializer(serializers.ModelSerializer):
    s3_file = UploadedFileSerializer(read_only=True)

    class Meta:
        model = Factura
        fields = "__all__"


class FacturaCreateSerializer(serializers.Serializer):
    n_factura = serializers.IntegerField(min_value=1)
    class Meta:
        model = Factura
        fields = '__all__'

class FacturaOffsetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacturaOffset
        fields = '__all__'

class NotaCreditoSerializer(serializers.ModelSerializer):
    s3_file = UploadedFileSerializer(read_only=True)

    class Meta:
        model = NotaCredito
        fields = "__all__"

    
class NotaDebitoSerializer(serializers.ModelSerializer):
    s3_file = UploadedFileSerializer(read_only=True)

    class Meta:
        model = NotaDebito
        fields = "__all__"