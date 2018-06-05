from django.urls import path

from . import views

app_name = 'inventario'
urlpatterns = [
    path('', views.index, name='index'),
    path('landingAdmin/', views.LandingAdmin.as_view(), name='landingAdmin'),
    path('borrarPrestamo/', views.borrarPrestamo, name='borrarPrestamo'),
    path('verPrestamo/', views.verPrestamo, name='verPrestamo'),
    path('borrarUsuario/', views.borrarUsuario, name='borrarUsuario'),
    path('AceptarReservas/<str:string_id>', views.AceptarReservas, name="AceptarReservas"),
    path('RechazarReservas/<str:string_id>', views.RechazarReservas, name="RechazarReservas"),
]

