from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Articulo, Reserva
import datetime
from T3_INGSW import settings
from django.contrib.contenttypes.models import ContentType

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .models import *
from django.urls import reverse
import json

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


def ficha(request, id):
    if request.user.is_authenticated:
        print(settings.SITE_ROOT)
        try: # IF ITEM ID EXISTS
            obj = Articulo.objects.get(pk=id)

            # GET LASTEST RESERVATIONS
            reservas = Reserva.objects.filter(object_id= id).order_by('-id')[:10]

            # render
            if request.user.profile.isAdmin:  # IF USER IS STAFF OR ADMIN
                time = str(datetime.datetime.today())
                context = {'articulo': obj, 'time': time, 'reservas': reservas}
                return render(request, 'articulo_admin.html', context)
                #return render(request, 'articulo.html', context)
            else:
                rut = request.user.profile.rut
                time = str(datetime.datetime.today())
                context = {'articulo': obj, 'rut': rut, 'time': time, 'reservas': reservas}
                return render(request, 'articulo.html', context)
        except:
            if request.user.profile.isAdmin:  # IF USER IS STAFF OR ADMIN
                context = {'id': id}
                return render(request, 'articulo_admin.html', context)
                #return render(request, 'articulo.html', context)
            else:
                context = {'id': id}
                return render(request, 'articulo.html', context)
    else:  # USER IS NOT LOGGED IN
        return redirect('/')  # REDIRECT TO INDEX (LOGIN) PAGE


def update_articulo(request):
    if request.method == 'POST':
        id = request.POST['id']
        articulo = Articulo.objects.get(pk = id)
        articulo.nombre = request.POST['name']
        articulo.descripcion = request.POST['description']
        articulo.estado = request.POST['status']
        articulo.lista_tags = request.POST['tags']
        articulo.save()
        return redirect('/ficha/' + id + '/?updated=True')
    else:
        return HttpResponse("Whoops!")

def reserva_articulo(request):
    if request.method == 'POST':
        id = request.POST['id']
        articulo = Articulo.objects.get(pk = id)
        estado_reserva = request.POST['estado_reserva']
        fh_reserva = request.POST['fh_reserva']
        fh_ini = request.POST['inicio'] + " " + request.POST['hora_inicio']
        fh_termino = request.POST['termino'] + " " + request.POST['hora_termino']
        ct = ContentType.objects.get_for_model(articulo)
        reserva = Reserva.objects.create(profile=request.user.profile, fh_reserva=fh_reserva, fh_ini_reserva=fh_ini,
                                         fh_fin_reserva=fh_termino, estado_reserva=estado_reserva, object_id=id,
                                         content_type= ct)

        reserva.save()
        return redirect('/')
    else:
        return HttpResponse("Whoops!")

def index(request):

    #Envia a la pagina de inicio
    #Dependiendo si es admin o no

    if (request.user.is_authenticated):
        if request.user.profile.isAdmin:
            return HttpResponseRedirect(reverse('landingAdmin'))
        else:
            return HttpResponseRedirect(reverse('buscar'))
    return render(request, 'custom_login.html')


def showProfile(request):

    #Si no inicio sesion, se va al inicio
    if not (request.user.is_authenticated):
        return HttpResponseRedirect(reverse('index'))

    #Obtener reservas y prestamos
    reservas = Reserva.objects.filter(profile__rut=request.user.profile.rut).order_by('-id')[:10]
    prestamos = Prestamo.objects.filter(profile__rut=request.user.profile.rut).order_by('-id')[:10]

    #Enviarlos al perfil
    return render(request, 'user_profile.html', {'reservas': reservas, 'prestamos': prestamos})

def get_user(email):
    try:
        return Profile.objects.get(mail=email.lower()).user
    except Profile.DoesNotExist:
        return None


def customlogin(request):

    #Formulario recibe datos e inicia sesion

    email = request.POST['email']
    password = request.POST['password']
    username = get_user(email).username
    user = authenticate(username=username, password=password)

    #Si el usuario existe
    if user is not None:
        if user.is_active:
            login(request, user)

            #Redirigirlo si es admin o no
            if user.profile.isAdmin:
                return HttpResponseRedirect(reverse('landingAdmin'))
            else:
                return HttpResponseRedirect(reverse('buscar'))
        else:

            #Validador
            messages.error(request, 'Correo y/o Contraseña incorrectos')
            return HttpResponseRedirect(reverse('index'))
    else:
        messages.error(request, 'Correo y/o Contraseña incorrectos')
        return HttpResponseRedirect(reverse('index'))


def signup(request):

    #Recibe datos por post y crea usuario
    if request.method == "POST":
        rut = request.POST['rut']
        mail = request.POST['mail']
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        password = request.POST['password1']
        password2 = request.POST['password2']
        user = get_user(mail)

        #Valida que las contrasenas coincidan
        if password == password2:
            if user is None:
                user = User.objects.create_user(rut, mail, password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                user.refresh_from_db()
                user.profile.rut = rut
                user.profile.mail = mail
                user.save()
                user = authenticate(username=user.username, password=password)
                login(request, user)

                #Iniciar y redigir si es admin o no
                if user.profile.isAdmin:
                    return HttpResponseRedirect(reverse('landingAdmin'))
                else:
                    return HttpResponseRedirect(reverse('buscar'))
            else:
                return render(request, 'signup.html')
        else:
            messages.error(request,'Las contraseñas no coinciden')
            return render(request, 'signup.html')
    return render(request, 'signup.html')

def change_password(request):

    #Recibe datos por post y actualiza contrasena
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Su clave fue cambiada exitosamente')
            return redirect('change_password')
        else:

            #Validador
            messages.error(request, 'No se pudo cambiar su clave. Verifique que la clave actual o que la clave nueva'
                                    ' y su repetición coincidan.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })

def deleteRes(request):
    #Borra las reservas enviadas por POST
    delList = request.POST.getlist('element')
    Reserva.objects.filter(id__in=delList).delete()
    return HttpResponseRedirect(reverse('profile'))


def event_adding(event, di, df, type):
    if di.month < 10:
        month_i = "0" + str(di.month)
    else:
        month_i = str(di.month)

    if di.day < 10:
        day_i = "0" + str(di.day)
    else:
        day_i = str(di.day)

    if di.hour < 10:
        hour_i = "0" + str(di.hour)
    else:
        hour_i = str(di.hour)

    if di.minute < 10:
        minute_i = "0" + str(di.minute)
    else:
        minute_i = str(di.minute)

    if df.month < 10:
        month_f = "0" + str(df.month)
    else:
        month_f = str(df.month)

    if df.day < 10:
        day_f = "0" + str(df.day)
    else:
        day_f = str(df.day)

    if df.hour < 10:
        hour_f = "0" + str(df.hour)
    else:
        hour_f = str(df.hour)

    if df.minute < 10:
        minute_f = "0" + str(df.minute)
    else:
        minute_f = str(df.minute)

    if type == 1:
        name = (Espacio.objects.get(id=event.object_id)).nombre + "-" + event.estado_prestamo
    else:
        name = (Espacio.objects.get(id=event.object_id)).nombre + "-" + event.estado_reserva

    time_i = str(di.year) + "-" + str(month_i) + "-" + str(day_i) + "T" + hour_i + ":" + minute_i
    time_f = str(df.year) + "-" + str(month_f) + "-" + str(day_f) + "T" + hour_f + ":" + minute_f

    return {
        "title": name,
        "start": time_i,
        "end": time_f
    }


def calendar(request):
    events = [
    ]

    ct = ContentType.objects.get_for_model(Espacio)

    prestamos = Prestamo.objects.all()

    reservas = Reserva.objects.all()

    for i in range(0, len(prestamos)):

        event = prestamos[i]

        if event.content_type == ct:
            di = event.fh_ini_prestamo
            df = event.fh_fin_prestamo

            event_json = event_adding(event, di, df, 1)
            events.append(event_json)

    for i in range(0, len(reservas)):

        event = reservas[i]

        if event.content_type == ct:
            di = event.fh_ini_reserva
            df = event.fh_fin_reserva

            event_json = event_adding(event, di, df, 2)
            events.append(event_json)

    events_string = json.dumps(events)

    return render(request, 'calendario.html', {'events': events_string})


def buscar(request):
    if request.method == "POST":
        busqueda = request.POST['elemento']
        lista = Articulo.objects.filter(lista_tags__contains=busqueda)
        return render(request, 'buscar.html', {'lista': lista})
    else:
        lista = []
        return render(request, 'buscar.html', {'lista': lista})


def busquedaAvanzada(request):
    if request.method == "POST":
        busqueda = request.POST['elemento']
        estado = request.POST['estado']
        lista = Articulo.objects.filter(lista_tags__contains=busqueda)
        lista = lista.filter(estado__contains=estado)
        return render(request, 'busquedaAvanzada.html', {'lista': lista})
    else:
        lista = []
        return render(request, 'busquedaAvanzada.html', {'lista': lista})


def goToArticulos(request):
    if request.method == "POST":
        return redirect('buscar')
    else:
        return render(request, 'calendario.html')


def goToEspacios(request):
    if request.method == "POST":
        return redirect('calendar')
    else:
        return render(request, 'buscar.html')

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
