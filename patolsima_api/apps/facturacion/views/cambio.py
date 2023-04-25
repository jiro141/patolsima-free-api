from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from patolsima_api.apps.facturacion.utils.cambios import (
    obtener_cambio_usd_bs_mas_reciente,
)


class CambioDelDiaView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        return Response(
            status=200, data={"usd_bs": obtener_cambio_usd_bs_mas_reciente()}
        )
