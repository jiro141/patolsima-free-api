from rest_framework import serializers
from django.db import transaction
from patolsima_api.apps.facturacion.models import Orden, ItemOrden, Cliente
from patolsima_api.apps.core.models import Estudio
from .pago import PagoSerializer


class ItemOrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOrden
        fields = "__all__"


class OrdenSerializer(serializers.ModelSerializer):
    items_orden = ItemOrdenSerializer(many=True, read_only=True)
    pagos = PagoSerializer(many=True, read_only=True)

    confirmada = serializers.ReadOnlyField()
    pagada = serializers.ReadOnlyField()

    class Meta:
        model = Orden
        fields = "__all__"


class OrdenCreateSerializer(serializers.Serializer):
    estudio_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1), min_length=1
    )

    @transaction.atomic
    def create(self, validated_data):
        estudio_ids = validated_data["estudio_ids"]

        estudios = Estudio.objects.filter(id__in=estudio_ids).all()
        if estudios.count() != len(estudio_ids):
            raise serializers.ValidationError(
                "The number of matching Estudio instances in the database is different than the number in 'estudio_ids'"
            )

        estudio1 = estudios.first()
        cliente = Cliente.objects.get_or_create(
            ci_rif=f"V{estudio1.paciente.ci}",
            defaults={
                "razon_social": estudio1.paciente.nombre_completo,
                "telefono_fijo": estudio1.paciente.telefono_fijo,
                "telefono_celular": estudio1.paciente.telefono_celular,
                "direccion": estudio1.paciente.direccion,
            },
        )

        orden = Orden(cliente=cliente)
        items_orden = [ItemOrden(estudio=estudio, orden=orden) for estudio in estudios]
        ItemOrden.objects.bulk_create(items_orden)
        return orden
