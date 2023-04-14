from rest_framework import serializers
from patolsima_api.apps.core.models import Estudio, Paciente, Patologo, MedicoTratante


def get_fk_objects_for_estudio_CU_serializers(validated_data):
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
