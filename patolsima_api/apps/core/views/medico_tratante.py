from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions
from rest_framework.filters import SearchFilter

from patolsima_api.apps.core.models import MedicoTratante
from patolsima_api.apps.core.serializers import (
    MedicoTratanteListSerializer,
    MedicoTratanteSerializer,
)


class MedicoTratanteViewSet(viewsets.ModelViewSet):
    queryset = MedicoTratante.objects.all().order_by("-created_at")
    serializer_class = MedicoTratanteSerializer
    permission_classes = [DjangoModelPermissions & DjangoObjectPermissions]
    filter_backends = (SearchFilter,)
    search_fields = ["nombres", "apellidos", "especialidad", "ncomed"]

    def list(self, *args, **kwargs):
        self.serializer_class = MedicoTratanteListSerializer
        return viewsets.ModelViewSet.list(self, *args, **kwargs)
