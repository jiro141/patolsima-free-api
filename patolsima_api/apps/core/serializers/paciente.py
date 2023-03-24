from rest_framework import serializers


from patolsima_api.apps.core.models import Paciente


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = [
            "ci",
            "nombres",
            "apellidos",
            "fecha_nacimiento",
            "direccion",
            "email",
            "telefono_fijo",
            "telefono_celular",
        ]
