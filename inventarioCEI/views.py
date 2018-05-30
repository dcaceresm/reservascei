from time import strftime

from datetime import date, timedelta
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import *


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

"""def dateChange(date, cant, anterior, signo):
    months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    val = 0

    if cant == 1:
        val = -4
    elif cant == 2:
        val = -1
    elif cant == 3:
        val = 1
    elif cant == 4:
        val = 4

    day = date.day

    return date.replace(day=day + (val + anterior)*7)#+ (val + anterior)*7)"""

def calendar(request):
    #signo 1 positivo 0 negativo
    # fechas de prestamos se guardan f = datetime.datetime(2018, 5, 7, 15, 0, tzinfo=<UTC>) año mes día hora y min en utc
    # f.year =2018
    # d = date.today()
    # d.weekday() = 0 -> lunes

    #TIMEDELTA

    today = date.today()
    #today = dateChange(today, cant, anterior, signo)
    day = today.day
    weekday = today.weekday()
    week = []

    today = today - timedelta(days = weekday)
    day = today.day

    #for i in range(day - weekday, day - weekday + 7):
    #    week.append(i)

    #for i in range(0, weekday + 1):
    #    today = today - timedelta(days = 1)

    for i in range(day, day + 7):
        week.append(i)


    weekStart = today
    weekEnd = today + timedelta(days=6)

    #weekStart = today.replace(day=day - weekday)
    #weekEnd = today.replace(day=day + 6 - weekday)

    month = [weekStart, weekEnd]
    days = 5
    hours = 9

    times = ["9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]
    matrix = [[0 for x in range(days+1)] for y in range(hours)]

    ini_time = 9;
    end_time = 6;

    prestamos = Prestamo.objects.filter(fh_ini_prestamo__range=[weekStart, weekEnd]) | Prestamo.objects.filter(
        fh_fin_prestamo__range=[weekStart, weekEnd])

    for i in range(hours):
        for j in range(days):

            if j == 0:
               matrix[i][j] = (str(ini_time) + ":00")
            if j!=0:
                for element in prestamos:

                    if (element.fh_ini_prestamo.day == weekStart.day + j-1) & (element.tipo_objeto == "espacio"):
                        condIni = element.fh_ini_prestamo.hour-3 <= ini_time & ini_time < element.fh_fin_prestamo.hour-3
                        if(condIni):
                            matrix[i][j] = element

        ini_time += 1

    return render(request, 'inventarioCEI/calendario.html', {'Mon': week[0], 'Tue': week[1],'Wed': week[2],'Thu': week[3],'Fri': week[4], 'month': month, 'prestamos': prestamos, 'matrix': matrix})
    #return render(request, 'inventarioCEI/calendario.html', {'Mon': week[0], 'Tue': week[1], 'Wed': week[2], 'Thu': week[3], 'Fri': week[4]})

def buscar(request):
    if request.method == "POST":
        busqueda = request.POST['elemento']
        lista = Articulo.objects.filter(lista_tags__contains=busqueda)
        return render(request, 'inventarioCEI/buscar.html', {'lista': lista})
    else:
        lista = []
        return render(request, 'inventarioCEI/buscar.html', {'lista': lista})


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
