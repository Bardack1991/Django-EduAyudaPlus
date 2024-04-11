from django.urls import path
from . import views

urlpatterns = [
    path('editar-cuenta', views.editarCuenta, name='editar-cuenta'),
    path('registro', views.registro, name='registro'),
    path('', views.inicio, name='inicio'),
    path('inicio-sesion', views.inicioSesion, name='inicio-sesion'),
    path('menu-usuario', views.menuUsuario, name='menu-usuario'),
    path('recuperar-cuenta', views.recuperarCuenta, name='recuperar-cuenta'),
]