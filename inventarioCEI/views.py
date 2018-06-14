from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .models import *
from django.urls import reverse

def index(request):
    if (request.user.is_authenticated):
        return HttpResponseRedirect('profile')
    return render(request, 'custom_login.html')


def showProfile(request):
    if not (request.user.is_authenticated):
        return HttpResponseRedirect(reverse('index'))
    reservas = Reserva.objects.filter(profile__rut=request.user.profile.rut).order_by('-id')[:10]
    prestamos = Prestamo.objects.filter(profile__rut=request.user.profile.rut).order_by('-id')[:10]
    return render(request, 'user_profile.html', {'reservas': reservas, 'prestamos': prestamos})

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
            messages.error(request, 'Correo y/o Contraseña incorrectos')
            return HttpResponseRedirect(reverse('index'))
    else:
        messages.error(request, 'Correo y/o Contraseña incorrectos')
        return HttpResponseRedirect(reverse('index'))


def signup(request):
    if request.method == "POST":
        rut = request.POST['rut']
        mail = request.POST['mail']
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        password = request.POST['password1']
        password2 = request.POST['password2']
        user = get_user(mail)
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
                return redirect('profile')
            else:
                return render(request, 'signup.html')
        else:
            messages.error(request,'Las contraseñas no coinciden')
            return render(request, 'signup.html')
    return render(request, 'signup.html')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Su clave fue cambiada exitosamente')
            return redirect('change_password')
        else:
            messages.error(request, 'No se pudo cambiar su clave. Verifique que la clave actual o que la clave nueva'
                                    ' y su repetición coincidan.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })

def deleteRes(request):
    delList = request.POST.getlist('element')
    Reserva.objects.filter(id__in=delList).delete()
    return HttpResponseRedirect(reverse('index'))