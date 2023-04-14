from rest_framework.serializers import ModelSerializer
from patolsima_api.apps.core.models import (
    Informe,
    InformeGenerado,
    ResultadoInmunostoquimica,
)
from patolsima_api.apps.s3_management.serializers import S3FileSerializer


class InformeGeneradoSerializer(ModelSerializer):
    s3_file = S3FileSerializer(read_only=True)

    class Meta:
        model = InformeGenerado
        fields = "__all__"


class ResultadoInmunostoquimicaSerializer(ModelSerializer):
    class Meta:
        model = ResultadoInmunostoquimica
        fields = "__all__"


class InformeSerializer(ModelSerializer):
    informes_generados = InformeGeneradoSerializer(many=True, read_only=True)
    resultadod_inmunostoquimica = ResultadoInmunostoquimicaSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = Informe
        fields = "__all__"
