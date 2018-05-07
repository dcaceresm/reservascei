
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


from .models import *


admin.site.register(Espacio)
admin.site.register(Reserva)
admin.site.register(Articulo)
admin.site.register(Prestamo)
admin.site.register(Profile)