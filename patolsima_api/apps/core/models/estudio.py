from datetime import datetime, timedelta
from django.db import models, transaction
from django.db.models.signals import post_save
from django.utils.timezone import make_aware
from simple_history.models import HistoricalRecords
from softdelete.models import SoftDeleteManager
from patolsima_api.utils.models import AuditableMixin, ArchivableMixing
from patolsima_api.apps.uploaded_file_management.models import UploadedFile
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
            .annotate(
                informe_existe=models.Case(
                    models.When(informe__isnull=False, then=models.Value(True)),
                    default=models.Value(False),
                )
            )
            .annotate(
                informe_aprobado=models.Case(
                    models.When(informe__aprobado=True, then=models.Value(True)),
                    default=models.Value(False),
                )
            )
            .annotate(
                informe_completado=models.Case(
                    models.When(informe__completado=True, then=models.Value(True)),
                    default=models.Value(False),
                )
            )
        )


class Estudio(AuditableMixin, ArchivableMixing):
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
    medico_tratante = models.ForeignKey(
        MedicoTratante, on_delete=models.DO_NOTHING, null=True
    )
    patologo = models.ForeignKey(Patologo, on_delete=models.DO_NOTHING, null=True)
    adjuntos = models.ManyToManyField(UploadedFile)
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
        start_of_this_year = make_aware(datetime(year, 1, 1))
        offset_record = (
            EstudioCodigoOffset.objects.filter(
                created_at__gte=start_of_this_year, tipo_estudio=instance.tipo
            )
            .order_by("-created_at")
            .first()
        )

        filter_ = {
            "tipo": instance.tipo,
            "created_at__gte": start_of_this_year
            if not offset_record
            else offset_record.created_at,
        }

        count_estudios = (
            cls.objects.filter(**filter_) | cls.objects.deleted_set().filter(**filter_)
        ).count()

        if offset_record:
            count_estudios += offset_record.offset

        instance.codigo = (
            f"{prefixes[instance.tipo]}:{str(count_estudios).zfill(3)}-{year}"
        )
        instance.save()

    @transaction.atomic
    def archive(self, save_=True):
        if hasattr(self, "informe"):
            self.informe.archive(save_=save_)

        for muestra in self.muestras.all():
            muestra.archive(save_=save_)
        super().archive(save_=save_)


class EstudioCodigoOffset(AuditableMixin):
    tipo_estudio = models.CharField(
        max_length=32,
        choices=Estudio.TipoEstudio.choices,
        default=Estudio.TipoEstudio.BIOPSIA,
    )
    offset = models.PositiveIntegerField()


post_save.connect(Estudio.post_create, sender=Estudio)
