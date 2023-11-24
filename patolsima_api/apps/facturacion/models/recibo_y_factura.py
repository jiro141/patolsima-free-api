from django.db import models
from decimal import Decimal
from simple_history.models import HistoricalRecords
from patolsima_api.utils.models import AuditableMixin
from patolsima_api.apps.uploaded_file_management.models import UploadedFile
from .orden import Orden
from .pago import Pago


class AbstractRecibo(AuditableMixin):
    orden = models.OneToOneField(Orden, on_delete=models.CASCADE)
    s3_file = models.OneToOneField(UploadedFile, on_delete=models.CASCADE, null=True)
    fecha_generacion = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        abstract = True

    @property
    def pdf_reder_context(self):
        return {}  


class Factura(AbstractRecibo):
    n_factura = models.PositiveIntegerField(unique=True, db_index=True)
    history = HistoricalRecords()
    monto = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00")
    )
    
 


class Recibo(AbstractRecibo):
    history = HistoricalRecords()

    @property
    def pdf_reder_context(self):
        return {"n_recibo": self.id}

class FacturaOffset(AuditableMixin):
    factura_offset = models.PositiveIntegerField()
    
    


class NotasCredito(AbstractRecibo):
    n_factura =models.PositiveIntegerField(default=0)
    n_notacredito = models.AutoField(primary_key=True)
    # pago = models.OneToOneField(Pago, on_delete=models.CASCADE, related_name="nota_de_credito")
    monto = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal(" 0.00")
    )

class NotasDebito(AbstractRecibo):
    n_notadebito = models.PositiveIntegerField(unique=True)
    n_factura =models.PositiveIntegerField(default=0)
    monto = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal(" 0.00")
    )

