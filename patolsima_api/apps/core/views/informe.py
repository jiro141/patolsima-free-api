from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from patolsima_api.apps.core.models import (
    Informe,
    InformeGenerado,
    ResultadoInmunostoquimica,
)
from patolsima_api.apps.core.serializers import (
    InformeSerializer,
    InformeGeneradoSerializer,
    ResultadoInmunostoquimicaSerializer,
)


class InformeViewSet(viewsets.ModelViewSet):
    queryset = Informe.objects.all().order_by("-created_at")
    serializer_class = InformeSerializer
    permission_classes = [DjangoModelPermissions & DjangoObjectPermissions]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("estudio__codigo", "completado", "aprobado")


class InformeGeneradoViewSet(viewsets.ModelViewSet):
    queryset = Informe.objects.all().order_by("-created_at")
    serializer_class = InformeSerializer
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


class ResultadoInmunostoquimicaViewSet(viewsets.ModelViewSet):
    queryset = Informe.objects.all().order_by("-created_at")
    serializer_class = InformeSerializer
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
