from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from patolsima_api.apps.core.models import Estudio
from patolsima_api.apps.core.serializers import (
    EstudioSerializer,
    EstudioListSerializer,
    EstudioCreateUpdateSerializer,
)


class EstudioViewSet(viewsets.ModelViewSet):
    queryset = Estudio.objects.with_prioridad()
    serializer_class = EstudioSerializer
    permission_classes = [DjangoModelPermissions & DjangoObjectPermissions]
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ["paciente__ci", "paciente__nombres", "paciente__apellidos"]
    filterset_fields = ["paciente", "codigo", "tipo"]

    def list(self, *args, **kwargs):
        self.serializer_class = EstudioListSerializer
        request = args[0]
        params = request.query_params
        if (
            params
            and "prioridad" in params
            and isinstance(params["prioridad"], str)
            and params["prioridad"].upper() in Estudio.Prioridad
        ):
            self.queryset = self.queryset.filter(prioridad=params["prioridad"].upper())
        return super().list(self, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.serializer_class = EstudioCreateUpdateSerializer
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.serializer_class = EstudioCreateUpdateSerializer
        return super().update(request, *args, **kwargs)
