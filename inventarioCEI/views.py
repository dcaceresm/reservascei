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
from datetime import date
import json



class LandingAdmin(TemplateView):
    template_name = "landingPageAdmin.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.isAdmin:
                return super(LandingAdmin, self).get(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('buscar'))
        else:  # USER IS NOT LOGGED IN
            return redirect('/')  # REDIRECT TO INDEX (LOGIN) PAGE

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
        context['estados_espacio'] = Espacio.ESTADO_CHOICES

        return context


def ficha(request, id):
    if request.user.is_authenticated:
        print(settings.SITE_ROOT)
        try:  # IF ITEM ID EXISTS
            obj = Articulo.objects.get(pk=id)

            # GET LASTEST RESERVATIONS
            reservas = Reserva.objects.filter(object_id=id).order_by('-id')[:10]

            # render
            if request.user.profile.isAdmin:  # IF USER IS STAFF OR ADMIN
                time = str(datetime.datetime.today())
                context = {'articulo': obj, 'time': time, 'reservas': reservas}
                return render(request, 'articulo_admin.html', context)
                # return render(request, 'articulo.html', context)
            else:
                rut = request.user.profile.rut
                time = str(datetime.datetime.today())
                context = {'articulo': obj, 'rut': rut, 'time': time, 'reservas': reservas}
                return render(request, 'articulo.html', context)
        except:
            if request.user.profile.isAdmin:  # IF USER IS STAFF OR ADMIN
                context = {'id': id}
                return render(request, 'articulo_admin.html', context)
                # return render(request, 'articulo.html', context)
            else:
                context = {'id': id}
                return render(request, 'articulo.html', context)
    else:  # USER IS NOT LOGGED IN
        return redirect('/')  # REDIRECT TO INDEX (LOGIN) PAGE


def update_articulo(request):
    if request.method == 'POST':
        id = request.POST['id']
        articulo = Articulo.objects.get(pk=id)
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
        articulo = Articulo.objects.get(pk=id)
        estado_reserva = request.POST['estado_reserva']
        fh_reserva = request.POST['fh_reserva']

        fh_ini = request.POST['inicio']
        h_ini = fh_ini.split(" ")[1]
        ampm_ini = fh_ini.split(" ")[2]
        if ampm_ini == 'PM':
            h_ini_arr = h_ini.split(":")
            hora_i = int(h_ini_arr[0]) + 12
            h_ini = str(hora_i) + ":" + h_ini_arr[1]
        d_ini = fh_ini.split(" ")[0].split("/")[0]
        m_ini = fh_ini.split(" ")[0].split("/")[1]
        y_ini = fh_ini.split(" ")[0].split("/")[2]
        fh_ini_formated = y_ini + "-" + m_ini + "-" + d_ini + " " + h_ini

        fh_termino = request.POST['termino']
        h_ter = fh_termino.split(" ")[1]
        ampm_ter = fh_termino.split(" ")[2]
        if ampm_ter == 'PM':
            h_ter_arr = h_ter.split(":")
            hora_t = int(h_ter_arr[0]) + 12
            h_ter = str(hora_t) + ":" + h_ter_arr[1]
        d_ter = fh_termino.split(" ")[0].split("/")[0]
        m_ter = fh_termino.split(" ")[0].split("/")[1]
        y_ter = fh_termino.split(" ")[0].split("/")[2]
        fh_ter_formated = y_ter + "-" + m_ter + "-" + d_ter + " " + h_ter


        ct = ContentType.objects.get_for_model(articulo)
        reserva = Reserva.objects.create(profile=request.user.profile, fh_reserva=fh_reserva, fh_ini_reserva=fh_ini_formated,
                                         fh_fin_reserva=fh_ter_formated, estado_reserva=estado_reserva, object_id=id,
                                         content_type=ct)

        reserva.save()
        return redirect('/profile')
    else:
        return HttpResponse("Whoops!")


def index(request):
    # Envia a la pagina de inicio
    # Dependiendo si es admin o no

    if (request.user.is_authenticated):
        if request.user.profile.isAdmin:
            return HttpResponseRedirect(reverse('calendarAdmin'))
        else:
            return HttpResponseRedirect(reverse('buscar'))
    return render(request, 'custom_login.html')


def showProfile(request):
    # Si no inicio sesion, se va al inicio
    if not (request.user.is_authenticated):
        return HttpResponseRedirect(reverse('index'))

    # Obtener reservas y prestamos
    reservas = Reserva.objects.filter(profile__rut=request.user.profile.rut).order_by('-id')[:10]
    prestamos = Prestamo.objects.filter(profile__rut=request.user.profile.rut).order_by('-id')[:10]

    # Enviarlos al perfil
    return render(request, 'user_profile.html', {'reservas': reservas, 'prestamos': prestamos})


def get_user(email):
    try:
        return Profile.objects.get(mail=email.lower()).user
    except Profile.DoesNotExist:
        return None


def customlogin(request):
    # Formulario recibe datos e inicia sesion

    email = request.POST['email']
    password = request.POST['password']
    username = get_user(email).username
    user = authenticate(username=username, password=password)

    # Si el usuario existe
    if user is not None:
        if user.is_active:
            login(request, user)

            # Redirigirlo si es admin o no
            if user.profile.isAdmin:
                return HttpResponseRedirect(reverse('calendarAdmin'))
            else:
                return HttpResponseRedirect(reverse('buscar'))
        else:

            # Validador
            messages.error(request, 'Correo y/o Contraseña incorrectos')
            return HttpResponseRedirect(reverse('index'))
    else:
        messages.error(request, 'Correo y/o Contraseña incorrectos')
        return HttpResponseRedirect(reverse('index'))


def signup(request):
    # Recibe datos por post y crea usuario
    if request.method == "POST":
        rut = request.POST['rut']
        mail = request.POST['mail']
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        password = request.POST['password1']
        password2 = request.POST['password2']
        user = get_user(mail)

        # Valida que las contrasenas coincidan
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

                # Iniciar y redigir si es admin o no
                if user.profile.isAdmin:
                    return HttpResponseRedirect(reverse('landingAdmin'))
                else:
                    return HttpResponseRedirect(reverse('buscar'))
            else:
                return render(request, 'signup.html')
        else:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'signup.html')
    return render(request, 'signup.html')


def change_password(request):
    # Recibe datos por post y actualiza contrasena
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Su clave fue cambiada exitosamente')
            return redirect('change_password')
        else:

            # Validador
            messages.error(request, 'No se pudo cambiar su clave. Verifique que la clave actual o que la clave nueva'
                                    ' y su repetición coincidan.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


def deleteRes(request):
    # Borra las reservas enviadas por POST
    delList = request.POST.getlist('element')
    Reserva.objects.filter(id__in=delList).delete()
    return HttpResponseRedirect(reverse('profile'))

def restarHoras(hora):
    if hora == 0:
        return 20
    if hora == 1:
        return 21
    if hora == 2:
        return 22
    if hora == 3:
        return 23
    return hora - 4

# event_adding: agrega un evento en el formato necesario para ser tomado por el calendario
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


# calendar: chequea los eventos que deben estar en la grilla
def calendar(request):
    if request.user.is_authenticated:
        events = []

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
    else:  # USER IS NOT LOGGED IN
        return redirect('/')  # REDIRECT TO INDEX (LOGIN) PAGE


# buscar: retorna una lista con los articulos que concuerdan con la busqueda
def buscar(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            busqueda = request.POST['elemento']
            lista = Articulo.objects.filter(lista_tags__contains=busqueda)
            return render(request, 'buscar.html', {'lista': lista})
        else:
            lista = Articulo.objects.all()[:5]
            return render(request, 'buscar.html', {'lista': lista})
    else:  # USER IS NOT LOGGED IN
        return redirect('/')  # REDIRECT TO INDEX (LOGIN) PAGE


def busquedaAvanzada(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            busqueda = request.POST['elemento']
            lista = Articulo.objects.filter(lista_tags__contains=busqueda)

            """id_elemento = request.POST['id_elemento']
            lista = Articulo.objects.filter(id = id_elemento)"""

            estado = request.POST['estado']
            if estado != "Todos":
                lista = lista.filter(estado__contains=estado)
            fecha_inicio = request.POST['fechaInicioBusq']
            fecha_fin = request.POST['fechaFinBusq']

            if (fecha_inicio != "") & (fecha_fin != ""):
                reservas = Reserva.objects.filter(estado_reserva="Aceptada") & \
                           (Reserva.objects.filter(fh_ini_reserva__range=[fecha_inicio, fecha_fin]) | \
                            Reserva.objects.filter(fh_fin_reserva__range=[fecha_inicio, fecha_fin]))

                for reserva in reservas:
                    id_object = reserva.object_id
                    object = Articulo.objects.get(id=id_object)
                    if object in lista:
                        lista = lista.exclude(id=id_object)

            return render(request, 'busquedaAvanzada.html', {'lista': lista})
        else:
            lista = []
            return render(request, 'busquedaAvanzada.html', {'lista': lista})
    else:  # USER IS NOT LOGGED IN
        return redirect('/')  # REDIRECT TO INDEX (LOGIN) PAGE


# goToArticulos: redirecciona a la busqueda del landing del user
def goToArticulos(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            return redirect('buscar')
        else:
            return render(request, 'calendario.html')

    else:  # USER IS NOT LOGGED IN
        return redirect('/')  # REDIRECT TO INDEX (LOGIN) PAGE


# goToEspacios: redirecciona a la gilla de landing user
def goToEspacios(request):
    if request.method == "POST":
        return redirect('calendar')
    else:
        return render(request, 'buscar.html')

def calendarAdmin(request):
    if request.user.is_authenticated:
        if request.user.profile.isAdmin:

            events = []

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
            return render(request, 'adminTabs/IndexTabFromAdmin.html', {'events': events_string})

        else:
            return redirect('/')
            #return redirect('landingUser/')
    else:  # USER IS NOT LOGGED IN
        return redirect('/')  # REDIRECT TO INDEX (LOGIN) PAGE


def AceptarReservas(request, string_id=""):
    if string_id == "":
        response = redirect('landingAdmin')
        response['Location'] += '?tab=reservas'
        return response

    id_elements = string_id.split(",")
    for id_elemento in id_elements:
        reserva = get_object_or_404(Reserva, pk=id_elemento)
        reserva.estado_reserva = Reserva.ESTADO_CHOICES[1][0]
        reserva.save()
        try:
            existe = Prestamo.objects.get(id=id_elemento)
        except Prestamo.DoesNotExist:
            existe = None
            prestamo = Prestamo(profile=reserva.profile, fh_ini_prestamo=reserva.fh_ini_reserva
                                , fh_fin_prestamo=reserva.fh_fin_reserva, estado_prestamo='Vigente'
                                , content_type=reserva.content_type, object_id=reserva.object_id)
            prestamo.save();

    response = redirect('landingAdmin')
    response['Location'] += '?tab=reservas'
    return response


def RechazarReservas(request, string_id=""):
    if string_id == "":
        response = redirect('landingAdmin')
        response['Location'] += '?tab=reservas'
        return response

    id_elements = string_id.split(",")
    for id_elemento in id_elements:
        reserva = get_object_or_404(Reserva, pk=id_elemento)
        reserva.estado_reserva = Reserva.ESTADO_CHOICES[2][0]
        reserva.save()
    response = redirect('landingAdmin')
    response['Location'] += '?tab=reservas'
    return response


def borrarPrestamo(request):
    id_prestamo =request.POST["identificador"]
    prestamo= get_object_or_404(Prestamo,pk=id_prestamo)
    prestamo.delete()
    response = redirect('landingAdmin')
    response['Location'] += '?tab=prestamos'
    return response


def borrarUsuario(request):
    rut_usuario =request.POST["identificador"]
    profile = get_object_or_404(Profile, rut=rut_usuario)
    profile.delete()
    response = redirect('landingAdmin')
    response['Location'] += '?tab=usuarios'
    return response


def borrarEspacio(request):
    id_espacio =request.POST["identificador"]
    espacio= get_object_or_404(Espacio,pk=id_espacio)
    espacio.delete()
    response = redirect('landingAdmin')
    response['Location'] += '?tab=espacios'
    return response


def borrarArticulo(request):
    id_articulo =request.POST["identificador"]
    articulo= get_object_or_404(Articulo,pk=id_articulo)
    articulo.delete()
    response = redirect('landingAdmin')
    response['Location'] += '?tab=articulos'
    return response


def borrarReserva(request):
    id_reserva =request.POST["identificador"]
    reserva= get_object_or_404(Reserva,pk=id_reserva)
    reserva.delete()
    response = redirect('landingAdmin')
    response['Location'] += '?tab=reservas'
    return response


def verPrestamo(request):
    id_prestamo = request.POST["identificador"]
    prest = get_object_or_404(Prestamo, pk=id_prestamo)
    return HttpResponse("Redirigir a ficha de prestamo: " + str(prest.id))
    # renderear ficha
    # return redirect('inventario:landingAdmin')


def crearPrestamo(request):
    return redirect('landingAdmin')
