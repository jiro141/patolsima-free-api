from rest_framework import serializers
from patolsima_api.apps.core.models import MedicoTratante


class MedicoTratanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicoTratante
        fields = [
            "id",
            "ci",
            "nombres",
            "apellidos",
            "direccion",
            "email",
            "telefono_fijo",
            "telefono_celular",
            "ncomed",
            "especialidad",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class MedicoTratanteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicoTratante
        fields = [
            "id",
            "ncomed",
            "nombres",
            "apellidos",
            "especialidad",
            "email",
            "telefono_celular",
        ]
