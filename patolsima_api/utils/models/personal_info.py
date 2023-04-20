from django.db import models


class NombreMixin(models.Model):
    nombres = models.CharField(max_length=255, db_index=True)
    apellidos = models.CharField(max_length=255, db_index=True)

    class Meta:
        abstract = True


class EmailMixin(models.Model):
    email = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True


class DireccionMixin(models.Model):
    direccion = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True


class TelefonoMixin(models.Model):
    telefono_fijo = models.CharField(max_length=255, null=True, blank=True)
    telefono_celular = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True


class NCOMEDMixin(models.Model):
    """
    Holds the NCOMED (numero/codigo del colegio de medicos de Venezuela
    """

    ncomed = models.CharField(
        max_length=32, unique=True, db_index=True, null=True, blank=True
    )

    class Meta:
        abstract = True


class PersonalInfoMixin(NombreMixin, TelefonoMixin, DireccionMixin, EmailMixin):
    class Meta:
        abstract = True
