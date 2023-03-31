from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from patolsima_api.apps.core.models import Estudio
from patolsima_api.apps.core.serializers import EstudioSerializer, EstudioListSerializer


class EstudioViewSet(viewsets.ModelViewSet):
    queryset = Estudio.objects.all()
    serializer_class = EstudioSerializer
    permission_classes = [DjangoModelPermissions & DjangoObjectPermissions]
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ["paciente__nombres", "paciente__apellidos"]
    filter_fields = ["paciente__ci", "codigo", "tipo"]

    def list(self, *args, **kwargs):
        self.serializer_class = EstudioListSerializer
        return viewsets.ModelViewSet.list(self, *args, **kwargs)
