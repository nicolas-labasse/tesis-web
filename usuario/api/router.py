from rest_framework.routers import DefaultRouter
from usuario.api.views import UsuarioApiViewSet
from django.urls import path

router = DefaultRouter()

router.register(prefix='', viewset=UsuarioApiViewSet, basename='usuario')


