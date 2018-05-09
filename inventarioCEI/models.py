from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
    )

    rut = models.CharField(max_length=15, null=True, blank=True, unique=True)
    mail = models.CharField(max_length=200, blank=True)
    isAdmin = models.BooleanField(default=False)
    hab = models.BooleanField(default = 1)


    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.rut

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Espacio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)
    URLfoto = models.CharField(max_length=100)
    estado = models.CharField(max_length=20)
    capacidad = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    rut = models.CharField(max_length=100)
    fh_reserva = models.DateTimeField()
    fh_ini_reserva = models.DateTimeField()
    fh_fin_reserva = models.DateTimeField()
    estado_reserva = models.CharField(max_length=100)
    id_objeto = models.IntegerField()
    tipo_objeto = models.CharField(max_length=100)

    def __str__(self):
        return self.rut

class Articulo(models.Model):
    nombre = models.CharField(max_length=100)
    URLfoto = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)
    estado = models.CharField(max_length=100)
    lista_tags = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Prestamo(models.Model):
    rut = models.CharField(max_length=100)
    fh_ini_prestamo = models.DateTimeField()
    fh_fin_prestamo = models.DateTimeField()
    estado_prestamo = models.CharField(max_length=100)
    id_objeto = models.IntegerField()
    tipo_objeto = models.CharField(max_length=100)

    def __str__(self):
        return self.rut