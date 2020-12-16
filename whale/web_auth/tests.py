from django.test import TestCase, Client
from .models import OTPDevice
from django.contrib.auth.models import User

# Create your tests here.


class OTPDeviceTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        user = User.objects.create_user('testuser','test@domain.tld', '$Test1234')
        user.first_name = 'Jhon'
        user.last_name = 'Doe'
        user.save()
        otp_device = OTPDevice.create(user.id, name='otp_test_device')
        otp_device.save()
        return super().setUpTestData()

    def test_otp_login(self):
        print("--- Test OTP Login device ---")
        user = User.objects.filter(username= 'testuser')[0]
        otp_device = OTPDevice.objects.filter(user = user)[0]
        otp_code = otp_device.gen_otp_code()
        client = Client()
        logged_in = client.login(username = user, challenge=otp_code)
        self.assertTrue(logged_in)
