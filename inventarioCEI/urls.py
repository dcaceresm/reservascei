from django.urls import path, re_path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('update_articulo', views.update_articulo, name='update_articulo'),
    path('reserva_articulo', views.reserva_articulo, name='reserva_articulo'),
    path('landingAdmin/', views.LandingAdmin.as_view(), name='landingAdmin'),
    re_path(r'ficha/(?P<id>[0-9]*)/$', views.ficha, name='ficha'),
]

urlpatterns += staticfiles_urlpatterns()

