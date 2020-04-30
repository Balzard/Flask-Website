from app import app
from app.forms import*
from app.models import*
from app import db
from werkzeug.urls import url_parse

from flask import render_template, redirect
from flask import url_for, flash, request

from flask_login import login_required, login_user, logout_user, current_user, LoginManager

####################
# Public section   #
####################

# Home page
@app.route("/")
def home():
    pass

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

#####################
# Users section     #
#####################

# players list page
@app.route("/players")
def players():
    pass

# teams page
@app.route("/teams")
def teams():
    pass

# ...

######################
# Admins section     #
######################

# Add player
@app.route("/addPlayer")
def addPlayer():
    pass

# ...
