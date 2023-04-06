from django.db import models
from patolsima_api.apps.s3_management.models import S3File
from patolsima_api.utils.models import AuditableMixin
from simple_history.models import HistoricalRecords
from .muestra import Muestra


class FaseMuestra(AuditableMixin):
    muestra = models.ForeignKey(Muestra, on_delete=models.CASCADE, related_name="fases")
    estado = models.CharField(
        max_length=32, choices=Muestra.Estados.choices, default=Muestra.Estados.RECIBIDA
    )
    notas = models.TextField(max_length=4092)
    adjuntos = models.ManyToManyField(S3File)

    history = HistoricalRecords()

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if not created:
            return
        muestra = instance.muestra
        if muestra.estado != instance.estado:
            muestra.estado = instance.estado
            muestra.save()


models.signals.post_save.connect(FaseMuestra.post_create, FaseMuestra)
