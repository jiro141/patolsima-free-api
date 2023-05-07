from rest_framework.serializers import ModelSerializer
from patolsima_api.apps.core.models import FaseMuestra
from patolsima_api.apps.uploaded_file_management.serializers import (
    UploadedFileSerializer,
)


class FaseMuestraSerializer(ModelSerializer):
    adjuntos = UploadedFileSerializer(many=True, read_only=True)

    class Meta:
        model = FaseMuestra
        fields = "__all__"
