from django.db import models
from simple_history.models import HistoricalRecords
from patolsima_api.utils.models import (
    AuditableMixin,
    TelefonoMixin,
    DireccionMixin,
    EmailMixin,
)


class Cliente(AuditableMixin, TelefonoMixin, DireccionMixin, EmailMixin):
    razon_social = models.CharField(max_length=255)
    ci_rif = models.CharField(max_length=32, unique=True, db_index=True)

    history = HistoricalRecords()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["ci_rif"],
                condition=models.Q(deleted_at=None),
                name="unique_ci_rif_non_deleted_only",
            )
        ]
