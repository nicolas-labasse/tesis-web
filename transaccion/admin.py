from django.contrib import admin
from transaccion.models import Transaccion


@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'precio', 'fechaCreacion', 'mp_id', 'estado_pago')
    search_fields = ('usuario', 'precio')



