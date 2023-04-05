from rest_framework import serializers
from patolsima_api.apps.core.models import Estudio, Paciente, Patologo, MedicoTratante
from patolsima_api.apps.s3_management.serializers import S3FileSerializer
from .paciente import PacienteListSerializer
from .medico_tratante import MedicoTratanteListSerializer
from .patologo import PatologoListSerializer
from .muestra import MuestraSerializer


class EstudioSerializer(serializers.ModelSerializer):
    paciente = PacienteListSerializer(read_only=True)
    medico_tratante = MedicoTratanteListSerializer(read_only=True)
    patologo = PatologoListSerializer(read_only=True)
    muestras = MuestraSerializer(read_only=True, many=True)
    adjuntos = S3FileSerializer(read_only=True, many=True)
    prioridad = serializers.ReadOnlyField()
    codigo = serializers.ReadOnlyField()

    class Meta:
        model = Estudio
        fields = "__all__"


class EstudioCreateUpdateSerializer(serializers.Serializer):
    paciente_ci = serializers.IntegerField(write_only=True)
    medico_tratante_id = serializers.IntegerField(write_only=True)
    patologo_id = serializers.IntegerField(write_only=True)
    notas = serializers.CharField(write_only=True)
    urgente = serializers.BooleanField(write_only=True)
    envio_digital = serializers.BooleanField(write_only=True)
    tipo = serializers.ChoiceField(Estudio.TipoEstudio, write_only=True)

    def _get_fk_objects(self, validated_data):
        paciente_ci, medico_tratante_id, patologo_id = (
            validated_data.pop("paciente_ci"),
            validated_data.pop("medico_tratante_id"),
            validated_data.pop("patologo_id"),
        )
        try:
            paciente = Paciente.objects.get(ci=paciente_ci)
            medico_tratante = MedicoTratante.objects.get(id=medico_tratante_id)
            patologo = Patologo.objects.get(id=patologo_id)
        except Paciente.DoesNotExist:
            raise serializers.ValidationError(f"paciente {paciente_ci} not found.")
        except MedicoTratante.DoesNotExist:
            raise serializers.ValidationError(
                f"medico tratante {medico_tratante_id} not found."
            )
        except Patologo.DoesNotExist:
            raise serializers.ValidationError(f"patologo {patologo_id} not found.")

        return paciente, medico_tratante, patologo

    def create(self, validated_data):
        match validated_data:
            case {
                "paciente_ci": paciente_ci,
                "medico_tratante_id": medico_tratante_id,
                "patologo_id": patologo_id,
            }:
                paciente, medico_tratante, patologo = self._get_fk_objects(
                    validated_data
                )
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
        )
        return estudio

    def update(self, instance, validated_data):
        """
        :param instance: Estudio record that's going to be modified
        :param validated_data: Validated dict containing the keys that comes from the endpoint
        :return: instance but modified
        """

        validated_data["paciente_ci"] = validated_data.pop(
            "paciente_ci", instance.paciente.ci
        )
        validated_data["medico_tratante_id"] = validated_data.pop(
            "medico_tratante_id", instance.medico_tratante.id
        )
        validated_data["patologo_id"] = validated_data.pop(
            "patologo_id", instance.patologo.id
        )

        paciente, medico_tratante, patologo = self._get_fk_objects(validated_data)

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
