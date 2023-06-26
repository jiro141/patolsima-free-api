from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from django_filters.rest_framework import DjangoFilterBackend

from patolsima_api.apps.core.models import (
    Estudio,
    Informe,
    ResultadoInmunostoquimica,
)
from patolsima_api.apps.core.serializers import (
    InformeSerializer,
    InformeListSerializer,
    ResultadoInmunostoquimicaSerializer,
)
from patolsima_api.apps.core.utils.informes import (
    generar_informe_preview,
    generar_y_guardar_informe,
    completar_informe,
    aprobar_informe,
)
from patolsima_api.utils.responses import method_not_allowed


class InformeViewSet(viewsets.ModelViewSet):
    queryset = Informe.objects.all().order_by("-created_at")
    serializer_class = InformeSerializer
    permission_classes = [DjangoModelPermissions]
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

    @action(detail=True, methods=["GET"])
    def pdf_preview(self, request, pk=None):
        return generar_informe_preview(self.get_object())

    @action(detail=True, methods=["GET"])
    def generate_pdf(self, request, pk=None):
        return Response(status=200, data=generar_y_guardar_informe(self.get_object()))

    @action(detail=True, methods=["POST"])
    def completado(self, request: Request, pk=None):
        return Response(
            status=200, data={"confirm": completar_informe(self.get_object())}
        )

    @action(detail=True, methods=["POST"])
    def aprobar(self, request: Request, pk=None):
        return Response(
            status=200, data={"confirm": aprobar_informe(self.get_object())}
        )


class ResultadoInmunostoquimicaViewSet(viewsets.ModelViewSet):
    queryset = ResultadoInmunostoquimica.objects.all()
    serializer_class = ResultadoInmunostoquimicaSerializer
    permission_classes = [DjangoModelPermissions]

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
