from rest_framework import serializers
from patolsima_api.apps.core.models import Muestra


class MuestraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Muestra
        fields = [
            "id",
            "estudio",
            "tipo_de_muestra",
            "descripcion",
            "notas",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
