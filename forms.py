from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
    name = StringField('First Name', validators=[DataRequired(), Length(max=64)], render_kw={"placeholder": "NOMBRE"})
    lastName = ('Last Name', validators=[DataRequired(), Length(max=31)], render_kw={"placeholder": "APELLIDO"})
    numDocument = ('Document', validators=[DataRequired(), Length(max=20)], render_kw={"placeholder": "NUMERO DE DOCUMENTO"})
    telephone = ('Telephone', validators=[DataRequired(), Length(max=20)], render_kw={"placeholder": "TELEFONO"})
    userName = ('UserName', validators=[DataRequired(), Length(max=15)], render_kw={"placeholder": "NOMBRE DE USUARIO"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "CORREO ELECTRONIO"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "CONTRASENA"})
    password2 = PasswordField('Password2', validators=[DataRequired()], render_kw={"placeholder": "CONFIRMAR CONTRASENA"})
    submit = SubmitField('Register')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=128)])
    title_slug = StringField('Slug title', validators=[Length(max=128)])
    content = StringField('Content')
    submit = SubmitField('Send')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()], render_kw={"placeholder": "CORREO ELECTRONICO"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "CONTRASENA"})
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')