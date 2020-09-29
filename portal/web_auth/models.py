import pyotp
from django.conf import settings
from django.db import models


class OTPDevice(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    otp_key = models.CharField(max_length=16)
    name = models.CharField(max_length=100)

    def is_valid_code(self, challenge):
        totp = pyotp.TOTP(self.otp_key)
        return totp.verify(challenge)

    def get_otp_sync(self, service_domain=''):
        otp_secret = self.otp_key
        return pyotp.TOTP(otp_secret).provisioning_uri(self.name.__str__(), issuer_name=service_domain)

    def gen_otp_code(self):
        return pyotp.TOTP(self.otp_key)

    def __str__(self):
        return f"{self.user}: {self.name}"

    @classmethod
    def create(cls, user, name):
        otp_device = cls(
            user_id=user,
            otp_key=pyotp.random_base32(),
            name=name
        )
        return otp_device

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'],
                name='otp_device_name_unique'
            )
        ]
