from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
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
    comm = StringField("Commentaire :", validators=[InputRequired(),Length(min=3,max=210)])

from app.models import Joueur
