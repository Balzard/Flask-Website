from flask_login import UserMixin
from app.forms import MyRegistrationForm
from app import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

class Equipe(db.Model):
    __tablename__ = "equipe"
    nom = db.Column(db.String, primary_key=True)

class Entrainement(db.Model):
    __tablename__ = "entrainement"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    horaire = db.Column(db.Date, nullable=False)

class Match(db.Model):
    __tablename__ = "match"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    heure = db.Column(db.Date, nullable=False)
    score = db.Column(db.String(10), nullable=False)
    rival = db.Column(db.String(20), nullable=False)
    equipe = db.Column(db.String, db.ForeignKey("equipe.nom"))

class Joueur(UserMixin ,db.Model):
    __tablename__ = "joueur"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pseudo = db.Column(db.String(15), unique=True, nullable=False)
    mdp = db.Column(db.String(15))
    mdp_hash = db.Column(db.String(128))
    nom = db.Column(db.String(20), nullable=False)
    prenom = db.Column(db.String(20), nullable=False)
    naissance = db.Column(db.DATE, nullable=False)
    admin = db.Column(db.Boolean, default=False)
    equipe = db.Column(db.String, db.ForeignKey("equipe.nom"), nullable=True)

    def getUsername(self):
        return self.pseudo

    def set_password(self, mdp):
        self.mdp_hash = generate_password_hash(mdp)

    def check_password(self, mdp):
        return check_password_hash(self.mdp_hash, mdp)

class Materiel(db.Model):
    __tablename__ = "materiel"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantite = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String, nullable=False)

class Produit(db.Model):
    __tablename__  = "produit"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantite = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String, nullable=False)
    tarif = db.Column(db.Float, nullable=False)

class Commentaire(db.Model):
    __tablename__ = "commentaire"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    texte = db.Column(db.String(210), nullable=False)
    autheur = db.Column(db.String(21), nullable=True)


db.drop_all()
db.create_all()

# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return Joueur.query.get(int(userid))
