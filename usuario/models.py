from django.db import models
from recorrido.models import Recorrido
# Create your models here.

class Usuario(models.Model):
    email = models.CharField(max_length=200, unique=True)
    nombre = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='images', null=True, blank=True)
    recorridoFavorito = models.ForeignKey(Recorrido, on_delete=models.CASCADE, related_name='recorridoFavorito', null=True, blank=True)
    ultimosRecorridos = models.ForeignKey(Recorrido, related_name='ultimosRecorridos', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

