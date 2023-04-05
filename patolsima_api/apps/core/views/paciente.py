from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions

from patolsima_api.apps.core.models import Paciente
from patolsima_api.apps.core.serializers import (
    PacienteSerializer,
    PacienteListSerializer,
)


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all().order_by("-created_at")
    serializer_class = PacienteSerializer
    permission_classes = [DjangoModelPermissions & DjangoObjectPermissions]

    def list(self, *args, **kwargs):
        self.serializer_class = PacienteListSerializer
        return viewsets.ModelViewSet.list(self, *args, **kwargs)
