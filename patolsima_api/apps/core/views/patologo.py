from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions
from rest_framework.filters import SearchFilter

from patolsima_api.apps.core.models import Patologo
from patolsima_api.apps.core.serializers import (
    PatologoSerializer,
    PatologoListSerializer,
)


class PatologoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Patologo.objects.all()
    serializer_class = PatologoSerializer
    permission_classes = [DjangoModelPermissions & DjangoObjectPermissions]
    filter_backends = (SearchFilter,)
    search_fields = ["nombres", "apellidos", "ncomed"]

    def list(self, *args, **kwargs):
        self.serializer_class = PatologoListSerializer
        return viewsets.ModelViewSet.list(self, *args, **kwargs)
