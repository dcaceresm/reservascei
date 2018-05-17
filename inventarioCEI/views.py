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
        context['prestamos'] = Prestamo.objects.all().order_by("-pk")
        context['estados_prestamo'] = Prestamo.ESTADO_CHOICES
        prestamos = Prestamo.objects.all().order_by("-pk")
        articulos = Articulo.objects.all().order_by("-pk")
        espacios = Espacio.objects.all().order_by("-pk")
        return context

def AceptarReservas(request):
    id_elemento = request.POST["fila"]
    reserva = get_object_or_404(Reserva, pk=id_elemento)
    reserva.estado_reserva = "Aceptado"
    reserva.save()
    return redirect('inventario:landingAdmin')
