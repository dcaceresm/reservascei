from time import strftime

from datetime import date, timedelta
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import *


# variables globales


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def anteriorSemana(request):
    # today = date.today()
    global today
    global semana
    weekday = today.weekday()
    week = []

    today = today - timedelta(days=weekday)
    today = today + timedelta(days=semana * 7)
    today = today - timedelta(days=7)

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

    for i in range(hours):
        for j in range(days):

            if j == 0:
                matrix[i][j] = (str(ini_time) + ":00")
            if j != 0:
                for element in prestamos:

                    if (element.fh_ini_prestamo.day == weekStart.day + j - 1) & (element.tipo_objeto == "espacio"):
                        condIni = element.fh_ini_prestamo.hour - 3 <= ini_time & ini_time < element.fh_fin_prestamo.hour - 3
                        if (condIni):
                            matrix[i][j] = element

        ini_time += 1

    return render(request, 'inventarioCEI/calendario.html',
                  {'Mon': week[0], 'Tue': week[1], 'Wed': week[2], 'Thu': week[3], 'Fri': week[4], 'month': month,
                   'prestamos': prestamos, 'matrix': matrix})


def anteriorMes(request):
    global today
    global semana
    weekday = today.weekday()
    week = []

    today = today - timedelta(days=weekday)
    today = today + timedelta(days=semana * 7)
    today = today - timedelta(weeks=4)
    day = today.day

    #for i in range(day, day + 7):
    #    week.append(i)

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

    for i in range(hours):
        for j in range(days):

            if j == 0:
                matrix[i][j] = (str(ini_time) + ":00")
            if j != 0:
                for element in prestamos:

                    if (element.fh_ini_prestamo.day == weekStart.day + j - 1) & (element.tipo_objeto == "espacio"):
                        condIni = element.fh_ini_prestamo.hour - 3 <= ini_time & ini_time < element.fh_fin_prestamo.hour - 3
                        if (condIni):
                            matrix[i][j] = element

        ini_time += 1

    return render(request, 'inventarioCEI/calendario.html',
                  {'Mon': week[0], 'Tue': week[1], 'Wed': week[2], 'Thu': week[3], 'Fri': week[4], 'month': month,
                   'prestamos': prestamos, 'matrix': matrix})


def siguienteSemana(request):
    # today = date.today()
    global today
    global semana
    weekday = today.weekday()
    week = []

    today = today - timedelta(days=weekday)
    today = today + timedelta(days=semana * 7)
    today = today + timedelta(days=7)

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

    for i in range(hours):
        for j in range(days):

            if j == 0:
                matrix[i][j] = (str(ini_time) + ":00")
            if j != 0:
                for element in prestamos:

                    if (element.fh_ini_prestamo.day == weekStart.day + j - 1) & (element.tipo_objeto == "espacio"):
                        condIni = element.fh_ini_prestamo.hour - 3 <= ini_time & ini_time < element.fh_fin_prestamo.hour - 3
                        if (condIni):
                            matrix[i][j] = element

        ini_time += 1

    return render(request, 'inventarioCEI/calendario.html',
                  {'Mon': week[0], 'Tue': week[1], 'Wed': week[2], 'Thu': week[3], 'Fri': week[4], 'month': month,
                   'prestamos': prestamos, 'matrix': matrix})


def siguienteMes(request):
    global today
    global semana
    weekday = today.weekday()
    week = []

    today = today - timedelta(days=weekday)
    today = today + timedelta(days=semana * 7)
    today = today + timedelta(weeks=4)
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

    for i in range(hours):
        for j in range(days):

            if j == 0:
                matrix[i][j] = (str(ini_time) + ":00")
            if j != 0:
                for element in prestamos:

                    if (element.fh_ini_prestamo.day == weekStart.day + j - 1) & (element.tipo_objeto == "espacio"):
                        condIni = element.fh_ini_prestamo.hour - 3 <= ini_time & ini_time < element.fh_fin_prestamo.hour - 3
                        if (condIni):
                            matrix[i][j] = element

        ini_time += 1

    return render(request, 'inventarioCEI/calendario.html',
                  {'Mon': week[0], 'Tue': week[1], 'Wed': week[2], 'Thu': week[3], 'Fri': week[4], 'month': month,
                   'prestamos': prestamos, 'matrix': matrix})


def calendar(request, tipo=0):
    # CORREGIR! SALE 32

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
                  {'Mon': week[0], 'Tue': week[1], 'Wed': week[2], 'Thu': week[3], 'Fri': week[4], 'month': month,
                   'prestamos': prestamos, 'matrix': matrix})


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
