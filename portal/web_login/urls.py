from django.urls import path

from . import views

app_name = "login_web"
urlpatterns = [
    path('', views.InicioView.as_view(), name="inicio")
]
