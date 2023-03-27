from django.db import models
from simple_history.models import HistoricalRecords
from patolsima_api.utils.models import AuditableMixin
from patolsima_api.apps.core.models.estudio import Estudio


class Muestra(AuditableMixin):
    estudio = models.ForeignKey(Estudio, on_delete=models.CASCADE)
    tipo_de_muestra = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=512, null=True, blank=True)
    notas = models.TextField(null=True, blank=True)

    history = HistoricalRecords()
