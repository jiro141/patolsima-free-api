from django.db import models
from django.contrib.auth.models import User
from datetime import date
from simple_history.models import HistoricalRecords
from patolsima_api.utils.models import NombreMixin, AuditableMixin, NCOMEDMixin
from patolsima_api.apps.uploaded_file_management.models import UploadedFile


class Patologo(AuditableMixin, NombreMixin, NCOMEDMixin):
    firma = models.ForeignKey(UploadedFile, on_delete=models.DO_NOTHING, null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["ncomed"],
                condition=models.Q(deleted_at=None),
                name="patologo_ncomed_unique_when_not_deleted",
            ),
            models.UniqueConstraint(
                fields=["user"],
                condition=models.Q(deleted_at=None),
                name="patologo_user_unique_when_not_deleted",
            ),
        ]

    def __str__(self):
        return f"({self.id})({self.ncomed}) {self.apellidos} {self.nombres}"

    history = HistoricalRecords()
