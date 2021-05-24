from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired, ValidationError
from src.models import User

class LoginForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email()],render_kw={"placeholder": "Email", "type": "email"})
	password = PasswordField("Password", validators=[DataRequired()],render_kw={"placeholder": "Password"})
	remember_me = BooleanField("Remember me")
	submit = SubmitField("Sign in")

class RegisterForm(FlaskForm):
	first_name = StringField("First name", validators=[DataRequired(), Length(min=3, max=42)],render_kw={"placeholder": "Prénom"})
	last_name = StringField("Last name", validators=[DataRequired(), Length(min=3, max=42)],render_kw={"placeholder": "Nom"})
	username = StringField("Username", validators=[DataRequired(), Length(min=3, max=62)],render_kw={"placeholder": "Username"})
	email = StringField("Email", validators=[DataRequired(),Email()],render_kw={"placeholder": "Email", "type": "E-mail"})
	password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=42)],render_kw={"placeholder": "Mot de passe"})
	repeat_password = PasswordField("Repeat password", validators=[DataRequired(), EqualTo('password')],render_kw={"placeholder": "Répeter votre mot de passe"})
	avatar = FileField("avatar")
	submit = SubmitField("Sign up")

	def validate_username(self, username):
		if User.query.filter_by(username=username.data).first():
			raise ValidationError("That username is taken, please choose a different one.")

	def validate_email(self, email):
		if User.query.filter_by(email=email.data).first():
			raise ValidationError("That email is taken, please choose a different one.")

class BillingForm(FlaskForm):
	first_name = StringField("First name", validators=[Length(min=0, max=42)],render_kw={"placeholder": "Prénom"})
	last_name = StringField("Last name", validators=[Length(min=0, max=42)],render_kw={"placeholder": "Nom"})
	city = StringField("City", validators=[DataRequired(), Length(min=3, max=42)], render_kw={"placeholder": "Votre ville (Obligatoire)"})
	address = StringField("Address", validators=[DataRequired(), Length(min=3, max=42)], render_kw={"placeholder": "Votre addresse (Obligatoire)"})
	phone = StringField("Phone",validators=[DataRequired(), Length(min=8, max=15)],  render_kw={"placeholder": "Votre numero de télephone (Obligatoire)"})
	phone2 = StringField("Phone",validators=[Length(min=8, max=15)],  render_kw={"placeholder": "Votre numero de télephone"})
	submit = SubmitField("Continuer le paiement")
