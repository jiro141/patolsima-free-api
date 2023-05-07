from django.db import models
from datetime import date
from simple_history.models import HistoricalRecords
from patolsima_api.utils.models import NombreMixin, AuditableMixin, NCOMEDMixin
from patolsima_api.apps.uploaded_file_management.models import UploadedFile


class Patologo(AuditableMixin, NombreMixin, NCOMEDMixin):
    firma = models.ForeignKey(UploadedFile, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f"({self.id})({self.ncomed}) {self.apellidos} {self.nombres}"

    history = HistoricalRecords()
