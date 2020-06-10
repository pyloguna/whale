from flask_login import UserMixin

from db import get_db


class CredentialManager:
    # autentica un usuario
    @staticmethod
    def auth(user, password=None, auth_type="basic"):
        db = get_db()
        if auth_type == "basic":  # verificacion sencilla, no hace hashing de contraseñas
            user = db.execute(
                "SELECT * FROM credenciales WHERE id = ?", (user.id,)
            ).fetchone()
            if user:
                return user[1] == password
        return False




