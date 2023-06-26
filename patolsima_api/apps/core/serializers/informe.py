from rest_framework.serializers import ModelSerializer, ReadOnlyField, ValidationError
from django.db import transaction
from patolsima_api.apps.core.models import (
    Estudio,
    Informe,
    ResultadoInmunostoquimica,
    Patologo,
)
from patolsima_api.apps.core.utils.patologo import check_user_is_patologo
from patolsima_api.apps.uploaded_file_management.serializers import (
    UploadedFileSerializer,
)


class ResultadoInmunostoquimicaSerializer(ModelSerializer):
    def create(self, validated_data):
        informe = validated_data["informe"]
        if informe.estudio.tipo != Estudio.TipoEstudio.INMUNOSTOQUIMICA:
            raise ValidationError(
                "Estudio.tipo must be Estudio.TipoEstudio.INMUNOSTOQUIMICA"
            )

        resultado_inmunostoquimica = ResultadoInmunostoquimica.objects.create(
            informe=informe,
            procedimiento=validated_data.get("procedimiento"),
            reaccion=validated_data.get("reaccion"),
            diagnostico_observaciones=validated_data.get("diagnostico_observaciones"),
        )

        return resultado_inmunostoquimica

    def update(self, instance, validated_data):
        validated_data.pop(
            "informe", None
        )  # Informe should be immutable after creating Inmunostoquimica rows

        for field_name, field_value in validated_data.items():
            setattr(instance, field_name, field_value)

        return instance

    class Meta:
        model = ResultadoInmunostoquimica
        fields = "__all__"


class InformeSerializer(ModelSerializer):
    informes_generado = UploadedFileSerializer(read_only=True)
    resultadod_inmunostoquimica = ResultadoInmunostoquimicaSerializer(
        many=True, read_only=True
    )

    def create(self, validated_data):
        patologo = check_user_is_patologo(self.context["request"].user)
        with transaction.atomic():
            new_informe = super().create(validated_data)
            estudio = new_informe.estudio
            estudio.patologo = patologo
            estudio.save()

        return new_informe

    def update(self, instance, validated_data):
        for field_name, field_value in validated_data.items():
            if field_name in ("completado", "aprobado"):
                continue
            setattr(instance, field_name, field_value)

        return instance

    class Meta:
        model = Informe
        fields = "__all__"


class InformeListSerializer(ModelSerializer):
    estudio_tipo = ReadOnlyField()
    estudio_codigo = ReadOnlyField()
    estudio_paciente_id = ReadOnlyField()
    estudio_paciente_ci = ReadOnlyField()
    estudio_patologo_id = ReadOnlyField()
    estudio_patologo_name = ReadOnlyField()
    estudio_prioridad = ReadOnlyField()

    class Meta:
        model = Informe
        fields = [
            "estudio_id",
            "estudio_tipo",
            "estudio_codigo",
            "estudio_paciente_id",
            "estudio_paciente_ci",
            "estudio_patologo_id",
            "estudio_patologo_name",
            "estudio_prioridad",
            "completado",
            "aprobado",
            "created_at",
            "updated_at",
        ]
