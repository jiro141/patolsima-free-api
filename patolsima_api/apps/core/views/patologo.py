from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions

from patolsima_api.apps.core.models import Patologo
from patolsima_api.apps.core.serializers import (
    PatologoSerializer,
    PatologoListSerializer,
)


class PatologoViewSet(viewsets.ModelViewSet):
    queryset = Patologo.objects.all()
    serializer_class = PatologoSerializer
    permission_classes = [DjangoModelPermissions & DjangoObjectPermissions]

    def list(self, *args, **kwargs):
        self.serializer_class = PatologoListSerializer
        return viewsets.ModelViewSet.list(self, *args, **kwargs)
