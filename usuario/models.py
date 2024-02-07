from django.db import models
from recorrido.models import Recorrido
# Create your models here.

class Usuario(models.Model):
    email = models.CharField(max_length=200, unique=True)
    nombre = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='images', null=True, blank=True)
    recorridoFavorito = models.OneToOneField(Recorrido, on_delete=models.CASCADE, null=True, blank=True)
    ultimosRecorridos = models.ManyToManyField(Recorrido, related_name='ultimosRecorridos', blank=True)

    def __str__(self):
        return self.nombre

