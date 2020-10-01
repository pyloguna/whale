from django.urls import path

from . import views

app_name = "web_auth"
urlpatterns = [
    path('', views.InicioView.as_view(), name="inicio"),
    path('login', views.BasicLoginView.as_view(), name='login'),
    path('registro', views.RegistroView.as_view(), name='registro'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('dashboard', views.DashBoardView.as_view(), name='dashboard'),
    path('login/qrauth/<str:payload>', views.OTPLoginView.as_view(), name='otpLogin'),
    path('otp/devices/register', views.OTPManageDeviceView.as_view(), name='otpDeviceAdd'),
    path('otp/devices/<str:otp_device>/logincode', views.OTPLoginCodeView.as_view(), name='otpLoginCode'),
    path('otp/devices/<str:otp_device>/remove', views.OTPDeleteDeviceView.as_view(), name='otpDeviceRemove'),
    path('otp/devices/<str:otp_device>/sync', views.OTPDeviceSecretView.as_view(), name='otpSyncCode')
]
