from rest_framework.serializers import ModelSerializer
from calificacion.api import serializers
from pInteres.models import PuntoInteres

class PuntoInteresSerializer(ModelSerializer):
    class Meta:
        model = PuntoInteres
        fields = '__all__'


