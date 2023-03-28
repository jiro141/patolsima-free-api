from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions

from patolsima_api.apps.core.models import Estudio
from patolsima_api.apps.core.serializers import EstudioSerializer, EstudioListSerializer


class EstudioViewSet(viewsets.ModelViewSet):
    queryset = Estudio.objects.all()
    serializer_class = EstudioSerializer
    permission_classes = [DjangoModelPermissions & DjangoObjectPermissions]

    def list(self, *args, **kwargs):
        self.serializer_class = EstudioListSerializer
        return viewsets.ModelViewSet.list(self, *args, **kwargs)
