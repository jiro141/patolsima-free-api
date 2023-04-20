from django.db import models
from decimal import Decimal
from simple_history.models import HistoricalRecords
from patolsima_api.utils.models import AuditableMixin
from patolsima_api.apps.s3_management.models import S3File
from .orden import Orden


class Recibo(AuditableMixin):
    orden = models.OneToOneField(Orden, on_delete=models.CASCADE)
    s3_file = models.OneToOneField(S3File, on_delete=models.CASCADE)
    fecha_generacion = models.DateTimeField(null=True, blank=True)
    history = HistoricalRecords()


class Factura(Recibo):
    n_factura = models.PositiveIntegerField(unique=True, db_index=True)

    history = HistoricalRecords()
