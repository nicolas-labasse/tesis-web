from django.contrib import admin
from .models import PuntoInteres


# Register your models here.
@admin.register(PuntoInteres)
class PuntoIteresAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'latitud', 'longitud', 'imagen')
    search_fields = ('nombre', 'latitud', 'longitud')