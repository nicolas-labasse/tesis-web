from django.urls import path
from ProyectoHistoryArApp.views import *


urlpatterns = [
  path('', home, name='home'),
  path('recorrido/', recorrido, name='recorrido'),
  path('recorrido_detalle/', recorrido_detalle, name='recorrido_detalle'),
  path('suscripciones/', suscripciones, name='suscripciones'),
  path('panel_admin/', panel_admin, name='panel_admin'),

  #Pagos
  path('generar_compra/', generar_compra, name='generar_compra'),

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

]