from django.http import HttpResponse
import csv
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import DjangoModelPermissions
from django_filters.rest_framework import DjangoFilterBackend
from patolsima_api.apps.facturacion.models.transaccion import Transaccion


class TransaccionesViewSet(ModelViewSet):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="exportar.csv"'

        writer = csv.writer(response)
        writer.writerow(['rif/ci', 'cliente', 'tipo','numero control', 'monto', 'fecha emision'])

        # Escribe los datos del modelo en el archivo CSV
        queryset = Transaccion.objects.all()
        for item in queryset:
            writer.writerow([item.rifci, item.cliente, item.tipo, item.n_control, item.monto, item.fecha_emision])

        return response