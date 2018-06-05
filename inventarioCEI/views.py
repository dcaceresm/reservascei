from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .models import *
from django.urls import reverse
from .forms import SignUpForm

from pprint import pprint

def index(request):
    if (request.user.is_authenticated):
        return HttpResponseRedirect('profile')
    return render(request, 'custom_login.html')


def showProfile(request):
    if not (request.user.is_authenticated):
        return HttpResponseRedirect(reverse('index'))

    data = request.GET.get('pestana', "Reservas")

    if(data=="Reservas"):

        reservas = Reserva.objects.filter(profile__rut=request.user.profile.rut).order_by('-id')[:10]
        estados = Reserva.objects.filter(profile__rut=request.user.profile.rut).order_by('-id')\
                            .values_list('estado_reserva', flat=True)[:10]
        list= zip(reservas, estados)
        return render(request, 'user_profile.html', {'result': list})

    else:

        prestamos = Prestamo.objects.filter(profile__rut=request.user.profile.rut).order_by('-id')[:10]
        estados = Prestamo.objects.filter(profile__rut=request.user.profile.rut).order_by('-id') \
                             .values_list('estado_prestamo', flat=True)[:10]
        list = zip(prestamos, estados)
        return render(request, 'user_profile.html', {'result': list})



def get_user(email):
    try:
        return Profile.objects.get(mail=email.lower()).user
    except Profile.DoesNotExist:
        return None


def customlogin(request):
    email = request.POST['email']
    password = request.POST['password']
    username = get_user(email).username
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('profile'))
        else:
            return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('index'))


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.rut = form.cleaned_data.get('rut')
            user.profile.mail = form.cleaned_data.get('mail')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })

def deleteRes(request):
    delList = request.POST.getlist('element')

    pprint(delList)

    #espacios_por_borrar = Espacio.objects.filter(nombre__in=delList).values_list('id', flat=True)
    #articulos_por_borrar = Articulo.objects.filter(nombre__in=delList).values_list('id', flat=True)

    Reserva.objects.filter(id__in=delList).delete()
    #Reserva.objects.filter(object_id__in=articulos_por_borrar).delete()

    return HttpResponseRedirect(reverse('index'))