from rest_framework.routers import DefaultRouter
from transaccion.api.views import TransaccionApiViewSet


router = DefaultRouter()

router.register(prefix='', viewset= TransaccionApiViewSet, basename='transaccion')