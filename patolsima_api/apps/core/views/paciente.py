from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from patolsima_api.apps.core.models import Paciente
from patolsima_api.apps.core.serializers import (
    PacienteSerializer,
    PacienteListSerializer,
)


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all().order_by("-created_at")
    serializer_class = PacienteSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ("ci", "nombres", "apellidos")
    filterset_fields = ("ci", "email")

    def list(self, *args, **kwargs):
        self.serializer_class = PacienteListSerializer
        return viewsets.ModelViewSet.list(self, *args, **kwargs)
