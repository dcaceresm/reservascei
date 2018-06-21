from django.urls import path, re_path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

app_name = 'inventario'
urlpatterns = [
    path('', views.index, name='index'),
    path('update_articulo', views.update_articulo, name='update_articulo'),
    path('reserva_articulo', views.reserva_articulo, name='reserva_articulo'),
    path('landingAdmin/', views.LandingAdmin.as_view(), name='landingAdmin'),
    path('borrarPrestamo/', views.borrarPrestamo, name='borrarPrestamo'),
    path('borrarArticulo/', views.borrarArticulo, name='borrarArticulo'),
    path('borrarReserva/', views.borrarReserva, name='borrarReserva'),
    path('borrarEspacio/', views.borrarEspacio, name='borrarEspacio'),
    path('borrarUsuario/', views.borrarUsuario, name='borrarUsuario'),
    path('verPrestamo/', views.verPrestamo, name='verPrestamo'),
    path('AceptarReservas/<str:string_id>', views.AceptarReservas, name="AceptarReservas"),
    path('RechazarReservas/<str:string_id>', views.RechazarReservas, name="RechazarReservas"),
    re_path(r'ficha/(?P<id>[0-9]*)/$', views.ficha, name='ficha'),

]

urlpatterns += staticfiles_urlpatterns()

