from rest_framework.serializers import ModelSerializer
from calificacion.models import Calificacion



class CalificacionSerializer(ModelSerializer):
    class Meta:
        model = Calificacion
        fields = ['id', 'usuario', 'recorrido', 'comentario', 'puntuacion', 'fecha_creacion']

    