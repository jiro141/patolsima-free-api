from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions

from patolsima_api.apps.core.models import MedicoTratante
from patolsima_api.apps.core.serializers import (
    MedicoTratanteListSerializer,
    MedicoTratanteSerializer,
)


class MedicoTratanteViewSet(viewsets.ModelViewSet):
    queryset = MedicoTratante.objects.all()
    serializer_class = MedicoTratanteSerializer
    permission_classes = [DjangoModelPermissions & DjangoObjectPermissions]

    def list(self, *args, **kwargs):
        self.serializer_class = MedicoTratanteListSerializer
        return viewsets.ModelViewSet.list(self, *args, **kwargs)
