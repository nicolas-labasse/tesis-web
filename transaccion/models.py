from django.db import models
from usuario.models import Usuario

# Create your models here.

class Transaccion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mp_id = models.CharField(max_length=100, blank=True, null=True)
    precio = models.FloatField(null=True, blank=True)
    fechaCreacion = models.DateField(auto_now_add=True)
    usuario_str = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.usuario.nombre





