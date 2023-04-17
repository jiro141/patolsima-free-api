from rest_framework import serializers


from patolsima_api.apps.core.models import Paciente


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = [
            "id",
            "ci",
            "nombres",
            "apellidos",
            "fecha_nacimiento",
            "edad",
            "direccion",
            "email",
            "telefono_fijo",
            "telefono_celular",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class PacienteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = [
            "id",
            "ci",
            "nombres",
            "apellidos",
            "email",
            "telefono_celular",
        ]
