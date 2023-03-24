from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions

from patolsima_api.apps.core.models import Paciente
from patolsima_api.apps.core.serializers import PacienteSerializer


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    permission_classes = [DjangoModelPermissions & DjangoObjectPermissions]
