from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
from patolsima_api.apps.core.models import (
    Paciente,
    MedicoTratante,
    Patologo,
    Estudio,
    EstudioCodigoOffset,
    Muestra,
    FaseMuestra,
    Informe,
    ResultadoInmunostoquimica,
)
from patolsima_api.utils.admin import date_to_admin_readable


class PacienteAdmin(SimpleHistoryAdmin):
    list_display = ("id", "ci", "nombres", "apellidos", "email", "telefono_celular")
    search_fields = ("ci", "apellidos", "email")


class MedicoTratanteAdmin(SimpleHistoryAdmin):
    list_display = (
        "id",
        "ci",
        "ncomed",
        "nombres",
        "apellidos",
        "email",
        "especialidad",
        "telefono_celular",
    )
    search_fields = ("ci", "ncomed", "apellidos", "email", "especialidad")


class PatologoAdmin(SimpleHistoryAdmin):
    list_display = (
        "id",
        "ncomed",
        "nombres",
        "apellidos",
    )
    search_fields = ("ci", "ncomed", "apellidos", "email", "especialidad")


class MuestraInline(admin.TabularInline):
    model = Muestra


class MuestraAdmin(SimpleHistoryAdmin):
    list_select_related = ("estudio",)
    list_display = (
        "id",
        "codigo_estudio",
        "tipo_de_muestra",
        "estado",
        "created_at_formatted",
        "updated_at_formatted",
    )
    search_fields = ("estudio__codigo", "tipo_de_muestra")
    list_filter = ("estado", "created_at", "updated_at")

    @admin.display(ordering="estudio__codigo", description="Estudio")
    def codigo_estudio(self, obj: Muestra):
        return obj.estudio.codigo

    @admin.display(ordering="created_at", description="Creado el")
    def created_at_formatted(self, obj: Estudio):
        return date_to_admin_readable(obj.created_at)

    @admin.display(ordering="updated_at", description="Actualizado el")
    def updated_at_formatted(self, obj: Estudio):
        return date_to_admin_readable(obj.updated_at)


class EstudioAdmin(SimpleHistoryAdmin):
    inlines = [
        MuestraInline,
    ]
    list_select_related = ["paciente", "patologo", "medico_tratante", "informe"]
    list_display = (
        "id",
        "codigo",
        "tipo",
        "prioridad",
        "paciente_ci",
        "paciente_full_name",
        "patologo_full_name",
        "medico_tratante_ncomed",
        "urgente",
        "envio_digital",
        "tiene_informe",
        "created_at_formatted",
        "updated_at_formatted",
    )
    search_fields = (
        "paciente__ci",
        "paciente__nombres",
        "paciente__apellidos",
        "codigo",
    )
    list_filter = ("tipo", "urgente", "envio_digital", "created_at", "updated_at")

    @admin.display(ordering="paciente__ci", description="C.I.")
    def paciente_ci(self, obj: Estudio):
        return obj.paciente.ci

    @admin.display(ordering="prioridad", description="Prioridad")
    def prioridad(self, obj: Estudio):
        return obj.prioridad_procedural

    @admin.display(ordering="paciente__apellidos", description="Nombre Completo")
    def paciente_full_name(self, obj: Estudio):
        return f"{obj.paciente.apellidos} {obj.paciente.nombres}"

    @admin.display(ordering="patologo__apellidos", description="Patologo")
    def patologo_full_name(self, obj: Estudio):
        return f"{obj.patologo.apellidos} {obj.patologo.nombres}"

    @admin.display(ordering="medico_tratante__ncomed", description="NCOMED Medico")
    def medico_tratante_ncomed(self, obj: Estudio):
        return obj.paciente.ci

    @admin.display(ordering="created_at", description="Creado el")
    def created_at_formatted(self, obj: Estudio):
        return date_to_admin_readable(obj.created_at)

    @admin.display(ordering="updated_at", description="Actualizado el")
    def updated_at_formatted(self, obj: Estudio):
        return date_to_admin_readable(obj.updated_at)

    @admin.display
    def tiene_informe(self, obj: Estudio):
        return bool(obj.informe)


class EstudioCodigoOffsetAdmin(SimpleHistoryAdmin):
    list_display = (
        "id",
        "tipo_estudio",
        "offset",
        "created_at_formatted",
        "updated_at_formatted",
    )

    @admin.display(ordering="created_at", description="Creado el")
    def created_at_formatted(self, obj: Estudio):
        return date_to_admin_readable(obj.created_at)

    @admin.display(ordering="updated_at", description="Actualizado el")
    def updated_at_formatted(self, obj: Estudio):
        return date_to_admin_readable(obj.updated_at)


class FaseMuestraAdmin(SimpleHistoryAdmin):
    list_display = ("id", "muestra_id", "estado", "created_at", "updated_at")


class ResultadoInmunostoquimicaInline(admin.TabularInline):
    model = ResultadoInmunostoquimica


class InformeAdmin(SimpleHistoryAdmin):
    list_select_related = ("estudio",)
    list_display = (
        "codigo_estudio",
        "completado",
        "aprobado",
        "created_at_formatted",
        "updated_at_formatted",
    )
    search_fields = ("estudio__codigo",)
    list_filter = ("completado", "aprobado", "created_at", "updated_at")
    inlines = [
        ResultadoInmunostoquimicaInline,
    ]

    @admin.display(ordering="estudio__codigo", description="Estudio")
    def codigo_estudio(self, obj: Muestra):
        return obj.estudio.codigo

    @admin.display(ordering="created_at", description="Creado el")
    def created_at_formatted(self, obj: Estudio):
        return date_to_admin_readable(obj.created_at)

    @admin.display(ordering="updated_at", description="Actualizado el")
    def updated_at_formatted(self, obj: Estudio):
        return date_to_admin_readable(obj.updated_at)


admin.site.register(Paciente, PacienteAdmin)
admin.site.register(MedicoTratante, MedicoTratanteAdmin)
admin.site.register(Patologo, PatologoAdmin)
admin.site.register(Estudio, EstudioAdmin)
admin.site.register(EstudioCodigoOffset, EstudioCodigoOffsetAdmin)
admin.site.register(Muestra, MuestraAdmin)
admin.site.register(FaseMuestra, FaseMuestraAdmin)
admin.site.register(Informe, InformeAdmin)
