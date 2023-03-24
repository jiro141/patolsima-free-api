from django.contrib import admin

# Register your models here.
from patolsima_api.apps.core.models import Paciente


class PacienteAdmin(admin.ModelAdmin):
    pass


admin.site.register(Paciente, PacienteAdmin)
