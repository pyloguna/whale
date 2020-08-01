from django.shortcuts import render, redirect
from django.views import generic, TemplateView

class InicioView(TemplateView):
    template_name = "web_login/inicio.html"