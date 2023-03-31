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
        request = args[0]
        params = request.query_params
        if (
            params
            and "prioridad" in params
            and isinstance(params["prioridad"], str)
            and params["prioridad"].upper() in Estudio.Prioridad
        ):
            self.queryset = Estudio.add_priority_to_list_queryset(self.get_queryset())
            self.queryset = self.queryset.filter(prioridad=params["prioridad"].upper())
        return viewsets.ModelViewSet.list(self, *args, **kwargs)
