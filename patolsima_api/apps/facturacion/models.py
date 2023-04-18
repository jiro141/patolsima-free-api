from django.db import models
from simple_history.models import HistoricalRecords
from patolsima_api.utils.models import AuditableMixin


class ItemRecibo(AuditableMixin):
    descripcion = models.CharField(max_length=255)
    tipo_estudio = models.CharField(max_length=32, null=True, blank=False)
    cantidad = models.PositiveIntegerField()


# Create your models here.
class AbstractRecibo(AuditableMixin):
    razon_social = models.CharField(max_length=255)
    ci_rif = models.CharField(max_length=32)
    telefono = models.CharField(max_length=32, null=True, blank=True)
