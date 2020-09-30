import io

from PIL import Image
from django.http import HttpResponseServerError, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import BasicLoginForm, RegistroForm, AgregarOTPDeviceForm
from .models import OTPDevice
import qrcode
import base64


def gen_qr_code(string):
    qr_gen = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4)
    qr_gen.add_data(string)
    qr_gen.make(fit=True)
    qr_img = qr_gen.make_image()
    img = io.BytesIO()
    qr_img.save(img, format="PNG")
    img.seek(0)
    return img


class InicioView(TemplateView):
    template_name = "web_auth/inicio.html"


class DashBoardView(LoginRequiredMixin, TemplateView):
    template_name = "web_auth/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['otp_devices'] = OTPDevice.objects.filter(user=self.request.user.id)
        return context


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
    def get(self, request, payload):
        payload = base64.decodebytes(payload.encode('utf-8')).decode('utf-8').split(':')
        try:
            credentials = authenticate(request, username=payload[0], challenge=payload[1])
            if credentials:
                login(request, credentials)
                return redirect(reverse('web_auth:dashboard'))
        except KeyError:
            HttpResponseServerError("Información Malformada")


class OTPManageDeviceView(LoginRequiredMixin, View):
    def post(self, request):
        form = AgregarOTPDeviceForm(request.POST)
        if form.is_valid():
            otp_name = form.cleaned_data.get("otp_name")
            if not OTPDevice.objects.filter(name=otp_name).exists():
                otp_device = OTPDevice.create(user=self.request.user.id, name=otp_name)
                otp_device.save()
        return redirect('web_auth:dashboard')


class OTPDeleteDeviceView(LoginRequiredMixin, View):
    def post(self, request, otp_device):
        otp_device = OTPDevice.objects.get(user=self.request.user.id, name=otp_device)
        if otp_device is not None:
            otp_device.delete()
            return redirect('web_auth:dashboard')


class OTPDeviceSecretView(LoginRequiredMixin, View):
    def get(self, request, otp_device):
        otp_device = OTPDevice.objects.get(user=self.request.user.id, name=otp_device)
        if otp_device is not None:
            otp_secret = otp_device.get_sync_code(self.request.user.email, request.META['HTTP_HOST'])
            img = gen_qr_code(otp_secret)
            return HttpResponse(img.read(), content_type="image/png")
        error_img = Image.new('RGBA', (1, 1), (0, 0, 0, 255))
        response = HttpResponse(content_type="image/png")
        error_img.save(response, "PNG")
        return response


class OTPLoginCodeView(LoginRequiredMixin, View):
    def get(self, request, otp_device):
        otp_device = OTPDevice.objects.get(user=self.request.user.id, name=otp_device)
        if otp_device is not None:
            otp_code = otp_device.gen_otp_code()
            payload = base64.urlsafe_b64encode(f"{self.request.user.username}:{otp_code}"
                                               .encode('utf-8')).decode('utf-8')
            ruta = f"http{'s' if request.is_secure() else ''}://{request.META['HTTP_HOST']}/login/qrauth/"
            ruta += payload
            img = gen_qr_code(ruta)
            return HttpResponse(img.read(), content_type="image/png")
        error_img = Image.new('RGBA', (1, 1), (0, 0, 0, 255))
        response = HttpResponse(content_type="image/png")
        error_img.save(response, "PNG")
        return response


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
