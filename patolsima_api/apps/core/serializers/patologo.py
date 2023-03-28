from rest_framework import serializers
from patolsima_api.apps.core.models import Patologo


class PatologoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patologo
        fields = [
            "ncomed",
            "firma",
            "nombres",
            "apellidos",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class PatologoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patologo
        fields = [
            "nombres",
            "apellidos",
        ]
