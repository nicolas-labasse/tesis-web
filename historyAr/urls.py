"""historyAr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from pInteres.api.router import router as router_pInteres
from recorrido.api.router import router as router_recorrido
from usuario.api.router import router as router_usuario
from transaccion.api.router import router as router_transaccion
from calificacion.api.router import router as router_calificacion
from rest_framework import permissions
from django.contrib.auth.views import LoginView


schema_view = get_schema_view(
    openapi.Info(
        title="HistoryAR API",
        default_version='v1',
        description="API for HistoryAR",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="nicolaslabasse4@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/recorrido/', include(router_recorrido.urls), {'basename': 'recorrido'}),
    path('api/puntoInteres/', include(router_pInteres.urls), {'basename': 'puntoInteres'}),
    path('api/usuario/', include(router_usuario.urls), {'basename': 'usuario'}),
    path('api/usuario/', include('usuario.api.router'), {'basename': 'usuario-favorito'}),
    path('api/usuario/', include('usuario.api.router'), {'basename': 'editar-imagen-usuario'}),
    path('api/usuario/', include('usuario.api.router'), {'basename': 'editar-usuario-nombre'}),
    path('api/transaccion/', include(router_transaccion.urls), {'basename': 'transaccion'}),
    path('api/calificacion/', include(router_calificacion.urls), {'basename': 'calificacion'}),
    

    # Swagger
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # ReDoc
    path('redocs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)