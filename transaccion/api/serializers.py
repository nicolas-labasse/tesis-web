from rest_framework.serializers import ModelSerializer
from transaccion.models import  Transaccion



class TransaccionSerializer(ModelSerializer):
    class Meta:
            model = Transaccion
            fields = ['id', 'usuario', 'mp_id', 'precio', 'fechaCreacion']



