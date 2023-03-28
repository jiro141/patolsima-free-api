from django.db import models
from datetime import date
from simple_history.models import HistoricalRecords
from patolsima_api.utils.models import AuditableMixin, PersonalInfoMixin


class Paciente(AuditableMixin, PersonalInfoMixin):
    ci = models.PositiveIntegerField(primary_key=True)
    fecha_nacimiento = models.DateField(null=True)

    history = HistoricalRecords()

    @property
    def edad(self):
        today = date.today()
        return (
            today.year
            - self.fecha_nacimiento.year
            - (
                (today.month, today.day)
                < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
            )
        )
