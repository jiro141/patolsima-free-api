from rest_framework import serializers
from patolsima_api.apps.core.models import Estudio, Paciente, Patologo, MedicoTratante
from .paciente import PacienteListSerializer
from .medico_tratante import MedicoTratanteListSerializer
from .patologo import PatologoListSerializer
from .muestra import MuestraSerializer


class EstudioSerializer(serializers.ModelSerializer):
    paciente = PacienteListSerializer(read_only=True)
    medico_tratante = MedicoTratanteListSerializer(read_only=True)
    patologo = PatologoListSerializer(read_only=True)
    muestras = MuestraSerializer(read_only=True, many=True)
    prioridad = serializers.ReadOnlyField()
    codigo = serializers.ReadOnlyField()

    class Meta:
        model = Estudio
        fields = "__all__"


class EstudioListSerializer(serializers.ModelSerializer):
    paciente = PacienteListSerializer(read_only=True)
    medico_tratante = MedicoTratanteListSerializer(read_only=True)
    patologo = PatologoListSerializer(read_only=True)
    prioridad = serializers.ReadOnlyField()
    codigo = serializers.ReadOnlyField()

    class Meta:
        model = Estudio
        fields = [
            "id",
            "paciente",
            "medico_tratante",
            "patologo",
            "codigo",
            "tipo",
            "prioridad",
        ]
