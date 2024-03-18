from rest_framework.routers import DefaultRouter
from transaccion.api.views import TransaccionIDApiViewSet
from django.urls import path

router = DefaultRouter()

router.register(prefix='', viewset=TransaccionIDApiViewSet, basename='transaccion')