from asyncio import tasks

from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app.forms import MyLoginForm
from app.forms import MyRegistrationForm
from app.models import Joueur
from werkzeug.urls import url_parse
from flask_login import login_required, login_user, logout_user, current_user, LoginManager

from flask_login import login_required, login_user,logout_user, current_user



@app.route('/')
def main():
    return render_template('home.html')

