from rest_framework import serializers
from patolsima_api.apps.core.models import Muestra
from .fase_muestra import FaseMuestraSerializer


class MuestraSerializer(serializers.ModelSerializer):
    fases = FaseMuestraSerializer(many=True, read_only=True)

    class Meta:
        model = Muestra
        fields = [
            "id",
            "estudio",
            "tipo_de_muestra",
            "descripcion",
            "notas",
            "estado",
            "fases",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class MuestraListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Muestra
        fields = ["id", "estudio", "estudio", "tipo_de_muestra", "estado"]
