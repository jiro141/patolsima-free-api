from datetime import datetime, timedelta
from django.db import models
from django.db.models.signals import post_save
from django.utils.timezone import make_aware
from simple_history.models import HistoricalRecords
from softdelete.models import SoftDeleteManager
from patolsima_api.utils.models import AuditableMixin
from patolsima_api.apps.s3_management.models import S3File
from patolsima_api.apps.core.models.medico_tratante import MedicoTratante
from patolsima_api.apps.core.models.patologo import Patologo
from patolsima_api.apps.core.models.paciente import Paciente


class EstudiosManager(SoftDeleteManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                prioridad=models.Case(
                    models.When(
                        urgente=True, then=models.Value(Estudio.Prioridad.ALTA)
                    ),
                    models.When(
                        created_at__lt=(make_aware(datetime.now())) - timedelta(days=7),
                        then=models.Value(Estudio.Prioridad.MEDIA),
                    ),
                    default=models.Value(Estudio.Prioridad.BAJA),
                )
            )
        )


class Estudio(AuditableMixin):
    class TipoEstudio(models.TextChoices):
        BIOPSIA = "BIOPSIA"
        CITOLOGIA_GINECOLOGICA = "CITOLOGIA_GINECOLOGICA"
        CITOLOGIA_ESPECIAL = "CITOLOGIA_ESPECIAL"
        INMUNOSTOQUIMICA = "INMUNOSTOQUIMICA"

    class Prioridad(models.TextChoices):
        ALTA = "ALTA"
        MEDIA = "MEDIA"
        BAJA = "BAJA"

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico_tratante = models.ForeignKey(MedicoTratante, on_delete=models.DO_NOTHING)
    patologo = models.ForeignKey(Patologo, on_delete=models.DO_NOTHING, null=True)
    adjuntos = models.ManyToManyField(S3File)
    codigo = models.CharField(max_length=32, unique=True, db_index=True)
    notas = models.TextField(null=True, blank=True)
    urgente = models.BooleanField(default=False)
    envio_digital = models.BooleanField(default=True)
    tipo = models.CharField(
        max_length=32,
        choices=TipoEstudio.choices,
        default=TipoEstudio.BIOPSIA,
    )
    estudio_asociado = models.CharField(max_length=32, null=True, blank=True)
    confirmado = models.BooleanField(default=False)

    history = HistoricalRecords()
    objects = EstudiosManager()

    def __str__(self):
        return f"({self.id}) {self.tipo} [{self.codigo}]"

    @property
    def prioridad_procedural(self):
        # Used by other related models like Informe to add Estudio priority to the Serializer outputs
        if self.urgente:
            return self.Prioridad.ALTA
        elif self.created_at < (make_aware(datetime.now()) - timedelta(days=7)):
            return self.Prioridad.MEDIA

        return self.Prioridad.BAJA

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if not created:
            return

        prefixes = {
            cls.TipoEstudio.BIOPSIA: "B",
            cls.TipoEstudio.CITOLOGIA_GINECOLOGICA: "CG",
            cls.TipoEstudio.CITOLOGIA_ESPECIAL: "CE",
            cls.TipoEstudio.INMUNOSTOQUIMICA: "IHQ",
        }
        year = datetime.now().year
        filter_ = {
            "tipo": instance.tipo,
            "created_at__gte": make_aware(datetime(year, 1, 1)),
        }
        count_estudios = (
            cls.objects.filter(**filter_) | cls.objects.deleted_set().filter(**filter_)
        ).count()
        instance.codigo = (
            f"{prefixes[instance.tipo]}:{str(count_estudios).zfill(3)}-{year}"
        )
        instance.save()


post_save.connect(Estudio.post_create, sender=Estudio)
