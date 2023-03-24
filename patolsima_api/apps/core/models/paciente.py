from django.db import models
from datetime import date
from simple_history.models import HistoricalRecords


class Paciente(models.Model):
    ci = models.IntegerField(primary_key=True)
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField(null=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    telefono_fijo = models.CharField(max_length=255, null=True, blank=True)
    telefono_celular = models.CharField(max_length=255, null=True, blank=True)
    history = HistoricalRecords()

    @property
    def age(self):
        today = date.today()
        return (
            today.year
            - self.fecha_nacimiento.year
            - (
                (today.month, today.day)
                < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
            )
        )
