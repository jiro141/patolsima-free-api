from django.db import models


class NombreMixin(models.Model):
    nombres = models.CharField(max_length=255, db_index=True)
    apellidos = models.CharField(max_length=255, db_index=True)

    class Meta:
        abstract = True


class PersonalInfoMixin(NombreMixin):
    direccion = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    telefono_fijo = models.CharField(max_length=255, null=True, blank=True)
    telefono_celular = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True
