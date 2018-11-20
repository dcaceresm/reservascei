from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = [
    path('', views.index, name='index'),
    url(r'^profile/$', views.showProfile, name='profile'),
    url(r'^login/$', views.customlogin, name='login'),
    #url(r'^logout/$', auth_views.LogoutView.as_view(), {'next_page': 'index'}, name='logout'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^deleting/$', views.deleteRes, name='deleteRes'),
    url(r'^password/$', views.change_password, name='change_password'),
    path('update_articulo', views.update_articulo, name='update_articulo'),
    path('reserva_articulo', views.reserva_articulo, name='reserva_articulo'),
    path('landingAdmin/', views.LandingAdmin.as_view(), name='landingAdmin'),
    path('simpleAdmin/', views.SimpleAdmin.as_view(), name='simpleAdmin'),
    path('calendarAdmin/', views.calendarAdmin, name = 'calendarAdmin'),
    path('landingUser/', views.buscar, name = 'buscar'),
    path('calendar/', views.calendar, name='calendar'),
    path('goToArticulos/', views.goToArticulos, name='goToArticulos'),
    path('goToEspacios/', views.goToEspacios, name='goToEspacios'),
    path('busquedaAvanzada/', views.busquedaAvanzada, name='busquedaAvanzada'),
    path('borrarPrestamo/', views.borrarPrestamo, name='borrarPrestamo'),
    path('borrarArticulo/', views.borrarArticulo, name='borrarArticulo'),
    path('borrarReserva/', views.borrarReserva, name='borrarReserva'),
    path('borrarEspacio/', views.borrarEspacio, name='borrarEspacio'),
    path('borrarUsuario/', views.borrarUsuario, name='borrarUsuario'),
    path('verPrestamo/', views.verPrestamo, name='verPrestamo'),
    path('simpleAdminAction/', views.simpleAdminAction, name='simpleAdminAction'),
    path('AceptarReservas/<str:string_id>', views.AceptarReservas, name="AceptarReservas"),
    path('calendarAdmin/', views.calendarAdmin, name='calendarAdmin'),
    path('RechazarReservas/<str:string_id>', views.RechazarReservas, name="RechazarReservas"),
    re_path(r'ficha/(?P<id>[0-9]*)/$', views.ficha, name='ficha')
    ]

#urlpatterns += patterns('', url(r'^media/(?P<path>.*)$','django.views.static.serve', {
#        'document_root': settings.MEDIA_ROOT,
#    }),)



urlpatterns += staticfiles_urlpatterns()
