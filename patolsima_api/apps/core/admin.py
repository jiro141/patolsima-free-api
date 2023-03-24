from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
from patolsima_api.apps.core.models import Paciente


class PacienteAdmin(SimpleHistoryAdmin):
    pass


admin.site.register(Paciente, PacienteAdmin)
