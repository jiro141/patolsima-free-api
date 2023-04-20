from django.db import models
from datetime import date
from simple_history.models import HistoricalRecords
from patolsima_api.utils.models import AuditableMixin, PersonalInfoMixin


class Paciente(AuditableMixin, PersonalInfoMixin):
    class Sexo(models.TextChoices):
        MASCULINO = "MASCULINO"
        FEMENINO = "FEMENINO"

    ci = models.PositiveIntegerField(null=True, unique=True, db_index=True)
    fecha_nacimiento = models.DateField(null=True)
    sexo = models.CharField(max_length=16, choices=Sexo.choices, null=True, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"({self.id})({self.ci}) {self.apellidos} {self.nombres}"

    @property
    def nombre_completo(self):
        return f"{self.apellidos} {self.nombres}"

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
