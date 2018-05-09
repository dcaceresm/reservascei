from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Articulo
from django.shortcuts import render, redirect

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def buscar(request):

    if request.method == "POST":
        busqueda = request.POST['elemento']
        lista = Articulo.objects.filter(lista_tags__contains=busqueda)
        return render(request, 'inventarioCEI/buscar.html', {'lista': lista})
    else:
        lista = []
        return render(request, 'inventarioCEI/buscar.html', {'lista': lista})


class LandingAdmin(TemplateView):
    template_name = "inventarioCEI/landingPageAdmin.html"

    def get_context_data(self, **kwargs):
        return {}

