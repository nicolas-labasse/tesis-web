from rest_framework.routers import DefaultRouter
from calificacion.api.views import CalificacionApiViewSet
from django.urls import path

router = DefaultRouter()

router.register(prefix='', viewset=CalificacionApiViewSet, basename='calificacion')