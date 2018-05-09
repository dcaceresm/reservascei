from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('landingUser/', views.buscar, name = 'buscar'),
    path('landingAdmin/', views.LandingAdmin.as_view(), name='landingAdmin'),
]

