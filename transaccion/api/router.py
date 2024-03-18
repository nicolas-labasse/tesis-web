from rest_framework.routers import DefaultRouter
from transaccion.api.views import TransaccionApiViewSet
from django.urls import path

router = DefaultRouter()

router.register(prefix='', viewset=TransaccionApiViewSet, basename='transaccion')