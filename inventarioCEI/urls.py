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
    url(r'^logout/$', auth_views.logout, {'next_page': 'index'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^deleting/$', views.deleteRes, name='deleteRes'),
    url(r'^password/$', views.change_password, name='change_password'),
    path('update_articulo', views.update_articulo, name='update_articulo'),
    path('reserva_articulo', views.reserva_articulo, name='reserva_articulo'),
    path('landingAdmin/', views.LandingAdmin.as_view(), name='landingAdmin'),
    re_path(r'ficha/(?P<id>[0-9]*)/$', views.ficha, name='ficha')
    ]

#urlpatterns += patterns('', url(r'^media/(?P<path>.*)$','django.views.static.serve', {
#        'document_root': settings.MEDIA_ROOT,
#    }),)



urlpatterns += staticfiles_urlpatterns()


