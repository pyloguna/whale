from django import forms

class BasicLoginForm(forms.Form):
    correo = forms.EmailField()
    password = forms.CharField()

class RegistroForm(forms.Form):
    usuario = forms.CharField()
    correo = forms.EmailField()
    nombre = forms.CharField()
    password = forms.CharField()