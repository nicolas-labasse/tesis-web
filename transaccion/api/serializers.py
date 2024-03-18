from rest_framework.serializers import ModelSerializer
from transaccion.models import  Transaccion




class TransaccionSerializer(ModelSerializer):
    class Meta:
            model = Transaccion
            fields = '__all__'

class TransaccionSerializerID(ModelSerializer):
    class Meta:
            model = Transaccion
            fields = ['mp_id']

