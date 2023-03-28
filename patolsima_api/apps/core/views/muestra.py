from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions

from patolsima_api.apps.core.models import Muestra
from patolsima_api.apps.core.serializers import MuestraSerializer


class MuestraViewSet(viewsets.ModelViewSet):
    queryset = Muestra.objects.all()
    serializer_class = MuestraSerializer
    permission_classes = [DjangoModelPermissions & DjangoObjectPermissions]
