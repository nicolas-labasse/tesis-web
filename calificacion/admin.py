from django.contrib import admin
from calificacion.models import Calificacion

# Register your models here.

@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'recorrido', 'comentario', 'puntuacion', 'fecha_creacion')
    search_fields = ('usuario', 'recorrido', 'comentario', 'puntuacion')
