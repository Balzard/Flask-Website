from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import ValidationError, InputRequired, Length, Email, EqualTo

#herite de flaskform


class MyLoginForm(FlaskForm):
     username = StringField('Username :', validators=[InputRequired(), Length(min=5, max=80)])
     password = PasswordField('Password :', validators=[InputRequired(), Length(min=3, max=16)])
     submit = SubmitField('Login')

class MyRegistrationForm(FlaskForm):
      username = StringField('Username :', validators=[InputRequired(),Length(min=5, max=80)])
      firstname = StringField('First Name :', validators=[InputRequired(), Length(min=3,max=20)])
      lastname = StringField('Last Name :',validators=[InputRequired(),Length(min=3,max=30)])
      date = DateField("Birth Date :", validators=[InputRequired()])
      password = PasswordField('Password :', validators=[InputRequired(),Length(min=3, max=16)])
      password2 = PasswordField('Repeat Password :', validators=[InputRequired(),EqualTo('password')])
      submit = SubmitField('Register')
      def validate_username(self, username):
          user = Joueur.query.filter_by(pseudo=username.data).first()
          if user is not None:
                raise ValidationError('Please use a different username.')

class MyCommentForm(FlaskForm):
    comm = StringField("Commentaire :", validators=[InputRequired(), Length(min=3,max=210)])

class EditPLayerForm(FlaskForm):
    username = StringField("New username :", validators=[InputRequired(), Length(min=5,max=80)])
    old_password = StringField("Old password :", validators=[Length(min=3,max=16)])
    new_password_1 = StringField("New password  :", validators=[Length(min=3,max=16)])
    new_password_2 = StringField("Confirm new password  :", validators=[EqualTo("new_password_1")])
    submit = SubmitField("Edit Player")
    def validate_username(self, username):
        user = Joueur.query.filter_by(pseudo=username.data).first()
        if user is not None:
              raise ValidationError('Please use a different username.')

class EditTeamForm(FlaskForm):
    name = StringField("New name :", validators=[InputRequired(), Length(min=1,max=11)])

class MyProductForm(FlaskForm):
    name = StringField("Nom :", validators=[InputRequired(), Length(min=5,max=21)])
    quantite = StringField("Quantité :", validators=[InputRequired(), Length(min=1,max=3)])
    type = SelectField("Type :", choices=[("drink","Boisson"), ("eat","Nourriture")])
    tarif = StringField("Tarif :", validators=[InputRequired(), Length(min=1,max=4)])

from app.models import Joueur
