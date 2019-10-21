from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
    name = StringField('First Name', validators=[DataRequired(), Length(max=64)])
    lastName = ('Last Name', validators=[DataRequired(), Length(max=31)])
    address = ('Address', validators=[DataRequired(), Length(max=30)])
    telephone = ('Telephone', validators=[DataRequired(), Length(max=20)])
    payMethod = ('Pay Method', validators=[DataRequired(), Length(max=30)])
    userName = ('UserName', validators=[DataRequired(), Length(max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password2', validators=[DataRequired()])
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