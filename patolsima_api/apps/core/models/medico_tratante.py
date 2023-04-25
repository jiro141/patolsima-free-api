from django.db import models
from datetime import date
from simple_history.models import HistoricalRecords
from patolsima_api.utils.models import AuditableMixin, PersonalInfoMixin, NCOMEDMixin


class MedicoTratante(AuditableMixin, PersonalInfoMixin, NCOMEDMixin):
    ci = models.IntegerField(unique=True, null=True)
    especialidad = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return f"({self.id})({self.ncomed}) {self.apellidos} {self.nombres} [{self.especialidad}]"

    history = HistoricalRecords()
