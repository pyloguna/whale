from flask_login import UserMixin

from db import get_db
import pyotp

class CredentialManager:
    # autentica un usuario
    @staticmethod
    def auth(user, password=None, otp=None, auth_type="basic"):
        db = get_db()
        if auth_type == "basic":  # verificacion sencilla, no hace hashing de contraseñas
            user = db.execute(
                "SELECT * FROM credenciales WHERE id = ?", (user.id,)
            ).fetchone()
            if user:
                return user[1] == password
        elif auth_type == "otp":
            user = db.execute(''
                "SELECT * FROM credenciales WHERE id = ?", (user.id,)
            ).fetchone()
            if user:
                otpkey = user[2]
                totp = pyotp.TOTP(otpkey)
                tnow = totp.now()
                return totp.verify(otp)
        return False

    # retorna el secreto otp del usuario
    @staticmethod
    def get_otp_secret(user):
        db = get_db()
        user = db.execute(
            "SELECT * FROM credenciales WHERE id = ?", (user.id,)
        ).fetchone()
        if user:
            otp_key = user[3]
            return otp_key
        return None

    # retorna una clave otp
    @staticmethod
    def get_otp(user):
        db = get_db()
        user = db.execute(
            "SELECT * FROM credenciales WHERE id = ?", (user.id,)
        ).fetchone()
        if user:
            otp_key = user[2]
            totp = pyotp.TOTP(otp_key)
            return totp
        return None



