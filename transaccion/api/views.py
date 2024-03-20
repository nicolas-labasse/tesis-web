import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from transaccion.api.serializers import TransaccionSerializer
from transaccion.models import Transaccion
from django.shortcuts import get_object_or_404
from usuario.models import Usuario


class TransaccionApiViewSet(ModelViewSet):
    serializer_class = TransaccionSerializer
    queryset = Transaccion.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        mp_id = data.get('id')
        usuario_id = 1
        precio = 1250
        
        if mp_id and usuario_id:
            usuario = get_object_or_404(Usuario, id=usuario_id)
            transaccion = Transaccion.objects.create(mp_id=mp_id, usuario=usuario, precio=int(precio))
            serializer = self.get_serializer(transaccion)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response("Error: Se requiere ID de transacción y ID de usuario", status=status.HTTP_400_BAD_REQUEST)
        



