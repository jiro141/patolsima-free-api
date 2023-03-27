from django.db import models
from simple_history.models import HistoricalRecords
from patolsima_api.utils.models import AuditableMixin
from patolsima_api.apps.s3_management.models import S3File
from patolsima_api.apps.core.models.medico_tratante import MedicoTratante
from patolsima_api.apps.core.models.patologo import Patologo
from patolsima_api.apps.core.models.paciente import Paciente


class Estudio(AuditableMixin):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico_tratante = models.ForeignKey(MedicoTratante, on_delete=models.DO_NOTHING)
    patologo = models.ForeignKey(Patologo, on_delete=models.DO_NOTHING, null=True)
    adjuntos = models.ManyToManyField(S3File)
    codigo = models.CharField(max_length=32, unique=True, db_index=True)
    notas = models.TextField(null=True, blank=True)

    history = HistoricalRecords()
