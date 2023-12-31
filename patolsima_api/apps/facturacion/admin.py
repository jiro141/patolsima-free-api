from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
from patolsima_api.apps.facturacion.models import (
    Cliente,
    Orden,
    ItemOrden,
    Recibo,
    Factura,
    Pago,
    NotaPago,
    CambioUSDBS,
)

from patolsima_api.apps.facturacion.models.recibo_y_factura import NotaCreditoOffset, NotaDebitoOffset, NotasCredito, NotasDebito

from patolsima_api.apps.facturacion.models.recibo_y_factura import FacturaOffset
from patolsima_api.utils.admin import date_to_admin_readable
from patolsima_api.utils.models.admin import AuditableAdmin

# Register your models here.


class ClienteAdmin(AuditableAdmin, SimpleHistoryAdmin):
    list_display = (
        "id",
        "ci_rif",
        "razon_social",
        "created_at_formatted",
        "updated_at_formatted",
    )
    list_filter = ("created_at", "updated_at")
    search_fields = ("ci_rif", "razon_social")


class ItemOrdenAdminInline(admin.StackedInline):
    model = ItemOrden
    readonly_fields = ("estudio",)

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj):
        return False


class PagoAdminInline(admin.TabularInline):
    model = Pago
    readonly_fields = (
        "pendiente_por_pagar_usd",
        "total_usd",
        "monto_bs",
        "pendiente_por_pagar_bs",
        "total_bs",
    )

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj):
        return False


class FacturaAdminInline(admin.StackedInline):
    model = Factura
    readonly_fields = ("s3_file", "fecha_generacion", "n_factura")



class ReciboAdminInline(admin.StackedInline):
    model = Recibo
    readonly_fields = (
        "s3_file",
        "fecha_generacion",
    )


class OrdenAdmin(AuditableAdmin, SimpleHistoryAdmin):
    list_select_related = ("cliente",)
    list_display = (
        "id",
        "rif_cliente",
        "nombre_cliente",
        "confirmada",
        "pagada",
        "created_at_formatted",
        "updated_at_formatted",
    )
    list_filter = ("confirmada", "pagada", "created_at", "updated_at")
    search_fields = ("id", "cliente__ci_rif", "cliente__razon_social")
    inlines = [
        ItemOrdenAdminInline,
        PagoAdminInline,
        ReciboAdminInline,
        FacturaAdminInline,
    ]
    readonly_fields = ("pagada", "confirmada")

    @admin.display(ordering="cliente__ci_rif", description="CI/RIF")
    def rif_cliente(self, obj: Orden):
        return obj.cliente.ci_rif

    @admin.display(ordering="cliente__razon_social", description="Nombre Cliente")
    def nombre_cliente(self, obj: Orden):
        return obj.cliente.razon_social


class FacturaAdmin(AuditableAdmin, SimpleHistoryAdmin):
    list_display = (
        "id",
        "orden_id",
        "n_factura",
        "created_at_formatted",
        "updated_at_formatted",
        "fecha_generacion_formatted",
    )
    list_filter = ("created_at", "updated_at", "fecha_generacion")
    search_fields = ("n_factura", "orden_id")

    @admin.display(ordering="updated_at", description="Generada el")
    def fecha_generacion_formatted(self, obj: Factura):
        return date_to_admin_readable(obj.fecha_generacion)


class ReciboAdmin(AuditableAdmin, SimpleHistoryAdmin):
    list_display = (
        "id",
        "orden_id",
        "created_at_formatted",
        "updated_at_formatted",
        "fecha_generacion_formatted",
    )
    list_filter = ("created_at", "updated_at", "fecha_generacion")
    search_fields = ("id", "orden_id")

    @admin.display(ordering="updated_at", description="Generado el")
    def fecha_generacion_formatted(self, obj: Recibo):
        return date_to_admin_readable(obj.fecha_generacion)


class CambioUSDAdmin(AuditableAdmin, SimpleHistoryAdmin):
    list_display = (
        "id",
        "bs_e",
        "created_at_formatted",
        "updated_at_formatted",
    )
    
class FacturaoffsetAdmin(SimpleHistoryAdmin):
    list_display = (
        "id",
        "factura_offset",
        "created_at_formatted",
    )
    
    @admin.display(ordering="created_at", description="Creado el")
    def created_at_formatted(self,obj:FacturaOffset):
        return date_to_admin_readable(obj.created_at)
    
class NotasCreditoAdmin(SimpleHistoryAdmin):
    list_display = (
        "n_notacredito",
        "n_factura",
        "fecha_generacion",
    )
    
    
class NotasDebitoAdmin(SimpleHistoryAdmin):
    list_display = (

        "n_notadebito",
        "n_factura",
        "fecha_generacion",
    )

class NotaCreditoffsetAdmin(SimpleHistoryAdmin):
    list_display = (
        "id",
        "notacredito_offset",
        "created_at_formatted",
    )   
    @admin.display(ordering="created_at", description="Creado el")
    def created_at_formatted(self,obj:NotaCreditoOffset):
        return date_to_admin_readable(obj.created_at)
class NotaDebitoffsetAdmin(SimpleHistoryAdmin):
    list_display = (
        "id",
        "notadebito_offset",
        "created_at_formatted",
    )   
    @admin.display(ordering="created_at", description="Creado el")
    def created_at_formatted(self,obj:NotaDebitoOffset):
        return date_to_admin_readable(obj.created_at)


admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Orden, OrdenAdmin)
admin.site.register(Factura, FacturaAdmin)
admin.site.register(Recibo, ReciboAdmin)
admin.site.register(CambioUSDBS, CambioUSDAdmin)
admin.site.register(FacturaOffset, FacturaoffsetAdmin)
admin.site.register(NotaCreditoOffset, NotaCreditoffsetAdmin)
admin.site.register(NotaDebitoOffset, NotaDebitoffsetAdmin)
admin.site.register(NotasCredito,NotasCreditoAdmin)
admin.site.register(NotasDebito,NotasDebitoAdmin)
 