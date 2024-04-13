from django import views
from django.urls import path
from ProyectoHistoryArApp.views import *
urlpatterns = [
  #Paths de prueba que debo borrar
  path('success/', success, name='success'),
  path('pending/', pending, name='pending'),
  path('failure/', failure, name='failure'),

  #Index
  path('', home, name='home'),
  path('favoritos/<int:id>/', favoritos, name='favoritos'),
  path('contacto/', contacto, name='contacto'),

  #Suscripcion
  path('suscribirse/', suscribirse, name='suscribirse'),

  #Email
  path('contacto_email/', contacto_email, name='contacto_email'),
  path('gracias/', gracias, name='gracias'),


  #Perfil Usuario
  path('perfil/<int:id>', perfil, name='perfil'),
  path('editar_imagen_perfil/', editar_imagen_perfil, name='editar_imagen_perfil'),
  path('eliminar_favorito/', eliminar_favorito, name='eliminar_favorito'),

  #Comentario
  path('eliminar_comentario/<int:id>/<int:id_recorrido>/', eliminar_comentario, name='eliminar_comentario'),

  #Recorrido
  path('recorrido/', recorrido, name='recorrido'),
  path('recorrido_detalle/<int:id>/', recorrido_detalle, name='recorrido_detalle'),



  path('suscripciones/', suscripciones, name='suscripciones'),
  
  path('panel_admin/', panel_admin, name='panel_admin'),

  #Usuarios
  path('usuarios/', usuarios, name='usuarios'),
  path('crear_usuario', crear_usuario, name='crear_usuario'),
  path('editar_usuario/<int:id>/', editar_usuario, name='editar_usuario'),
  path('eliminar_usuario/<int:id>/', eliminar_usuario, name='eliminar_usuario'),
  path('detalle_usuario/<int:id>/', detalle_usuario, name='detalle_usuario'),

  #Recorridos
  path('recorridos/', recorridos, name='recorridos'),
  path('crear_recorrido', crear_recorrido, name='crear_recorrido'),
  path('editar_recorrido/<int:id>/', editar_recorrido, name='editar_recorrido'),
  path('eliminar_recorrido/<int:id>/', eliminar_recorrido, name='eliminar_recorrido'),
  path('detalle_recorrido/<int:id>/', detalle_recorrido, name='detalle_recorrido'),

  #Puntos de Interes
  path('puntos_interes/', puntos_interes, name='puntos_interes'),
  path('crear_punto_interes', crear_punto_interes, name='crear_punto_interes'),
  path('editar_punto_interes/<int:id>/', editar_punto_interes, name='editar_punto_interes'),
  path('eliminar_punto_interes/<int:id>/', eliminar_punto_interes, name='eliminar_punto_interes'),
  path('detalle_punto_interes/<int:id>/', detalle_punto_interes, name='detalle_punto_interes'),

  #Transacciones
  path('transacciones/', transacciones, name='transacciones'),

]