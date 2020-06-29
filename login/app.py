# Python standard libraries
import json
import os
import sqlite3
import qrcode
import io

# Third party libraries
from flask import (
    Flask,
    redirect,
    request,
    url_for,
    render_template,
    send_file,
    session
)
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user
)

from oauthlib.oauth2 import WebApplicationClient
import requests

# Internal imports
from db import init_db_command
from user import User
from credential_manager import CredentialManager

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
dominio = os.environ.get("app_domain", "")


# Flask app setup
app = Flask(__name__,
            template_folder="web/template",
            static_url_path="",
            static_folder="web/static"

            )
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized():
    return "You must be logged in to access this content.", 403


# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

# OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template( "dashboard.html",
                                nombre=current_user.name,
                                correo=current_user.email,
                                imagen=current_user.profile_pic
                               )
    else:
        return render_template("login.html")


@app.route("/google-login")
def google_login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login", methods=["POST"])
def auth_callback():
    correo = request.form.get("usuario")
    password = request.form.get("pass")
    user = User.get(correo)
    if user and CredentialManager.auth(user, password=password):
        login_user(user, remember=True)
    return redirect(url_for("index"))

@app.route("/login/otp/<string:usuario>/<string:otp>")
def auth_otp_callback(usuario, otp):
    user = User.get(usuario)
    if user and CredentialManager.auth(user, otp=otp, auth_type="otp"):
        login_user(user, remember=True)
    return redirect(url_for("index"))

@app.route("/google-login/callback")
def gauth_callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in our db with the information provided
    # by Google
    # Doesn't exist? Add to database
    if not User.get(unique_id, auth_type="gauth"):
        User.create(unique_id, users_name, users_email, picture, auth_type="gauth")
    user = User.get(unique_id, auth_type="gauth")

    # Begin user session by logging the user in
    login_user(user, remember=True)

    # Send user back to homepage
    return redirect(url_for("index"))

@app.route("/registro", methods=["POST"])
def registro():
    correo = request.form.get("usuario")
    password = request.form.get("pass")
    nombre = request.form.get("nombre")
    if not User.get(correo):
        User.create(correo, nombre, correo, "")

    return render_template("login.html",
        correo = correo,
        password = password,
        nombre = nombre
    )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route('/qr')
@login_required
def qr():
    otp_code = CredentialManager.get_otp(current_user)
    qr_gen = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4)
    qr_gen.add_data("https://" + dominio + "/login/otp/"+current_user.id+"/" + otp_code.now())
    qr_gen.make(fit=True)
    qr_img = qr_gen.make_image()
    img = io.BytesIO()
    qr_img.save(img, format="PNG")
    img.seek(0)

    return send_file(img, mimetype="image/png")



if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 443, ssl_context="adhoc", debug=True)
