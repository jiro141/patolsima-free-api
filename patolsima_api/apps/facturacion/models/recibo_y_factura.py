from django.db import models
from decimal import Decimal
from simple_history.models import HistoricalRecords
from patolsima_api.utils.models import AuditableMixin
from patolsima_api.apps.uploaded_file_management.models import UploadedFile
from .orden import Orden


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

    @property
    def pdf_reder_context(self):
        if self.n_factura is None:
            try:
                last_instance = Factura.objects.latest('n_factura')
            except Factura.DoesNotExist:
                last_instance = None
            if last_instance is not None:
                self.n_factura = last_instance + 1
            else:
                self.n_factura = FacturaOffset.objects.filter("-created_at").last() + 1
        return {"n_factura": self.n_factura}
    
 


class Recibo(AbstractRecibo):
    history = HistoricalRecords()

    @property
    def pdf_reder_context(self):
        return {"n_recibo": self.id}

class FacturaOffset(AuditableMixin):
    factura_offset = models.PositiveIntegerField()
    
    
class NotaCredito(AbstractRecibo):
    factura = models.OneToOneField(Factura, on_delete=models.CASCADE)


