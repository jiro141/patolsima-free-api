from django.db import models
from datetime import date
from simple_history.models import HistoricalRecords
from patolsima_api.utils.models import AuditableMixin, PersonalInfoMixin, CIMixin


class Paciente(AuditableMixin, PersonalInfoMixin, CIMixin):
    class Sexo(models.TextChoices):
        MASCULINO = "MASCULINO"
        FEMENINO = "FEMENINO"

    fecha_nacimiento = models.DateField(null=True)
    sexo = models.CharField(max_length=16, choices=Sexo.choices, null=True, blank=True)

    history = HistoricalRecords()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["ci"],
                condition=models.Q(deleted_at=None),
                name="unique_constraint_only_for_not_deleted_ci_paciente",
            )
        ]

    def __str__(self):
        return f"({self.id})({self.ci}) {self.nombres} {self.apellidos} "

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
