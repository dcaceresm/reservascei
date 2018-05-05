from django.db import models

"""
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=100)
    mail = models.EmailField(max_length=100)
    contrasena = models.CharField(max_length=100)
    esAdmin = models.BooleanField()
    habilitado = models.BooleanField()

    def __str__(self):
        return self.nombre

"""

class Espacio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)
    URLfoto = models.CharField(max_length=100)
    estado = models.CharField(max_length=20)
    capacidad = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

class Reservas(models.Model):
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

class Prestamos(models.Model):
    rut = models.CharField(max_length=100)
    fh_ini_prestamo = models.DateTimeField()
    fh_fin_prestamo = models.DateTimeField()
    estado_prestamo = models.CharField(max_length=100)
    id_objeto = models.IntegerField()
    tipo_objeto = models.CharField(max_length=100)

    def __str__(self):
        return self.rut