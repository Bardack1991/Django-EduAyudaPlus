from django.urls import path, include
from . import views

#URL APP
urlpatterns = [
    path('editar-cuenta', views.editarCuenta, name='editar-cuenta'),
    path('registro', views.registro, name='registro'),
    path('', views.inicio, name='inicio'),
    path('inicio-sesion', views.inicioSesion, name='inicio-sesion'),
    path('menu-usuario', views.menuUsuario, name='menu-usuario'),
    path('recuperar-cuenta', views.recuperarCuenta, name='recuperar-cuenta'),
    path('logout', views.logout_view, name='logout'),
    path('carga-archivo/', views.carga_archivo, name='carga_archivo'),
    path('eliminar-archivo/<int:archivo_id>/', views.eliminar_archivo, name='eliminar_archivo'),
]

# URL API
api_urlpatterns = [
    path('inicio-sesion', views.get_token, name='api_inicio_sesion'),
    path('carga-archivo/', views.carga_archivo_api, name='api_carga_archivo'),
    path('servicios', views.servicio_list, name='servicio_list'),
    path('historial-servicios', views.historial_servicios_list, name='historial_servicios_list'),
]

urlpatterns += [
    path('api/', include((api_urlpatterns, 'api'))),
]