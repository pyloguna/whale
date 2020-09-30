from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from . import models


class OTPAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, challenge=None):
        try:
            user = User.objects.get(username=username)
            if user is not None:
                otp_devices = models.OTPDevice.objects.filter(user=user.id)
                for otp_device in otp_devices:
                    if otp_device is not None and otp_device.is_valid_code(challenge):
                        return user
            return None
        except User.DoesNotExists:
            raise ValidationError("credenciales incorrectas")

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
