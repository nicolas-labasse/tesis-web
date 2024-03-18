from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class TransaccionApiViewSet(ModelViewSet):
    print('vista del webhook')
    def get(self, request, *args, **kwargs):
        data = request.data
        print("Datos recibidos en la vista:", data)
        return Response(data)