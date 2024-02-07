from rest_framework.routers import DefaultRouter
from recorrido.api.views import RecorridoApiViewSet

router = DefaultRouter()

router.register(prefix='', viewset=RecorridoApiViewSet, basename='recorrido')