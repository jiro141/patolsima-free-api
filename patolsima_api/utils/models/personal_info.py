from django.db import models


class NombreMixin(models.Model):
    nombres = models.CharField(max_length=255, db_index=True)
    apellidos = models.CharField(max_length=255, db_index=True)

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

    @property
    def nombre_completo_nombre_primero(self):
        return f"{self.nombres} {self.apellidos}"

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
    You must ensure unicity of NCOMED field in the concrete model only if it is an Auditable model.
    """

    ncomed = models.CharField(max_length=32, db_index=True, null=True, blank=True)

    class Meta:
        abstract = True


class PersonalInfoMixin(NombreMixin, TelefonoMixin, DireccionMixin, EmailMixin):
    class Meta:
        abstract = True


class CIMixin(models.Model):
    """
    You must ensure unicity of CI field in the concrete model only if it is an Auditable model.
    """

    ci = models.CharField(null=True, blank=True, max_length=16, db_index=True)

    class Meta:
        abstract = True
