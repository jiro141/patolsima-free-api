from django.db import models
from simple_history.models import HistoricalRecords
from patolsima_api.utils.models import AuditableMixin, TelefonoMixin, DireccionMixin


class Cliente(AuditableMixin, TelefonoMixin, DireccionMixin):
    razon_social = models.CharField(max_length=255)
    ci_rif = models.CharField(max_length=32, db_index=True)

    history = HistoricalRecords()
