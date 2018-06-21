from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import *
from django.shortcuts import render, redirect, get_object_or_404

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class LandingAdmin(TemplateView):
    template_name = "landingPageAdmin.html"


    def get_context_data(self, **kwargs):
        context = super(LandingAdmin, self).get_context_data(**kwargs)
        context['reservas'] = Reserva.objects.all().order_by("-pk")
        context['estados_reserva'] = Reserva.ESTADO_CHOICES

        context['prestamos'] = Prestamo.objects.all().order_by("-pk")
        context['estados_prestamo'] = Prestamo.ESTADO_CHOICES
        context['estados_prestamo_tipo'] = Prestamo.TIPO_CHOICES

        context['usuarios'] = Profile.objects.all().order_by("-pk")
        context['estados_usuario'] = Profile.ESTADO_CHOICES

        context['articulos'] = Articulo.objects.all().order_by("-pk")
        context['estados_articulo'] = Articulo.ESTADO_CHOICES

        context['espacios'] = Espacio.objects.all().order_by("-pk")
        context['estados_espacio'] =Espacio.ESTADO_CHOICES

        return context

def AceptarReservas(request, string_id=""):
    if string_id == "":
        return redirect('inventario:landingAdmin')

    id_elements = string_id.split(",")
    for id_elemento in id_elements:
        reserva = get_object_or_404(Reserva, pk=id_elemento)
        reserva.estado_reserva = Reserva.ESTADO_CHOICES[1][0]
        reserva.save()
        try:
            existe = Prestamo.objects.get(id=id_elemento)
        except Prestamo.DoesNotExist:
            existe = None
            prestamo = Prestamo(rut=reserva.rut, fh_ini_prestamo=reserva.fh_ini_reserva
                            , fh_fin_prestamo=reserva.fh_fin_reserva, estado_prestamo='vigente'
                            , tipo_objeto=reserva.tipo_objeto, id_objeto=reserva.id_objeto)
            prestamo.save();

    return redirect('inventario:landingAdmin')

def RechazarReservas(request, string_id=""):
    if string_id == "":
        return redirect('inventario:landingAdmin')

    id_elements = string_id.split(",")
    for id_elemento in id_elements:
        reserva = get_object_or_404(Reserva, pk=id_elemento)
        reserva.estado_reserva = Reserva.ESTADO_CHOICES[2][0]
        reserva.save()
    return redirect('inventario:landingAdmin')

def borrarPrestamo(request):
    # id_prestamo =request.POST["identificador"]
    # prestamo= get_object_or_404(Prestamo,pk=id_prestamo)
    # prestamo.delete()
    response = redirect('inventario:landingAdmin')
    response['Location'] += '?tab=prestamos'
    return response

def borrarUsuario(request):
    # rut_usuario =request.POST["identificador"]
    # profile = get_object_or_404(Profile, rut=rut_usuario)
    # profile.delete()
    response = redirect('inventario:landingAdmin')
    response['Location'] += '?tab=usuarios'
    return response

def borrarEspacio(request):
    # id_espacio =request.POST["identificador"]
    # espacio= get_object_or_404(Espacio,pk=id_espacio)
    # espacio.delete()
    response = redirect('inventario:landingAdmin')
    response['Location'] += '?tab=espacios'
    return response

def borrarArticulo(request):
    # id_articulo =request.POST["identificador"]
    # articulo= get_object_or_404(Articulo,pk=id_articulo)
    # articulo.delete()
    response = redirect('inventario:landingAdmin')
    response['Location'] += '?tab=articulos'
    return response

def borrarReserva(request):
    # id_reserva =request.POST["identificador"]
    # reserva= get_object_or_404(Espacio,pk=id_reserva)
    # reserva.delete()
    response = redirect('inventario:landingAdmin')
    response['Location'] += '?tab=reservas'
    return response

def verPrestamo(request):
    id_prestamo =request.POST["identificador"]
    prest = get_object_or_404(Prestamo, pk=id_prestamo)
    return HttpResponse("Redirigir a ficha de prestamo: "+ str(prest.id))
    #renderear ficha
    #return redirect('inventario:landingAdmin')

def crearPrestamo(request):
    return redirect('inventario:landingAdmin')

