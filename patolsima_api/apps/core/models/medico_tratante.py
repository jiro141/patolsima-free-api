from django.db import models
from datetime import date
from simple_history.models import HistoricalRecords
from patolsima_api.utils.models import (
    AuditableMixin,
    PersonalInfoMixin,
    NCOMEDMixin,
    CIMixin,
)


class MedicoTratante(AuditableMixin, PersonalInfoMixin, NCOMEDMixin, CIMixin):
    especialidad = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["ncomed"],
                condition=models.Q(deleted_at=None),
                name="ncomed_unique_when_not_deleted",
            ),
            models.UniqueConstraint(
                fields=["ci"],
                condition=models.Q(deleted_at=None),
                name="unique_constraint_only_for_not_deleted_ci_medico_tratante",
            ),
        ]

    def __str__(self):
        return f"({self.id})({self.ncomed}) {self.apellidos} {self.nombres} [{self.especialidad}]"

    history = HistoricalRecords()
