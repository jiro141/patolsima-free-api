import enum
from enum import Enum
from django.db import models
from simple_history.models import HistoricalRecords
from patolsima_api.utils.models import AuditableMixin
from patolsima_api.apps.s3_management.models import S3File
from patolsima_api.apps.core.models.medico_tratante import MedicoTratante
from patolsima_api.apps.core.models.patologo import Patologo
from patolsima_api.apps.core.models.paciente import Paciente


class PrioridadEstudioEnum(enum.Enum):
    ALTA = "ALTA"
    MEDIA = "MEDIA"
    BAJA = "BAJA"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class TipoEstudioEnum(enum.Enum):
    BIOPSIA = "BIOPSIA"
    CITOLOGIA = "CITOLOGIA"
    CITOLOGIA_ESPECIAL = "CITOLOGIA_ESPECIAL"
    INMUNOSTOQUIMICA = "INMUNOSTOQUIMICA"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class Estudio(AuditableMixin):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico_tratante = models.ForeignKey(MedicoTratante, on_delete=models.DO_NOTHING)
    patologo = models.ForeignKey(Patologo, on_delete=models.DO_NOTHING, null=True)
    adjuntos = models.ManyToManyField(S3File)
    codigo = models.CharField(max_length=32, unique=True, db_index=True)
    notas = models.TextField(null=True, blank=True)
    prioridad = models.CharField(
        max_length=5,
        choices=PrioridadEstudioEnum.choices(),
        default=PrioridadEstudioEnum.BAJA,
    )
    tipo = models.CharField(
        max_length=18,
        choices=TipoEstudioEnum.choices(),
    )

    history = HistoricalRecords()
