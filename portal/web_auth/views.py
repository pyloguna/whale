from django.http import HttpResponseServerError
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import BasicLoginForm, RegistroForm, AgregarOTPDeviceForm
from .models import OTPDevice
import json


class InicioView(TemplateView):
    template_name = "web_auth/inicio.html"


class DashBoardView(LoginRequiredMixin, TemplateView):
    template_name = "web_auth/dashboard.html"


class BasicLoginView(TemplateView):
    template_name = "web_auth/login.html"

    def post(self, request):
        form = BasicLoginForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get("usuario")
            password = form.cleaned_data.get("password")
            credentials = authenticate(request, username=usuario, password=password)
            if credentials:
                login(request, credentials)
                return redirect(reverse('web_auth:dashboard'))
        return redirect(reverse('web_auth:login'))


class OTPLoginView(View):
    def post(self, request):
        json_data = json.loads(request.body)
        try:
            credentials = authenticate(request, email=json_data['email'], challenge=json_data['challenge'])
            if credentials:
                login(request, credentials)
                return redirect(reverse('web_auth:dashboard'))
        except KeyError:
            HttpResponseServerError("Información Malformada")


class OTPAddDeviceView(LoginRequiredMixin, View):
    def post(self, request):
        form = AgregarOTPDeviceForm(request.POST)
        if form.is_valid():
            otp_name = form.cleaned_data.get("otp_name")
            if not OTPDevice.objects.filter(name=otp_name).exists():
                otp_device = OTPDevice.create(user=request.user.id, name=otp_name)
                otp_device.save()
        return redirect('web_auth:dashboard')

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
            if self.registrar(usuario, correo, nombre, password):
                return redirect('web_auth:login')
        return redirect('web_auth:login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('web_auth:inicio'))
