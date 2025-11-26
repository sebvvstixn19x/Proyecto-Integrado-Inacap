from django.contrib import admin
from .models import Reporte, AccionModeracion


@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ("usuario", "motivo", "fecha", "revisado")
    list_filter = ("motivo", "revisado")
    search_fields = ("usuario__username",)


@admin.register(AccionModeracion)
class AccionModeracionAdmin(admin.ModelAdmin):
    list_display = ("reporte", "administrador", "accion", "fecha")
    list_filter = ("accion",)
