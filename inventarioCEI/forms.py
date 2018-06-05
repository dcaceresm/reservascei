from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        #fields = ('url', 'location', 'company')
        fields = ('rut', 'mail')


class SignUpForm(UserCreationForm):
    rut = forms.CharField(help_text='XX.XXX.XXX-X', required=True)
    mail = forms.EmailField(help_text='XXXXXX@XXXXX.XX', required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'rut', 'mail', 'first_name', 'last_name', 'password1', 'password2', )