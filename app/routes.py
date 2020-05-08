from app import app, db
from flask import render_template, redirect, url_for, flash, request
from flask import jsonify
from flask import json
from app.forms import*
from app.models import*
from werkzeug.urls import url_parse
from flask_login import login_required, login_user, logout_user, current_user, LoginManager
import datetime

from flask_login import login_required, login_user,logout_user, current_user

#create admin account
def create_players():
    user = Joueur(pseudo = "admin",prenom = "stephane", nom="leblanc",admin=True, naissance = datetime.date(1998,6,1), team=None)
    user.set_password("admin")
    equipe = Equipe.query.get("Equipe A")
    user2 = Joueur(pseudo="joueur", prenom="Sylvério", nom="Pool",admin=False, naissance=datetime.date(1998,8,27),team=equipe)
    user2.set_password("joueur")
    user3 = Joueur(pseudo="membre", prenom="Sindy", nom="Willems",admin=False, naissance=datetime.date(1997,3,21),team=equipe)
    user3.set_password("membre")
    db.session.add(user)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()

def createMatos():
    matos = Materiel(quantite=5, type="filet")
    matos2 = Materiel(quantite=4, type="table")
    db.session.add(matos)
    db.session.add(matos2)
    db.session.commit()

def createTeam():
    team = Equipe(nom="Equipe A")
    team2 = Equipe(nom="Equipe B")
    db.session.add(team)
    db.session.add(team2)
    db.session.commit()

def createComm():
    comm = Commentaire(texte="Comm1", auteur="anonyme", date=datetime.date.today())
    comm2 = Commentaire(texte="Comm2", auteur="anonyme", date=datetime.date.today())
    comm3 = Commentaire(texte="Comm3", auteur="joueur", date=datetime.date.today())
    db.session.add(comm)
    db.session.add(comm2)
    db.session.add(comm3)
    db.session.commit()

def createProduct():
    prod = Produit(nom="coca", quantite=25, type="soft", tarif=1.2)
    prod1 = Produit(nom="Paprika", quantite=10, type="chips", tarif=1.0)
    db.session.add(prod)
    db.session.add(prod1)
    db.session.commit()

createTeam()
create_players()
createMatos()
createComm()
createProduct()

####################
# Public section   #
####################

#Home page
@app.route("/")
def home():
    return render_template("home.html")

# Contact page
@app.route("/contact")
def contact():
    #return render_template("contact.html")
    return render_template("contacts.html")

# Training page + tarif
@app.route("/training")
def training():
    #trainings = Entrainement.query.all()
    #return render_template("training.html", trainings=trainings)
    return render_template("entrainements.html")

# Carnet d'or page
@app.route("/goldCarnet")
def goldCarnet():
    comms = Commentaire.query.all()
    list = []
    return render_template("carnet_or.html",comms=comms)

# Materiel page
@app.route("/materiel")
def materiel():
    #matos = Materiel.query.all()
    #return render_template("materiel.html", matos=matos)
    return render_template("materiel.html")

# Produit bar page
@app.route("/bar")
def bar():
    products = Produit.query.all()
    return render_template("bar.html", products=products)

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
        player = Joueur(pseudo=username,mdp=password,nom=lastName,prenom=firstName,naissance=birthDate,admin=False,team=None)
        player.set_password(password)
        # Add player to the db
        db.session.add(player)
        db.session.commit()
        # Login page
        return redirect(url_for("login"))
    else:
        return render_template("my_registration_form.html", form=form)

# Login page
@app.route("/login", methods=["GET","POST"])
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

# Ecrire un commentaire
@app.route("/comment", methods=["GET","POST"])
def comment():
    # Name
    if current_user.is_authenticated:
        pseudo = current_user.pseudo
    else:
        pseudo = "anonyme"
    # Get the message
    form = MyCommentForm()
    if form.validate_on_submit():
        txt = form.comm.data
        date = datetime.date.today()
        new_comm = Commentaire(texte=txt,auteur=pseudo,date=date)
        db.session.add(new_comm)
        db.session.commit()
        return redirect(url_for("goldCarnet"))
    else:
        return render_template("comment.html",form=form,pseudo=pseudo)

####################
# Player section   #
####################

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# liste de force
@app.route("/players")
@login_required
def players():
    players = Joueur.query.all()
    return render_template("joueurs.html", players=players)

# Page des équipes
@app.route("/teams")
@login_required
def teams():
    teams = Equipe.query.all()
    return render_template("equipes.html", teams=teams)

# Return a JSON object with all the players'id from a team
@app.route("/playersInTeam", methods=["POST"])
@login_required
def playersInTeams():
    nom = request.form["name"]
    # Take the team involved
    team = Equipe.query.get(nom)
    # Take all the players related to this team
    players_team = team.players
    list = []
    for player in players_team:
        list.append(player.getId())
    return json.dumps(list)



##################
# Admin section  #
##################


# Supprimer un joueur d'une équipe
@app.route("/deleteFromTeam/id=<id>")
@login_required
def deleteFromTeam(id):
    val = int(id)
    # Check
    player = Joueur.query.get(val)
    if player:
        player.deleteTeam()
        db.session.commit()
    else:
        return render_template("404.html"), 400
    #
    return redirect(url_for("teams"))

# Supprimer un jouer du club
@app.route("/deletePlayer/id=<id>")
@login_required
def deletePlayer(id):
    val = int(id)
    # Check if the player exists
    player = Joueur.query.get(val)
    if player:
        # check if its not yourself
        if val == current_user.getId():
            flash("You cannot delete yourself.", "info")
            return redirect(url_for("players"))
        else:
            db.session.delete(player)
            db.session.commit()
    else:
        msg = "Joueur cherché introuvable."
        return render_template("404.html", msg=msg), 400
    #
    return redirect(url_for("players"))

# Supprimer du materiel
@app.route("/deleteMatos/id=<id>")
@login_required
def deleteMatos(id):
    val = int(id)
    matos = Materiel.query.get(val)
    if matos:
        db.session.delete(matos)
        db.session.commit()
    else:
        msg = "Le matériel recherché n'existe pas."
        return render_template("404.html", msg=msg), 400
    return redirect(url_for("materiel"))

# Supprimer une équipe => mettre un alert en JS si il y a encore des joueurs
@app.route("/deleteTeam/name=<name>")
@login_required
def deleteTeam(name):
    team = Equipe.query.get(name)
    if team:
        db.session.delete(team)
        db.session.commit()
    else:
        msg = "Equipe cherchée introuvable."
        return render_template("404.html",msg=msg), 400

# Supprimer un produit bar
@app.route("/deleteProd/id=<id>")
@login_required
def deleteProd(id):
    val = int(id)
    prod = Produit.query.get(id)
    if prod:
        db.session.delete(prod)
        db.session.commit()
    else:
        msg = "Le produit recherché est introuvable."
        return render_template("404.html", msg=msg), 400

# Modifier un joueur -> le bouton ne sera dispo que pour l'admin ou le joueur conerné (Jinja2)
# Faire un JS demandant que la section old password soit remplie pour remplir new password
@app.route("/editPlayer/id=<id>", methods=["GET","POST"])
@login_required
def editPlayer(id):
    val = int(id)
    player = Joueur.query.get(val)
    # Formulaire adéquat
    form = EditPlayerForm()
    if form.validate_on_submit():
        # Traitement du nouveau pseudo
        new_pseudo = form.username.data
        player.editPseudo(new_pseudo)
        # Traitement du nouveau mdp
        old_mdp = form.old_password.data
        new_mdp = form.new_password_2.data
        if old_mdp:
            # Verification du mdp
            if not player.check_password(old_mdp):
                flash("Wrong Password", "info")
                return redirect(url_for("editPlayer", id=id))
            else:
                player.editMdp(new_mdp)
                player.set_password(new_mdp)
        db.session.commit()
        return redirect(url_for("players"))
    else:
        return render_template("editPlayer.html", player=player, form=form)

# Edit team
@app.route("/editTeam/nom=<nom>")
@login_required
def editTeam(nom):
    equipe = Equipe.query.get(nom)
    form = EditTeamForm()
    if form.validate_on_submit():
        new_name = form.name.data
        equipe.editName(new_name)
        db.session.commit()
        return redirect(url_for("teams"))
    else:
        render_template("editTeam.html", equipe=equipe, form=form)

# Edit a product
@app.route("/editProduct/id=<id>", methods=["GET","POST"])
@login_required
def editProduct(id):
    val = int(id)
    prod = Produit.query.get(val)
    form = MyProductForm()
    if form.validate_on_submit():
        # Récupération des données
        new_name = form.name.data
        new_quantite = form.quantite.data
        new_type = form.type.data
        new_tarif = form.tarif.data
        # Modification
        prod.editProd(new_name, new_quantite, new_type, new_tarif)
        db.session.commit()
        return redirect(url_for("products"))
    else:
        return render_template("editProduct.html",form=form,prod=prod)

##################
# AJAX routes    #
##################
@app.route("/askPlayerInfo", methods=["POST"])
@login_required
def askPlayerInfo():
    id = request.form["id"]
    id = int(id)
    player = Joueur.query.get(id)
    return json.dumps({"id": player.getId(), "pseudo": player.getUsername(), "admin": current_user.isAdmin()})

@app.route("/confirmAuthor", methods=["POST"])
def confirmAuthor():
    # Get the data
    name = request.form["name"]
    comms = Commentaire.query.all()
    # Look for all the authors
    list = []
    for comm in comms:
        tmp = comm.getAuthor()
        if tmp not in list:
            list.append(tmp)
    # Check if name is in the author list
    if name in list:
        return json.dumps(True)
    else:
        return json.dumps(False)

@app.route("/commsFromAuthor", methods=["POST"])
def commsFromAuthor():
    # Get the data
    name = request.form["name"]
    comms = Commentaire.query.filter_by(auteur=name).all()
    # Take the id
    list = []
    for comm in comms:
        list.append(comm.getId())
    return json.dumps(list)

@app.route("/infoComm", methods=["POST"])
def infoComm():
    id = request.form["id"]
    id = int(id)
    # Take the comm involved
    comm = Commentaire.query.get(id)
    # Return the information under JSON format
    return json.dumps({"id": comm.getId(), "auteur": comm.getAuthor(), "date": comm.getDate(), "texte": comm.getMessage()})

@app.route("/allComm", methods=["POST"])
def allComm():
    comms = Commentaire.query.all()
    list = []
    for comm in comms:
        list.append(comm.getId())
    return json.dumps(list)
