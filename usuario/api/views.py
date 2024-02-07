from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from usuario.models import Usuario
from usuario.api.serializers import UsuarioSerializer
from rest_framework.parsers import MultiPartParser , FormParser, JSONParser

class UsuarioApiViewSet(ModelViewSet):
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

