from django.db import models
from pInteres.models import PuntoInteres

# Create your models here.

class Recorrido(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=1000)
    duracion = models.CharField(max_length=100, blank=True, null=True)
    puntoInteres = models.ManyToManyField(PuntoInteres)
    def __str__(self):
        return self.nombre