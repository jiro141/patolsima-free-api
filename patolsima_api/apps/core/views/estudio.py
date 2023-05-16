from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend

from patolsima_api.apps.core.models import Estudio
from patolsima_api.apps.core.serializers import (
    EstudioSerializer,
    EstudioListSerializer,
    EstudioCreateSerializer,
    EstudioUpdateSerializer,
    ArchivoAdjuntoEstudio,
)
from patolsima_api.apps.core.utils.estudio import append_new_adjunto, remove_adjunto


class EstudioViewSet(viewsets.ModelViewSet):
    queryset = Estudio.objects.order_by("created_at")
    serializer_class = EstudioSerializer
    permission_classes = [DjangoModelPermissions & DjangoObjectPermissions]
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ["paciente__ci", "paciente__nombres", "paciente__apellidos"]
    filterset_fields = ["paciente_id", "codigo", "tipo", "confirmado"]

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
            self.queryset = self.queryset.filter(prioridad=params["prioridad"].upper())
        return super().list(self, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.serializer_class = EstudioCreateSerializer
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.serializer_class = EstudioUpdateSerializer
        return super().update(request, *args, **kwargs)

    @action(methods=["POST"], detail=True, serializer_class=ArchivoAdjuntoEstudio)
    def adjuntos(self, request, pk=None):
        if "file" not in request.FILES:
            raise ValidationError("'file' field missing")

        return Response(
            status=200,
            data=append_new_adjunto(self.get_object(), request.FILES["file"]),
        )

    @action(methods=["DELETE"], detail=True, url_path="adjuntos/(?P<file_id>[^/.]+)")
    def adjuntar_archivo(self, request, pk=None, file_id=None):
        remove_adjunto(self.get_object(), adjunto_id=file_id)
        return Response(status=200, data={"deleted": True})
