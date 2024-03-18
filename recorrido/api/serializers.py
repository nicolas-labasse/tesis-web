from rest_framework.serializers import ModelSerializer
from recorrido.models import Recorrido
from pInteres.api.serializers import PuntoInteresSerializer

class RecorridoSerializer(ModelSerializer):
    puntoInteres = PuntoInteresSerializer(many=True, read_only=True)

    class Meta:
        model = Recorrido
        fields = ('id', 'nombre', 'descripcion', 'duracion', 'puntoInteres')
    
    