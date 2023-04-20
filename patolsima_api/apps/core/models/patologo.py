from django.db import models
from datetime import date
from simple_history.models import HistoricalRecords
from patolsima_api.utils.models import NombreMixin, AuditableMixin, NCOMEDMixin
from patolsima_api.apps.s3_management.models import S3File


class Patologo(AuditableMixin, NombreMixin, NCOMEDMixin):
    firma = models.ForeignKey(S3File, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f"({self.id})({self.ncomed}) {self.apellidos} {self.nombres}"

    history = HistoricalRecords()
