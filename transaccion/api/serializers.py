from rest_framework.serializers import ModelSerializer
from transaccion.models import  TransaccionID




class TransaccionSerializer(ModelSerializer):
    class Meta:
        model = TransaccionID
        fields = '__all__'