from django.db import models

# Create your models here.
    
class PuntosInteres(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)
    modelo = models.CharField(max_length=200, null=True, blank=True)
    latitud = models.CharField(max_length=100, null=True, blank=True)
    longitud = models.CharField(max_length=100, null=True, blank=True)
    imagen = models.ImageField(upload_to='puntos_interes', null=True, blank=True)


    def __str__(self):
        return self.nombre
    

class Recorridos(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)
    descripcion = models.TextField(max_length=1500, null=True, blank=True)
    duracion = models.CharField(max_length=100, null=True, blank=True)
    puntoInteres = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nombre
    
class Usuario(models.Model):
    email = models.EmailField(max_length=100)
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='usuarios', null=True, blank=True)
    recorridoFavorito = models.CharField(max_length=255, null=True, blank=True)
    ultimosRecorridos = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return self.nombre
    

class Comentario(models.Model):
    usuario = models.CharField(max_length=100, null=True, blank=True)
    recorrido = models.CharField(max_length=100, null=True, blank=True)
    comentario = models.TextField(max_length=255, null=True, blank=True)
    puntuacion = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.comentario
