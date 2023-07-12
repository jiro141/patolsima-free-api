from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from patolsima_api.apps.core.models import Muestra
from patolsima_api.apps.core.serializers import MuestraSerializer, MuestraListSerializer


class MuestraViewSet(viewsets.ModelViewSet):
    queryset = Muestra.objects.all().order_by("-estudio_id", "id")
    serializer_class = MuestraSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ["estudio__codigo"]
    filterset_fields = ("estudio_id", "estado", "archived")

    def list(self, *args, **kwargs):
        self.serializer_class = MuestraListSerializer
        return super().list(self, *args, **kwargs)
