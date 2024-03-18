import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from transaccion.api.serializers import TransaccionSerializer, TransaccionSerializerID
from transaccion.models import Transaccion
from django.shortcuts import get_object_or_404
from usuario.models import Usuario

class TransaccionApiViewSet(ModelViewSet):
    serializer_class = TransaccionSerializerID
    queryset = Transaccion.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        mp_id = data.get('id')
        
        if mp_id:
            mp_api_url = 'https://api.mercadopago.com/v1/payments/' + str(mp_id)
            headers = {
                'Authorization': 'Bearer <TEST-4400576109328385-020611-19bb4fe2e975a39a1a2050a1955b5a15-1669576371>',
                'Content-Type': 'application/json'
            }
            response = requests.get(mp_api_url, headers=headers)

            if response.status_code == 200:
                mp_data = response.json()
                precio_pago = mp_data['transaction_amount']
                estado_pago = mp_data['status']
                fecha_pago = mp_data['date_created']
                
                usuario = get_object_or_404(Usuario, id=1)
                
                transaccion = Transaccion.objects.create(
                    mp_id=mp_id, 
                    usuario=usuario, 
                    precio=precio_pago,
                    estado_pago=estado_pago,
                    fecha_pago=fecha_pago
                )
                
                serializer = self.get_serializer(transaccion)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response("Error al obtener información de Mercado Pago", status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response("Error: ID de pago no proporcionado", status=status.HTTP_400_BAD_REQUEST)

