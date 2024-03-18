from rest_framework.viewsets import ModelViewSet
from pInteres.models import PuntoInteres
from pInteres.api.serializers import PuntoInteresSerializer
from rest_framework.response import Response
from rest_framework import status

"""class PuntoInteresApiViewSet(ModelViewSet):
    serializer_class = PuntoInteresSerializer 
    queryset = PuntoInteres.objects.all()
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)"""

from rest_framework.viewsets import ModelViewSet
from pInteres.models import PuntoInteres
from pInteres.api.serializers import PuntoInteresSerializer
from rest_framework.response import Response
from rest_framework import status

class PuntoInteresApiViewSet(ModelViewSet):
    serializer_class = PuntoInteresSerializer 
    queryset = PuntoInteres.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data

        ip_y_puerto = 'https://192.168.100.64:8080'
        
        imagen_url = data.get('imagen_url', '')  
        data['imagen_url'] = f'{ip_y_puerto}{imagen_url}'

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)





