from django.db import models, transaction
from django.db.models import F, Sum, Value
from django.db.models.functions import Coalesce
from django.db.models.signals import pre_save
from decimal import Decimal
from simple_history.models import HistoricalRecords
from softdelete.models import SoftDeleteManager
from patolsima_api.utils.models import AuditableMixin, ArchivableMixing
from patolsima_api.utils.quantize import round_2_decimals
from .cliente import Cliente
from .recibo_y_factura import Factura



class Transaccion( AuditableMixin, ArchivableMixing):
    rifci = models.CharField(max_length=50)
    cliente = models.CharField(max_length=50)
    tipo = models.CharField(max_length=32)
    n_control = models.PositiveIntegerField(unique=True, db_index=True)
    monto = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00")
    )
    monto_impuesto = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00"))
    fecha_emision = models.DateField(auto_now_add=True)