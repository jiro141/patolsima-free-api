from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions
from rest_framework.response import Response

from patolsima_api.apps.core.models import FaseMuestra
from patolsima_api.apps.core.serializers import FaseMuestraSerializer


class FaseMuestraViewSet(viewsets.ModelViewSet):
    queryset = FaseMuestra.objects.all().order_by("-muestra_id", "id")
    serializer_class = FaseMuestraSerializer
    permission_classes = [DjangoModelPermissions & DjangoObjectPermissions]

    def list(self, request, *args, **kwargs):
        """
        There is no reason to include a list method because the ids will be accessible using the detail for each
        Muestra instance.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return Response(status=405, data={"error": "Method not allowed"})
