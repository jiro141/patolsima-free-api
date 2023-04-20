from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions
from django_filters.rest_framework import DjangoFilterBackend

from patolsima_api.apps.core.models import (
    Estudio,
    Informe,
    InformeGenerado,
    ResultadoInmunostoquimica,
)
from patolsima_api.apps.core.serializers import (
    InformeSerializer,
    InformeListSerializer,
    InformeGeneradoSerializer,
    ResultadoInmunostoquimicaSerializer,
)
from patolsima_api.utils.responses import method_not_allowed


class InformeViewSet(viewsets.ModelViewSet):
    queryset = Informe.objects.all().order_by("-created_at")
    serializer_class = InformeSerializer
    permission_classes = [DjangoModelPermissions & DjangoObjectPermissions]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("estudio__codigo", "completado", "aprobado")

    def list(self, *args, **kwargs):
        self.serializer_class = InformeListSerializer
        request = args[0]
        params = request.query_params
        if (
            params
            and "prioridad" in params
            and isinstance(params["prioridad"], str)
            and params["prioridad"].upper() in Estudio.Prioridad
        ):
            self.queryset = self.queryset.filter(
                estudio_prioridad=params["prioridad"].upper()
            )
        return super().list(self, *args, **kwargs)


class InformeGeneradoViewSet(viewsets.ModelViewSet):
    queryset = InformeGenerado.objects.all()
    serializer_class = InformeGeneradoSerializer
    permission_classes = [DjangoModelPermissions & DjangoObjectPermissions]

    def list(self, request, *args, **kwargs):
        """
        There is no reason to include a list method because the ids will be accessible using the detail for each
        Informe instance.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return method_not_allowed()


class ResultadoInmunostoquimicaViewSet(viewsets.ModelViewSet):
    queryset = ResultadoInmunostoquimica.objects.all()
    serializer_class = ResultadoInmunostoquimicaSerializer
    permission_classes = [DjangoModelPermissions & DjangoObjectPermissions]

    def list(self, request, *args, **kwargs):
        """
        There is no reason to include a list method because the ids will be accessible using the detail for each
        Informe instance.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return method_not_allowed()
