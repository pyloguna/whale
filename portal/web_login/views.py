from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView

class InicioView(TemplateView):
    template_name = "web login/inicio.html"