from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^profile/$', views.showProfile, name='profile'),
    url(r'^login/$', views.customlogin, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'index'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^deleting/$', views.deleteRes, name='deleteRes'),
    url(r'^password/$', views.change_password, name='change_password'),
    #url(r'^admin/', admin.site.urls),
]