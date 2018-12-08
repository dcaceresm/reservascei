from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Articulo, Reserva, Prestamo
import datetime
from T3_INGSW import settings
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.db.models import Q
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


class SimpleAdmin(TemplateView):
    template_name = "simpleAdmin/landingAdminSimple.html"
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.isAdmin:
                return super(SimpleAdmin, self).get(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('buscar'))
        else:
            return redirect('/')


    def get_context_data(self, **kwargs):
        dt_today = datetime.datetime.now()
        dt_today_ini = dt_today.replace(hour=9, minute=0, second=0, microsecond=0)
        dt_today_ter = dt_today.replace(hour=18, minute=0, second=0, microsecond=0)
        dt_ayer = dt_today_ter - datetime.timedelta(days=1)
        context = super(SimpleAdmin, self).get_context_data(**kwargs)
        context['reservas_hoy'] = Reserva.objects.filter(estado_reserva = 'P', fh_ini_reserva__gte=dt_today_ini, fh_fin_reserva__lte=dt_today_ter)
        context['prestamos_hoy'] = Prestamo.objects.filter(fh_ini_prestamo__gte=dt_today_ini, fh_fin_prestamo__lte=dt_today_ter, estado_prestamo='V')
        context['prestamos_hoy_recibidos'] = Prestamo.objects.filter(fh_ini_prestamo__gte=dt_today_ini, fh_fin_prestamo__lte=dt_today_ter, estado_prestamo='R')
        context['prestamos_hoy_perdidos'] = Prestamo.objects.filter(fh_ini_prestamo__gte=dt_today_ini, fh_fin_prestamo__lte=dt_today_ter, estado_prestamo='P')
        context['prestamos_no_recibidos'] = Prestamo.objects.filter(fh_fin_prestamo__lte=dt_ayer, estado_prestamo='V')

        return context

def simpleAdminAction(request):
    if request.method=='POST':
        r_or_p = request.POST['rp']
        to_modify = request.POST.getlist('checked')
        act = request.POST['action']

        if r_or_p == 'r':
            dict_action = {'A': 1, 'R':2}
            for reservation_id in to_modify:
                reserva = Reserva.objects.get(pk=reservation_id)
                reserva.estado_reserva = Reserva.ESTADO_CHOICES[dict_action[act]][0]
                reserva.save()
                if act == 'A':

                    nuevo_prestamo = Prestamo.objects.create(profile=reserva.profile,fh_ini_prestamo=reserva.fh_ini_reserva,
                                                     fh_fin_prestamo=reserva.fh_fin_reserva, estado_prestamo='V')
                    if reserva.tipo == 'A':
                        nuevo_prestamo.tipo = 'A'
                        rels = reserva.related.filter(Model=InstanciaArticulo)
                    else:
                        nuevo_prestamo.tipo = 'E'
                        rels = reserva.related.filter(Model=Espacio)
                    for rel in rels:
                        nuevo_prestamo.related.add(rel)
                    nuevo_prestamo.save()
            return HttpResponseRedirect(reverse('simpleAdmin'))

        elif r_or_p == 'p':
            dict_action = {'A': 3, 'R':2}
            for prestamo_id in to_modify:
                prestamo = Prestamo.objects.get(pk=prestamo_id)
                prestamo.estado_prestamo = Prestamo.ESTADO_CHOICES[dict_action[act]][0]
                prestamo.save()
            return HttpResponseRedirect(reverse('simpleAdmin'))





def ficha(request, id):
    if request.user.is_authenticated:

        try:  # IF ITEM ID EXISTS
            obj = Articulo.objects.get(pk=id)

            # GET LASTEST RESERVATIONS
            instancias = InstanciaArticulo.objects.filter(articulo=obj)

            #Dado el cambio para aceptar múltiples objetos al mismo tiempo
            #Ahora hay que hacer la consulta manualmente :(
            all_reservas = Reserva.objects.filter(tipo='A').order_by('-pk')
            reservas = list()
            count = 0
            #Obtiene las primeras 10 reservas asociadas al articulo
            for r in all_reservas:
                if (count==10): break
                if r.related.first().articulo == obj:
                    reservas.append(r)
                    count += 1

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
        except Exception as e:
            print(e)
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
        libres = list(map(int, request.POST['libres'].split(',')))
        cantidad = int(request.POST['qty-select'])
        raw_fecha = request.POST['fecha']
        raw_h_ini = request.POST['hinicio']
        raw_h_ter = request.POST['htermino']

        # armar datetime de inicio y fin
        fecha = datetime.datetime.strptime(raw_fecha, "%d/%m/%Y")
        h_ini = datetime.datetime.strptime(raw_h_ini,"%I:%M %p")
        h_ter = datetime.datetime.strptime(raw_h_ter,"%I:%M %p")
        dt_ini=datetime.datetime.combine(fecha.date(),h_ini.time())
        dt_ter=datetime.datetime.combine(fecha.date(),h_ter.time())
        fh_reserva = datetime.datetime.now()
        #OBTENER LAS INSTANCIAS
        instancias = InstanciaArticulo.objects.filter(articulo = articulo, num_articulo__in=libres)[:cantidad]
        #GENERAR LA RESERVA
        r = Reserva.objects.create(profile = request.user.profile, fh_reserva=fh_reserva,
                                    fh_ini_reserva=dt_ini, fh_fin_reserva=dt_ter,tipo='A')
        for i in instancias:
            r.related.add(i)

        r.save()
        return redirect('/profile')
    else:
        return HttpResponse("Whoops!")


def index(request):
    # Envia a la pagina de inicio
    # Dependiendo si es admin o no

    if (request.user.is_authenticated):
        if request.user.profile.isAdmin:
            return HttpResponseRedirect(reverse('simpleAdmin'))
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
    username = get_user(email)
    print(username)
    if username is not None:
        print(username.username)
        user = authenticate(username=username.username, password=password)
        print(user)
        if user.is_active:
            login(request, user)

            # Redirigirlo si es admin o no
            if user.profile.isAdmin:
                return HttpResponseRedirect(reverse('simpleAdmin'))
            else:
                return HttpResponseRedirect(reverse('buscar'))
        else:

            # Validador
            messages.error(request, 'Correo y/o Contraseña incorrectos')
            return HttpResponseRedirect(reverse('index'))
    else:
        messages.error(request, 'Correo y/o Contraseña incorrectos')
        return HttpResponseRedirect(reverse('index'))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


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
        name = (Espacio.objects.get(id=event.related.first().pk)).nombre + "-" + event.estado_prestamo
    else:
        name = (Espacio.objects.get(id=event.related.first().pk)).nombre + "-" + event.estado_reserva

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
        if request.user.profile.isAdmin:
            return redirect('/')
        else:

            events = []
            prestamos = Prestamo.objects.all()

            reservas = Reserva.objects.all()

            for p in prestamos:
                if p.tipo == 'E':
                    di = p.fh_ini_prestamo
                    df = p.fh_fin_prestamo
                    event_json = event_adding(p, di, df, 1)
                    events.append(event_json)

            for r in reservas:
                if r.tipo == 'E':
                    di = r.fh_ini_reserva
                    df = r.fh_fin_reserva
                    event_json = event_adding(r, di, df, 2)
                    events.append(event_json)

            events_string = json.dumps(events)

            return render(request, 'calendario.html', {'events': events_string})
    else:  # USER IS NOT LOGGED IN
        return redirect('/')  # REDIRECT TO INDEX (LOGIN) PAGE


# buscar: retorna una lista con los articulos que concuerdan con la busqueda
def buscar(request):
    if request.user.is_authenticated:
        if request.user.profile.isAdmin:
            return redirect('/')
        else:
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
        if request.user.profile.isAdmin:
            return redirect('/')
        else:
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

            prestamos = Prestamo.objects.filter(tipo='E')

            reservas = Reserva.objects.filter(tipo='E')

            for event in prestamos:
                di = event.fh_ini_prestamo
                df = event.fh_fin_prestamo
                event_json = event_adding(event, di, df, 1)
                events.append(event_json)

            for event in reservas:
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



def ajax_check_free_spaces(request):
    dt_ini = datetime.datetime.strptime(request.GET.get('f_ini', None),"%Y-%m-%dT%H:%M:%S")
    dt_ter = datetime.datetime.strptime(request.GET.get('f_ter', None),"%Y-%m-%dT%H:%M:%S")
    all_res = Reserva.objects.filter(Q(fh_ini_reserva__lte=dt_ini,
                                      fh_fin_reserva__gte=dt_ini) | Q(fh_ini_reserva__gte=dt_ini,
                                                                      fh_fin_reserva__lte=dt_ter) | Q(fh_ini_reserva__lte=dt_ter,
                                                                      fh_fin_reserva__gte=dt_ter) | Q(fh_ini_reserva__lte=dt_ini, fh_fin_reserva__gte=dt_ter),
                                                                      tipo='E')
    ocupados = set([r.related.first() for r in all_res])
    all_spaces = set(Espacio.objects.all())
    opciones = [[e.pk, e.nombre] for e in all_spaces-ocupados]
    print(opciones)

    return JsonResponse(list(opciones), safe=False)
def ajax_reservations_from_article(request, id):
    obj = Articulo.objects.get(pk=id)
    instancias = InstanciaArticulo.objects.filter(articulo=obj)
    inst_set = set(instancias.values_list("num_articulo", flat=True))
    # armar datetime inicio fin
    raw_fecha = request.GET.get('fecha', None)
    raw_h_ini = request.GET.get('h_ini', None)
    raw_h_ter = request.GET.get('h_ter', None)
    fecha = datetime.datetime.strptime(raw_fecha, "%d/%m/%Y")
    h_ini = datetime.datetime.strptime(raw_h_ini,"%I:%M %p")
    h_ter = datetime.datetime.strptime(raw_h_ter,"%I:%M %p")
    dt_ini=datetime.datetime.combine(fecha.date(),h_ini.time())
    dt_ter=datetime.datetime.combine(fecha.date(),h_ter.time())
    all_res = Reserva.objects.filter(Q(fh_ini_reserva__lte=dt_ini,
                                      fh_fin_reserva__gte=dt_ini) | Q(fh_ini_reserva__gte=dt_ini,
                                                                      fh_fin_reserva__lte=dt_ter) | Q(fh_ini_reserva__lte=dt_ter,
                                                                      fh_fin_reserva__gte=dt_ter) | Q(fh_ini_reserva__lte=dt_ini, fh_fin_reserva__gte=dt_ter),
                                                                      tipo='A')

    ocupados = set()
    for r in all_res:
        articulos = set([ia.num_articulo for ia in r.related.filter(Model=InstanciaArticulo)])
        ocupados = ocupados | articulos
    perdidos = set([ia.num_articulo for ia in InstanciaArticulo.objects.filter(Q(estado='En Reparación')|Q(estado='Perdido'))])
    print(perdidos)
    libres = list(inst_set - ocupados - perdidos)
    qty = list(range(1,len(libres)+1))
    context = { 'libres':libres, 'cantidades': qty }
    return JsonResponse(context, safe=False)
