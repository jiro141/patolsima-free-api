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
    def with_prioridad(self):
        return self.annotate(
            prioridad=models.Case(
                models.When(urgente=True, then=models.Value(Estudio.Prioridad.ALTA)),
                models.When(
                    created_at__lt=(make_aware(datetime.now())) - timedelta(days=7),
                    then=models.Value(Estudio.Prioridad.MEDIA),
                ),
                default=models.Value(Estudio.Prioridad.BAJA),
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

    history = HistoricalRecords()
    objects = EstudiosManager()

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
        instance.codigo = f"{prefixes[instance.tipo]}:{count_estudios}-{year}"
        instance.save()


post_save.connect(Estudio.post_create, sender=Estudio)
