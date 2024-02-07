from rest_framework.serializers import ModelSerializer
from usuario.models import Usuario


class UsuarioSerializer(ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'