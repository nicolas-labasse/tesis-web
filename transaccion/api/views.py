from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from transaccion.api.serializers import TransaccionSerializer
from transaccion.models import TransaccionID

    
class TransaccionIDApiViewSet(ModelViewSet):
    serializer_class = TransaccionSerializer
    queryset = TransaccionID.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        print("Datos recibidos en el webhook:", data)
        id_transaccion = data.get('id')  # Obtener el ID de la data

        # Crear una instancia de TransaccionID y guardar el ID recibido
        transaccion_id = TransaccionID.objects.create(idTransaccion=id_transaccion)

        # Puedes hacer otras cosas con la instancia de TransaccionID si es necesario
        
        return Response(status=status.HTTP_201_CREATED)  # Devolver una respuesta exitosa