from datetime import datetime, timedelta
from django.db import models
from django.db.models import functions as model_functions
from django.utils.timezone import make_aware
from simple_history.models import HistoricalRecords
from patolsima_api.utils.models import AuditableMixin
from patolsima_api.apps.s3_management.models import S3File
from .estudio import Estudio


class InformesManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(estudio_tipo=models.F("estudio__tipo"))
            .annotate(estudio_codigo=models.F("estudio__codigo"))
            .annotate(estudio_paciente_id=models.F("estudio__id"))
            .annotate(estudio_paciente_ci=models.F("estudio__paciente__ci"))
            .annotate(estudio_patologo_id=models.F("estudio__patologo_id"))
            .annotate(
                estudio_patologo_name=model_functions.Concat(
                    models.F("estudio__patologo__nombres"),
                    models.Value(" "),
                    models.F("estudio__patologo__apellidos"),
                    output_field=models.CharField(),
                )
            )
            .annotate(
                estudio_prioridad=models.Case(
                    models.When(
                        estudio__urgente=True, then=models.Value(Estudio.Prioridad.ALTA)
                    ),
                    models.When(
                        estudio__created_at__lt=(make_aware(datetime.now()))
                        - timedelta(days=7),
                        then=models.Value(Estudio.Prioridad.MEDIA),
                    ),
                    default=models.Value(Estudio.Prioridad.BAJA),
                )
            )
        )


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

    history = HistoricalRecords()
    objects = InformesManager()


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

    history = HistoricalRecords()
