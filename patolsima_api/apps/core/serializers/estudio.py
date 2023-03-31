from rest_framework import serializers
from patolsima_api.apps.core.models import Estudio
from .paciente import PacienteListSerializer
from .medico_tratante import MedicoTratanteListSerializer
from .patologo import PatologoListSerializer
from .muestra import MuestraSerializer


class EstudioSerializer(serializers.ModelSerializer):
    paciente = PacienteListSerializer(read_only=True)
    medico_tratante = MedicoTratanteListSerializer(read_only=True)
    patologo = PatologoListSerializer(read_only=True)
    muestras = MuestraSerializer(read_only=True, many=True)

    class Meta:
        model = Estudio
        fields = [
            "id",
            "paciente",
            "medico_tratante",
            "patologo",
            "adjuntos",
            "codigo",
            "notas",
            "urgente",
            "envio_digital",
            "tipo",
            "muestras",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class EstudioListSerializer(serializers.ModelSerializer):
    paciente = PacienteListSerializer(read_only=True)
    medico_tratante = MedicoTratanteListSerializer(read_only=True)
    patologo = PatologoListSerializer(read_only=True)

    class Meta:
        model = Estudio
        fields = [
            "id",
            "paciente",
            "medico_tratante",
            "patologo",
            "codigo",
            "tipo",
        ]
