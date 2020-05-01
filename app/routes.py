from asyncio import tasks

from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app.forms import MyLoginForm
from app.forms import MyRegistrationForm
from app.models import Joueur
from werkzeug.urls import url_parse
from flask_login import login_required, login_user, logout_user, current_user, LoginManager

from flask_login import login_required, login_user,logout_user, current_user


#Home page
@app.route('/')
def home():
    return render_template('home.html')

# Contact page
@app.route("/contact")
def contact():
    pass

# Training page + tarif
@app.route("/training")
def training():
    pass

# Carnet d'or page

@app.route("/goldCarnet")
def goldCarnet():
    pass

# Material page
@app.route("/material")
def material():
    pass

# Comité page
@app.route("/committee")
def committee():
    pass

# Inscription page (inscription au club)
# Ajout dans la bd et utilisation de formulaire
@app.route("/inscription")
def inscription():
    pass

# Registration page
@app.route("/registration")
def registration():
    pass

# Login page
@app.route("/login")
def login():
    pass
