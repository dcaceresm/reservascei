from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('landingUser/', views.buscar, name = 'buscar'),
    path('calendar/', views.calendar, name='calendar'),
    path('goToArticulos/', views.goToArticulos, name='goToArticulos'),
    path('goToEspacios/', views.goToEspacios, name='goToEspacios'),
    path('busquedaAvanzada/', views.busquedaAvanzada, name='busquedaAvanzada'),
    path('landingAdmin/', views.LandingAdmin.as_view(), name='landingAdmin'),
]

