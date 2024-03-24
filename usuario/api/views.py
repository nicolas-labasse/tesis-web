from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from usuario.models import Usuario
from usuario.api.serializers import UsuarioSerializer, UsuarioFavoritoSerializer, EditarImagenUsuarioSerializer, EditarUsuarioNombreSerializer

"""class UsuarioApiViewSet(ModelViewSet):
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)"""

class UsuarioApiViewSet(ModelViewSet):
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            print('Exception:', e)
            return Response({'error': 'Error interno del servidor no entre al try'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class UsuarioFavoritoAPIView(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioFavoritoSerializer
    def put(self, request, id_usuario):
        try:
            usuario = self.get_object()
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditarImagenUsuario(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = EditarImagenUsuarioSerializer

    def update(self, request, *args, **kwargs):
        try:
            usuario = self.get_object()
            
            imagen_url = request.data.get('imagen_update', '')
            request.data['imagen_url'] = f'images/{imagen_url}'

            serializer = self.get_serializer(usuario, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            
            usuario.imagen = request.data.get('imagen_url', usuario.imagen)

            self.perform_update(serializer)

            return Response(serializer.data)
        except Exception as e:
            print('Exception:', e)
            return Response({'error': 'Error interno del servidor'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class EditarUsuarioNombre(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = EditarUsuarioNombreSerializer

    def update(self, request, *args, **kwargs):
        try:
            usuario = self.get_object()
            
            data = request.data.dict() 
            data['nombre'] = request.data.get('nombre', usuario.nombre)  

            serializer = self.get_serializer(usuario, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Exception as e:
            print('Exception:', e)
            return Response({'error': 'Error interno del servidor'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



