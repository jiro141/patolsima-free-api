from rest_framework.serializers import ModelSerializer, ReadOnlyField
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


class InformeListSerializer(ModelSerializer):
    estudio_tipo = ReadOnlyField()
    estudio_codigo = ReadOnlyField()
    estudio_paciente_id = ReadOnlyField()
    estudio_paciente_ci = ReadOnlyField()
    estudio_patologo_id = ReadOnlyField()
    estudio_patologo_name = ReadOnlyField()
    estudio_prioridad = ReadOnlyField()

    class Meta:
        model = Informe
        fields = [
            "estudio_id",
            "estudio_tipo",
            "estudio_codigo",
            "estudio_paciente_id",
            "estudio_paciente_ci",
            "estudio_patologo_id",
            "estudio_patologo_name",
            "estudio_prioridad",
            "completado",
            "aprobado",
        ]
