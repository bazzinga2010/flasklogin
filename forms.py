from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,EqualTo


class RegisterForm(FlaskForm):
	firstname = StringField("Enter your first name",validators = [DataRequired("Enter first name")])
	lastname = StringField("Enter your last name",validators = [DataRequired("Enter last name")])
	username = StringField("Enter Your User name",validators = [DataRequired("ENtr username")])
	password = PasswordField("Enter your Password",validators = [DataRequired("Enter valid password")])
	confirm = PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField("Register")


class LoginForm(FlaskForm):
	username = StringField("username",validators=[DataRequired()])
	password = PasswordField("Password",validators=[DataRequired()])
	remember = BooleanField("remember me")
	submit = SubmitField("Login")



