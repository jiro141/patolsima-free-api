from rest_framework.serializers import Serializer
from patolsima_api.apps.core.models import FaseMuestra
from patolsima_api.apps.s3_management.serializers import S3FileSerializer


class FaseMuestraSerializer(Serializer):
    adjuntos = S3FileSerializer(many=True, read_only=True)

    class Meta:
        model = FaseMuestra
        fields = "__all__"
