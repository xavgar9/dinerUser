from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    name = StringField('First Name', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
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