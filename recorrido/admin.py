from django.contrib import admin
from .models import Recorrido

# Register your models here.
@admin.register(Recorrido)
class RecorridoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'duracion')
    search_fields = ('nombre', 'descripcion')
