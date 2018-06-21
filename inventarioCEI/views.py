from time import strftime

from datetime import date, timedelta
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import *
import json


# variables globales


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


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
    """
    global today
    today = date.today()
    global semana
    semana = 0
    weekday = today.weekday()
    week = []

    today = today - timedelta(days=weekday)
    day = today.day
    dia = today

    for i in range(day, day + 7):
        day = dia.day
        week.append(day)
        dia = dia + timedelta(days=1)

    weekStart = today
    weekEnd = today + timedelta(days=6)

    month = [weekStart, weekEnd]
    days = 5
    hours = 9

    times = ["9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]
    matrix = [[0 for x in range(days + 1)] for y in range(hours)]

    ini_time = 9;
    end_time = 6;

    prestamos = Prestamo.objects.filter(fh_ini_prestamo__range=[weekStart, weekEnd]) | Prestamo.objects.filter(
        fh_fin_prestamo__range=[weekStart, weekEnd])

    ct = ContentType.objects.get_for_model(Espacio)
    
    for i in range(hours):
        for j in range(days):

            if j == 0:
                matrix[i][j] = (str(ini_time) + ":00")
            if j != 0:
                for element in prestamos:

                    if (element.fh_ini_prestamo.day == weekStart.day + j - 1) & (element.content_type == ct):
                        condIni = element.fh_ini_prestamo.hour - 3 <= ini_time & ini_time < element.fh_fin_prestamo.hour - 3
                        if (condIni):
                            matrix[i][j] = element

        ini_time += 1
    
    return render(request, 'inventarioCEI/calendario.html',
                  {'data_string': data_string, 'Mon': week[0], 'Tue': week[1], 'Wed': week[2], 'Thu': week[3], 'Fri': week[4], 'month': month,
                   'prestamos': prestamos, 'matrix': matrix})
    """

    events = [
        """{
            "title": 'event1',
            "start": '2018-06-06T09:30',
            "end": '2018-06-06T13:30:00'


        },
        {
            "title": 'event2',
            "start": '2018-06-10T12:30:00',
            "end": '2018-06-10T13:30:00'
        },
        {
            "title": 'event3',
            "start": '2010-01-09T12:30:00',
            "allDay": "false"
        }"""
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

    return render(request, 'inventarioCEI/calendario.html', {'events': events_string})


def buscar(request):
    if request.method == "POST":
        busqueda = request.POST['elemento']
        lista = Articulo.objects.filter(lista_tags__contains=busqueda)
        return render(request, 'inventarioCEI/buscar.html', {'lista': lista})
    else:
        lista = []
        return render(request, 'inventarioCEI/buscar.html', {'lista': lista})


def busquedaAvanzada(request):
    if request.method == "POST":
        busqueda = request.POST['elemento']
        estado = request.POST['estado']
        lista = Articulo.objects.filter(lista_tags__contains=busqueda)
        lista = lista.filter(estado__contains=estado)
        return render(request, 'inventarioCEI/busquedaAvanzada.html', {'lista': lista})
    else:
        lista = []
        return render(request, 'inventarioCEI/busquedaAvanzada.html', {'lista': lista})


def goToArticulos(request):
    if request.method == "POST":
        return redirect('buscar')
    else:
        return render(request, 'inventarioCEI/calendario.html')


def goToEspacios(request):
    if request.method == "POST":
        return redirect('calendar')
    else:
        return render(request, 'inventarioCEI/buscar.html')


class LandingAdmin(TemplateView):
    template_name = "inventarioCEI/landingPageAdmin.html"

    def get_context_data(self, **kwargs):
        return {}

        # para hacer calendario: tomar semana actual, ver de la lista de prestamos, cuales corresponden a la semana actual, darselos al hrml, este revisa cada grilla y ve si corresponde a la hora,
