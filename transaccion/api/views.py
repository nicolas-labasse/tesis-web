from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from transaccion.api.serializers import TransaccionSerializer
from transaccion.models import Transaccion


class TransaccionApiViewSet(ModelViewSet):
    serializer_class = TransaccionSerializer
    queryset = Transaccion.objects.all()
    print("TransaccionApiViewSet")
    def create(self, request, *args, **kwargs):
        data = request.data
        print("Datos recibidos en el webhook:", data)
        return Response()