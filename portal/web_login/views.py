from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import BasicLoginForm, RegistroForm


class InicioView(TemplateView):
    template_name = "web_login/inicio.html"

@login_required
class DashBoardView(TemplateView):
    template_name = "web_login/dashboard.html"

class BasicLoginView(TemplateView):
    template_name = "web_login/login.html"

    def post(self, request):
        form = BasicLoginForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get("usuario")
            password = form.cleaned_data.get("password")
            creds = authenticate(request, username = usuario, password = password)
            if creds:
                login(request, creds)
                return redirect(reverse('web_login:dashboard'))
        return redirect(reverse('web_login:login'))

class RegistroView(View):
    def registrar(self, usuario, correo, nombre, password):
        if not User.objects.filter(username=usuario).exists():
            usuario = User.objects.create_user(usuario, correo, password)
            usuario.first_name = nombre
            usuario.save()
            return True
        return False

    def post(self, request):
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get("usuario")
            correo = form.cleaned_data.get("correo")
            nombre = form.cleaned_data.get("nombre")
            password = form.cleaned_data.get("password")
            if self.registrar(usuario,correo,nombre,password):
                return redirect('web_login:login')
        return redirect('web_login:login')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('web_login:inicio'))