from rest_framework import serializers
from patolsima_api.apps.core.models import Estudio, Paciente, Patologo, MedicoTratante
from patolsima_api.apps.core.utils.serializers import (
    get_fk_objects_for_estudio_CU_serializers,
)
from patolsima_api.apps.uploaded_file_management.serializers import (
    UploadedFileSerializer,
)
from patolsima_api.utils.serializers import FileSerializer
from .paciente import PacienteListSerializer
from .medico_tratante import MedicoTratanteListSerializer
from .patologo import PatologoListSerializer
from .muestra import MuestraSerializer


class EstudioSerializer(serializers.ModelSerializer):
    paciente = PacienteListSerializer(read_only=True)
    medico_tratante = MedicoTratanteListSerializer(read_only=True)
    patologo = PatologoListSerializer(read_only=True)
    muestras = MuestraSerializer(read_only=True, many=True)
    adjuntos = UploadedFileSerializer(read_only=True, many=True)
    prioridad = serializers.ReadOnlyField()
    codigo = serializers.ReadOnlyField()
    estudio_asociado = serializers.ReadOnlyField()
    confirmado = serializers.ReadOnlyField()

    class Meta:
        model = Estudio
        fields = "__all__"


class EstudioCreateSerializer(serializers.Serializer):
    paciente_id = serializers.IntegerField(write_only=True)
    medico_tratante_id = serializers.IntegerField(write_only=True, allow_null=True)
    patologo_id = serializers.IntegerField(write_only=True, allow_null=True)
    notas = serializers.CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True
    )
    urgente = serializers.BooleanField(write_only=True, required=False)
    envio_digital = serializers.BooleanField(write_only=True, required=False)
    tipo = serializers.ChoiceField(Estudio.TipoEstudio, write_only=True)
    estudio_asociado = serializers.CharField(write_only=True, required=False)

    def create(self, validated_data):
        match validated_data:
            case {
                "paciente_id": paciente_id,
                "medico_tratante_id": medico_tratante_id,
                "patologo_id": patologo_id,
            }:
                (
                    paciente,
                    medico_tratante,
                    patologo,
                ) = get_fk_objects_for_estudio_CU_serializers(validated_data)
            case _:
                raise serializers.ValidationError(
                    "Fields paciente_id, medico_tratante_id and patologo_id needed to create an Estudio instance."
                )

        estudio = Estudio.objects.create(
            paciente=paciente,
            medico_tratante=medico_tratante,
            patologo=patologo,
            notas=validated_data.get("notas"),
            urgente=validated_data.get("urgente"),
            envio_digital=validated_data.get("envio_digital"),
            tipo=validated_data.get("tipo"),
            estudio_asociado=validated_data.get("estudio_asociado"),
        )
        return estudio

    def update(self, instance, validated_data):
        raise NotImplementedError("Method not implemented")

    @property
    def data(self):
        return EstudioSerializer(self.instance).data


class EstudioUpdateSerializer(serializers.Serializer):
    paciente_id = serializers.IntegerField(write_only=True, required=False)
    medico_tratante_id = serializers.IntegerField(write_only=True, required=False)
    patologo_id = serializers.IntegerField(write_only=True, required=False)
    notas = serializers.CharField(write_only=True, required=False)
    urgente = serializers.BooleanField(write_only=True, required=False)
    envio_digital = serializers.BooleanField(write_only=True, required=False)
    tipo = serializers.ChoiceField(Estudio.TipoEstudio, write_only=True, required=False)

    def create(self, validated_data):
        raise NotImplementedError("Method not implemented")

    def update(self, instance, validated_data):
        """
        :param instance: Estudio record that's going to be modified
        :param validated_data: Validated dict containing the keys that comes from the endpoint
        :return: instance but modified
        """

        validated_data["paciente_id"] = validated_data.pop(
            "paciente_id", instance.paciente.id
        )
        validated_data["medico_tratante_id"] = validated_data.pop(
            "medico_tratante_id", instance.medico_tratante.id
        )
        validated_data["patologo_id"] = validated_data.pop(
            "patologo_id", instance.patologo.id
        )

        paciente, medico_tratante, patologo = get_fk_objects_for_estudio_CU_serializers(
            validated_data
        )

        for field_name, field_value in validated_data.items():
            setattr(instance, field_name, field_value)

        instance.paciente = paciente
        instance.medico_tratante = medico_tratante
        instance.patologo = patologo
        instance.save()

        return instance

    @property
    def data(self):
        return EstudioSerializer(self.instance).data


class EstudioListSerializer(serializers.ModelSerializer):
    paciente = PacienteListSerializer(read_only=True)
    medico_tratante = MedicoTratanteListSerializer(read_only=True)
    patologo = PatologoListSerializer(read_only=True)
    prioridad = serializers.ReadOnlyField()
    codigo = serializers.ReadOnlyField()
    confirmado = serializers.ReadOnlyField()
    archived = serializers.ReadOnlyField()
    informe_existe = serializers.ReadOnlyField()
    informe_aprobado = serializers.ReadOnlyField()
    informe_completado = serializers.ReadOnlyField()

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
            "confirmado",
            "archived",
            "informe_existe",
            "informe_aprobado",
            "informe_completado",
            "created_at",
            "updated_at",
        ]


class ArchivoAdjuntoEstudio(FileSerializer):
    pass
