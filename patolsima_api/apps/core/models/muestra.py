from django.db import models
from simple_history.models import HistoricalRecords
from patolsima_api.utils.models import AuditableMixin
from patolsima_api.apps.core.models.estudio import Estudio


class Muestra(AuditableMixin):
    class Estados(models.TextChoices):
        RECIBIDA = "RECIBIDA"
        DESCRIPCION_MACROSCOPICA = "DESCRIPCION_MACROSCOPICA"
        DESHIDRATACION = "DESHIDRATACION"
        INCLUSION_EN_PARAFINA = "INCLUSION_EN_PARAFINA"
        CORTE_MICROTOMO = "CORTE_MICROTOMO"
        COLORACION = "COLORACION"
        COLORACIONES_ESPECIALES = "COLORACIONES_ESPECIALES"
        DIAGNOSTICO_MICROSCOPICO = "DIAGNOSTICO_MICROSCOPICO"
        ALMACENAMIENTO = "ALMACENAMIENTO"
        DISPOSICION_DE_RESIDUOS = "DISPOSICION_DE_RESIDUOS"
        PERDIDA = "PERDIDA"

    estudio = models.ForeignKey(
        Estudio, on_delete=models.CASCADE, related_name="muestras"
    )
    tipo_de_muestra = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=512, null=True, blank=True)
    notas = models.TextField(null=True, blank=True)
    estado = models.CharField(
        max_length=32, choices=Estados.choices, default=Estados.RECIBIDA
    )

    history = HistoricalRecords()
