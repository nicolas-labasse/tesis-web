from django.db import models

# Create your models here.

class Calificacion(models.Model):
    usuario = models.ForeignKey('usuario.Usuario', on_delete=models.CASCADE)
    recorrido = models.ForeignKey('recorrido.Recorrido', on_delete=models.CASCADE)
    comentario = models.TextField( blank=True, null=True)
    puntuacion = models.IntegerField( blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.usuario.nombre + self.usuario.email
