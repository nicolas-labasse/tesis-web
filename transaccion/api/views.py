from django.conf import settings
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
        mp_id = data['data']['id']
        usuario_id = request.query_params.get('id')
        precio = webHookTransaccion(mp_id)

        if mp_id and usuario_id:
            usuario = get_object_or_404(Usuario, id=usuario_id)
            transaccion = Transaccion.objects.create(mp_id=mp_id, usuario=usuario, precio=precio)
            serializer = self.get_serializer(transaccion)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(f"Error: Se requiere ID de transacción y ID de usuario.", status=status.HTTP_400_BAD_REQUEST)


def webHookTransaccion(mp_id):
    url = f'https://api.mercadopago.com/v1/payments/{mp_id}'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {settings.MERCADO_PAGO_ACCESS_TOKEN}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        transaccion = response.json()
        total_paid_amount = transaccion['transaction_details']['total_paid_amount']
        return total_paid_amount
    else:
        return None
        
        




