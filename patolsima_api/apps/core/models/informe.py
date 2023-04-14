from django.db import models
from patolsima_api.utils.models import AuditableMixin
from patolsima_api.apps.s3_management.models import S3File
from .estudio import Estudio


class Informe(AuditableMixin):
    estudio = models.OneToOneField(
        Estudio, on_delete=models.DO_NOTHING, primary_key=True
    )
    informes_generados = models.ManyToManyField(S3File, through="InformeGenerado")
    # Campos de texto enriquecido
    descripcion_macroscopica = models.TextField(max_length=10240, null=True, blank=True)
    descripcion_microscopica = models.TextField(max_length=10240, null=True, blank=True)
    diagnostico = models.TextField(max_length=10240, null=True, blank=True)
    notas = models.TextField(max_length=10240, null=True, blank=True)
    anexos = models.TextField(max_length=10240, null=True, blank=True)
    bibliografia = models.TextField(max_length=10240, null=True, blank=True)

    # Control de flujo de escritura
    completado = models.BooleanField(default=False)
    aprobado = models.BooleanField(default=False)


class InformeGenerado(AuditableMixin):
    s3_file = models.ForeignKey(S3File, on_delete=models.CASCADE)
    informe = models.ForeignKey("Informe", on_delete=models.CASCADE)


class ResultadoInmunostoquimica(AuditableMixin):
    informe = models.ForeignKey(
        Informe, on_delete=models.CASCADE, related_name="resultadod_inmunostoquimica"
    )
    procedimiento = models.CharField(max_length=256)
    reaccion = models.CharField(max_length=256)
    diagnostico_observaciones = models.TextField(max_length=1024, null=True, blank=True)
