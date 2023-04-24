from django.db import models
from decimal import Decimal
from simple_history.models import HistoricalRecords
from patolsima_api.utils.models import AuditableMixin


class CambioUSDBS(AuditableMixin):
    bs_e = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
