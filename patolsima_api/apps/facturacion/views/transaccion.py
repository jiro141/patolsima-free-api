from django.http import HttpResponse
import csv
from patolsima_api.apps.facturacion.serializers.transaccion import TransaccionSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import DjangoModelPermissions
from django_filters.rest_framework import DjangoFilterBackend
from patolsima_api.apps.facturacion.models.transaccion import Transaccion
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import date


class TransaccionesViewSet(ModelViewSet):
    queryset = Transaccion.objects.all()  
    serializer_class = TransaccionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    permission_classes = [DjangoModelPermissions]  

    @action(detail=False, methods=['get'])
    def download_csv(self, request):

        # Get the date filter from the request parameters (assuming 'start_date' and 'end_date' are provided)
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        # Process start_date and end_date strings into date objects
        start_date = date.fromisoformat(start_date_str) if start_date_str else None
        end_date = date.fromisoformat(end_date_str) if end_date_str else None

        queryset = self.get_queryset()

        # Filter queryset based on date range if start_date and end_date are provided
        if start_date and end_date:
            queryset = queryset.filter(fecha_emision__range=(start_date, end_date))
        response = HttpResponse(
                content_type="text/csv",
                headers={"Content-Disposition": 'attachment; filename="reporte.csv"'},
                )
        writer = csv.writer(response)
        writer.writerow(['rif/ci', 'cliente', 'tipo', 'numero control', 'monto', 'fecha emision'])

        if queryset.exists():  # Check if queryset has any data
            for item in queryset:
                writer.writerow([
                    item.rifci, item.cliente, item.tipo,
                    item.n_control, item.monto, item.fecha_emision
                ])
        else:
            writer.writerow(['No data found'])  # Indicate if there is no data in CSV

        return response