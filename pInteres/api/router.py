from rest_framework.routers import DefaultRouter
from pInteres.api.views import PuntoInteresApiViewSet

router = DefaultRouter()

router.register(prefix='', viewset=PuntoInteresApiViewSet, basename='pInteres')