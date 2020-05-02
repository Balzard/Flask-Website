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
@app.route("/")
def home():
    return render_template("home.html")

# Contact page
@app.route("/contact")
def contact():
    #return render_template("contact.html")
    return "Page des contacts du club."

# Training page + tarif
@app.route("/training")
def training():
    #trainings = Entrainement.query.all()
    #return render_template("training.html", trainings=trainings)
    return "Page pour les entrainements"

# Carnet d'or page
@app.route("/goldCarnet")
def goldCarnet():
    comms = Commentaire.query.all()
    #return render_template("goldCarnet.html", comms=comms)
    return "Page du carnet d'or"

# Materiel page
@app.route("/materiel")
def material():
    #matos = Materiel.query.all()
    #return render_template("materiel.html", matos=matos)
    return "Page du matériel"

# Inscription page (inscription au club)
# Ajout dans la bd et utilisation de formulaire
@app.route("/inscription", methods=["GET","POST"])
def inscription():
    form = MyRegistrationForm()
    if form.validate_on_submit():
        # Take data back
        username = form.username.data
        firstName = form.firstname.data
        lastName = form.lastname.data
        birthDate = form.date.data
        password = form.password2.data
        # Create new Joueur
        player = Joueur(pseudo=username,mdp=password,nom=lastName,prenom=firstName,naissance=birthDate,admin=False)
        player.set_password(password)
        # Add player to the db
        db.session.add(player)
        db.session.commit()
        # Home page
        return redirect(url_for("home"))
    else:
        return render_template("my_registration_form.html", form=form)

# Login page
@app.route("/login",methods=["GET","POST"])
def login():
    form = MyLoginForm()
    if form.validate_on_submit():
        player = Joueur.query.filter_by(pseudo=form.username.data).first()
        if player is None:
            flash("You're not registered yet.", "info")
            return redirect(url_for("login"))
        elif not player.check_password(form.password.data):
            flash("Invalid username or password.", "info")
            return redirect(url_for("login"))
        login_user(player)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != " ":
            next_page = url_for("home")
        return redirect(next_page)
    else:
        return render_template("my_login_form.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# liste de force
@app.route("/players")
@login_required
def players():
    #players = Joueur.query.all()
    #return render_template("listPlayer.html",players=players)
    return "Page des joueurs"
