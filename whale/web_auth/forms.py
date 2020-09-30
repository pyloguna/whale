from django import forms

CAMPOS_LOGIN_MAPEO = {
    'password': 'pass'
}


class BasicLoginForm(forms.Form):
    usuario = forms.CharField()
    password = forms.CharField()

    def add_prefix(self, field_name):
        field_name = CAMPOS_LOGIN_MAPEO.get(field_name, field_name)
        return super(BasicLoginForm, self).add_prefix(field_name)


class RegistroForm(forms.Form):
    usuario = forms.CharField()
    correo = forms.EmailField()
    nombre = forms.CharField()
    password = forms.CharField()

    def add_prefix(self, field_name):
        field_name = CAMPOS_LOGIN_MAPEO.get(field_name, field_name)
        return super(RegistroForm, self).add_prefix(field_name)


class AgregarOTPDeviceForm(forms.Form):
    otp_name = forms.CharField()
