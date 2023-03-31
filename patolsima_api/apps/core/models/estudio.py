from datetime import datetime, timedelta
from django.db import models
from django.utils.timezone import make_aware
from simple_history.models import HistoricalRecords
from patolsima_api.utils.models import AuditableMixin
from patolsima_api.apps.s3_management.models import S3File
from patolsima_api.apps.core.models.medico_tratante import MedicoTratante
from patolsima_api.apps.core.models.patologo import Patologo
from patolsima_api.apps.core.models.paciente import Paciente


class Estudio(AuditableMixin):
    class TipoEstudio(models.TextChoices):
        BIOPSIA = "BIOPSIA"
        CITOLOGIA = "CITOLOGIA"
        CITOLOGIA_ESPECIAL = "CITOLOGIA_ESPECIAL"
        INMUNOSTOQUIMICA = "INMUNOSTOQUIMICA"

    class Prioridad(models.TextChoices):
        ALTA = "ALTA"
        MEDIA = "MEDIA"
        BAJA = "BAJA"

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico_tratante = models.ForeignKey(MedicoTratante, on_delete=models.DO_NOTHING)
    patologo = models.ForeignKey(Patologo, on_delete=models.DO_NOTHING, null=True)
    adjuntos = models.ManyToManyField(S3File)
    codigo = models.CharField(max_length=32, unique=True, db_index=True)
    notas = models.TextField(null=True, blank=True)
    urgente = models.BooleanField(default=False)
    envio_digital = models.BooleanField(default=True)
    tipo = models.CharField(
        max_length=18,
        choices=TipoEstudio.choices,
        default=TipoEstudio.CITOLOGIA,
    )

    @property
    def prioridad_calculada(self):
        if self.urgente:
            return self.Prioridad.ALTA

        return (
            self.Prioridad.BAJA
            if (make_aware(datetime.now()) - self.created_at).days < 7
            else self.Prioridad.MEDIA
        )

    @classmethod
    def add_priority_to_list_queryset(
        cls, queryset: models.QuerySet
    ) -> models.QuerySet:
        return queryset.annotate(
            prioridad=models.Case(
                models.When(urgente=True, then=models.Value(Estudio.Prioridad.ALTA)),
                models.When(
                    created_at__lt=(make_aware(datetime.now())) - timedelta(days=7),
                    then=models.Value(Estudio.Prioridad.MEDIA),
                ),
                default=models.Value(Estudio.Prioridad.BAJA),
            )
        )

    history = HistoricalRecords()
