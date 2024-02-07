from django.db import models

# Create your models here.

class PuntoInteres(models.Model):
    nombre = models.CharField(max_length=200)
    modelo = models.CharField(max_length=200, null=True, blank=True)
    latitud = models.FloatField()
    longitud = models.FloatField()
    imagen = models.ImageField(upload_to='images', null=True, blank=True)

    def __str__(self):
        return self.nombre
