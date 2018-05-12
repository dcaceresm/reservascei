from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .models import Articulo


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class LandingAdmin(TemplateView):
    template_name = "landingPageAdmin.html"

    def get_context_data(self, **kwargs):
        return {}


def ficha(request, id):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:  # IF USER IS STAFF OR ADMIN
            try:  # IF ITEM ID EXISTS
                obj = Articulo.objects.get(pk=id)
                context = {'articulo': obj}
                return render(request, 'articulo_admin.html', context)
            except:  # IF ITEM ID DOESNT EXISTS
                context = {'id': id}
                return render(request, 'articulo_admin.html', context)
        else:
            try:
                obj = Articulo.objects.get(pk=id)
                context = {'articulo': obj}
                return render(request, 'articulo.html', context)
            except:
                context = {'id': id}
                return render(request, 'articulo.html', context)
    else:  # USER IS NOT LOGGED IN
        return redirect('/')  # REDIRECT TO INDEX (LOGIN) PAGE

def update_articulo(request):
    if request.method == 'POST':
        id = request.POST['id']
        articulo = Articulo.objects.get(pk = id)
        articulo.name = request.POST['name']
        articulo.text = request.POST['description']
        articulo.status = request.POST['status']
        articulo.tags = request.POST['tags']
        articulo.save()
        return redirect('/ficha/' + id + '/?updated=True')
    else:
        return HttpResponse("Whoops!")
