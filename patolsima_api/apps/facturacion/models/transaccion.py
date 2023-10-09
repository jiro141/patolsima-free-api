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
    Cliente = models.ForeignKey(Cliente, on_delete= models.CASCADE)
    class TipoTransaccion(models.TextChoices):
        FACTURA = "FACTURA"
        NOTADEBITO = "NOTA DEBITO"
        NOTACREDITO = "NOTA CREDITO"
        
    tipo = models.CharField(
        max_length=32,
        choices=TipoTransaccion.choices,
        default=TipoTransaccion.FACTURA,
    )
    