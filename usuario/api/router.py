from rest_framework.routers import DefaultRouter
from usuario.api.views import UsuarioApiViewSet, UsuarioFavoritoAPIView , EditarImagenUsuario, EditarUsuarioNombre
from django.urls import include, path

router = DefaultRouter()

router.register(r'usuarios', UsuarioApiViewSet, basename='usuario')
router.register(r'usuario_favorito', UsuarioFavoritoAPIView, basename='usuario-favorito')
router.register(r'editar_imagen_usuario', EditarImagenUsuario, basename='editar-imagen-usuario')
router.register(r'editar_usuario_nombre', EditarUsuarioNombre, basename='editar-usuario-nombre')

urlpatterns = [
    path('', include(router.urls)),
]


