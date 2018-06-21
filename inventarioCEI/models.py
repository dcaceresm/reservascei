from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

class Profile(models.Model):
    ESTADO_CHOICES = (
        ('Habilitado', 'Habilitado'),
        ('Inhabilitado', 'Inhabilitado'),
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
    )

    rut = models.CharField(max_length=15, null=True, blank=True, unique=True)
    mail = models.EmailField(max_length=150, unique=True)
    isAdmin = models.BooleanField(default=False)

    hab = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='Habilitado')


    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)



    # def __str__(self):
    #     return self.user.username

    def __str__(self):
        return self.user.first_name + " " +self.user.last_name + " " +self.rut

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)
    #
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()




class Espacio(models.Model):
    ESTADO_CHOICES = (
        ('Disponible', 'Disponible'),
        ('En préstamo', 'En préstamo'),
        ('En reparación', 'En reparación'),
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)
    image = models.ImageField(upload_to='../img/espacios')
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='Disponible')
    capacidad = models.IntegerField(default=0)

    reservas = GenericRelation('Reserva')
    prestamos = GenericRelation('Prestamo')

    def __str__(self):
        return self.nombre


class Articulo(models.Model):

    ESTADO_CHOICES = (
        ('Disponible', 'Disponible'),
        ('En préstamo', 'En préstamo'),
        ('En reparación', 'En reparación'),
        ('Perdido', 'Perdido'),
    )

    nombre = models.CharField(max_length=100)
    image = models.ImageField(upload_to='../img/articulos')
    descripcion = models.CharField(max_length=200)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='Disponible')
    lista_tags = models.CharField(max_length=200)

    reservas = GenericRelation('Reserva')
    prestamos = GenericRelation('Prestamo')

    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    ESTADO_CHOICES = (
        ('Pendiente', 'Pendiente'),
        ('Aceptada', 'Aceptada'),
        ('Rechazada', 'Rechazada'),
    )
    TIPO_CHOICES=(
        ('Artículo', 'Artículo'),
        ('Espacio','Espacio'),
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)

    fh_reserva = models.DateTimeField()
    fh_ini_reserva = models.DateTimeField()
    fh_fin_reserva = models.DateTimeField()
    estado_reserva = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='Pendiente')

    limit = models.Q(app_label='inventarioCEI', model='articulo') | models.Q(app_label='inventarioCEI', model='espacio')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=limit)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return str(self.profile.user.username) + " " + str(self.content_object.nombre)


class Prestamo(models.Model):
    ESTADO_CHOICES=(
        ('Vigente', 'Vigente'),
        ('Caducado','Caducado'),
        ('Perdido', 'Perdido'),
    )
    TIPO_CHOICES = (
        ('Artículo', 'Artículo'),
        ('Espacio', 'Espacio'),
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)

    fh_ini_prestamo = models.DateTimeField()
    fh_fin_prestamo = models.DateTimeField()
    estado_prestamo = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='Vigente')

    limit = models.Q(app_label='inventarioCEI', model='articulo') | models.Q(app_label='inventarioCEI', model='espacio')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=limit)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return str(self.profile.user.username) + " " + str(self.content_object.nombre)