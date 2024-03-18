from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from calificacion.api.serializers import CalificacionSerializer
from calificacion.models import Calificacion
from usuario.models import Usuario
from recorrido.models import Recorrido
from django.contrib.auth.models import User

class CalificacionApiViewSet(ModelViewSet):
    serializer_class = CalificacionSerializer
    queryset = Calificacion.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        usuario_id = data.get('usuario')
        
        if isinstance(usuario_id, list):
            usuario_id = usuario_id[0]

        recorrido_id = data.get('recorrido')
        if isinstance(recorrido_id, list):
            recorrido_id = recorrido_id[0]
            
        try:
            calificacion_existente = Calificacion.objects.get(usuario=usuario_id, recorrido=recorrido_id)
            if calificacion_existente:
                serializer = self.get_serializer(calificacion_existente, data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save() 
                return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Calificacion.DoesNotExist:
            try:
                usuario = Usuario.objects.get(id=usuario_id)
                recorrido = Recorrido.objects.get(id=recorrido_id)
            except Usuario.DoesNotExist:
                    raise Exception('Usuario no encontrado')
            except Recorrido.DoesNotExist:
                    raise Exception('Recorrido no encontrado')
                
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(usuario=usuario, recorrido=recorrido)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

