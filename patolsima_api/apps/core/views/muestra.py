from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions
from rest_framework.filters import SearchFilter

from patolsima_api.apps.core.models import Muestra
from patolsima_api.apps.core.serializers import MuestraSerializer, MuestraListSerializer


class MuestraViewSet(viewsets.ModelViewSet):
    queryset = Muestra.objects.all().order_by("-estudio_id", "id")
    serializer_class = MuestraSerializer
    permission_classes = [DjangoModelPermissions & DjangoObjectPermissions]
    filter_backends = (SearchFilter,)
    search_fields = ["estudio__codigo"]

    def list(self, *args, **kwargs):
        self.serializer_class = MuestraListSerializer
        return super().list(self, *args, **kwargs)
