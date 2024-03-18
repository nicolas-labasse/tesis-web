from django.db import models
from usuario.models import Usuario

# Create your models here.

class Transaccion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    precio = models.FloatField()
    fechaCreacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.usuario.nombre + self.usuario.email


