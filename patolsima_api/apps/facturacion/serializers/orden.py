from decimal import Decimal
from rest_framework import serializers
from django.db import transaction
from patolsima_api.apps.facturacion.models import Orden, ItemOrden, Cliente
from patolsima_api.apps.core.models import Estudio
from .cliente import ClienteListSerializer, ClienteSerializer
from .pago import PagoSerializer
from .recibo_y_factura import FacturaSerializer, ReciboSerializer


class ItemOrdenSerializer(serializers.ModelSerializer):
    archived = serializers.ReadOnlyField()

    class Meta:
        model = ItemOrden
        fields = "__all__"


class ItemOrdenUpdateSerializer(serializers.Serializer):
    monto_usd = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=Decimal("0.00")
    )

    def update(self, instance, validated_data):
        instance.monto_usd = validated_data.get("monto_usd", Decimal("0.00"))
        instance.save()
        return instance

    @property
    def data(self):
        return ItemOrdenSerializer(self.instance).data


class OrdenSerializer(serializers.ModelSerializer):
    items_orden = ItemOrdenSerializer(many=True, read_only=True)
    pagos = PagoSerializer(many=True, read_only=True)

    confirmada = serializers.ReadOnlyField()
    pagada = serializers.ReadOnlyField()
    archived = serializers.ReadOnlyField()

    factura = FacturaSerializer(read_only=True)
    recibo = ReciboSerializer(read_only=True)

    cliente = ClienteSerializer(read_only=True)
    balance = serializers.ReadOnlyField()

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

        estudios = Estudio.objects.filter(
            id__in=estudio_ids, items_orden__isnull=True
        ).all()
        if estudios.count() != len(estudio_ids):
            raise serializers.ValidationError(
                "The number of matching Estudio instances in the database is different than the number in 'estudio_ids'"
            )

        estudio1 = estudios.first()
        cliente, created = Cliente.objects.get_or_create(
            ci_rif=f"{estudio1.paciente.ci}",
            defaults={
                "razon_social": estudio1.paciente.nombre_completo,
                "telefono_fijo": estudio1.paciente.telefono_fijo,
                "telefono_celular": estudio1.paciente.telefono_celular,
                "direccion": estudio1.paciente.direccion,
            },
        )

        orden = Orden.objects.create(cliente=cliente)
        items_orden = [ItemOrden(estudio=estudio, orden=orden) for estudio in estudios]
        ItemOrden.objects.bulk_create(items_orden)
        return orden

    @property
    def data(self):
        return OrdenSerializer(self.instance).data


class OrdenUpdateSerializer(serializers.Serializer):
    cliente_id = serializers.IntegerField(required=True, allow_null=False)

    def update(self, instance: Orden, validated_data):
        cliente_id = validated_data["cliente_id"]

        # if instance.pagada:
        #     raise ValueError(
        #         f"Orden {instance.id} is already payed. Cliente can not be changed if it's payed"
        #     )

        with transaction.atomic():
            cliente = Cliente.objects.get(id=cliente_id)
            instance.cliente = cliente
            instance.save()

        return instance

    @property
    def data(self):
        return OrdenSerializer(self.instance).data


class OrdenListSerializer(serializers.ModelSerializer):
    cliente = ClienteListSerializer(read_only=True)
    fecha_recepcion = serializers.ReadOnlyField()
    fecha_impresion = serializers.ReadOnlyField()
    total_usd = serializers.ReadOnlyField()
    total_bs = serializers.ReadOnlyField()
    archived = serializers.ReadOnlyField()

    class Meta:
        model = Orden
        fields = [
            "id",
            "cliente",
            "confirmada",
            "pagada",
            "archived",
            "fecha_recepcion",
            "fecha_impresion",
            "total_usd",
            "total_bs",
            # "n_estudios",
            # "total",
            # "deauda"
        ]
