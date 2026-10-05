from django.contrib import admin

from .models import ViajeSonado


@admin.register(ViajeSonado)
class ViajeSonadoAdmin(admin.ModelAdmin):
    list_display = ["destino", "pais", "presupuesto", "fecha_tentativa", "visitado", "usuario"]
    list_filter = ["visitado", "pais"]
    search_fields = ["destino", "pais"]