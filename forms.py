from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
    name = StringField('First Name', validators=[DataRequired(), Length(max=64)], render_kw={"placeholder": "NOMBRE"})
    lastName = StringField('Last Name', validators=[DataRequired(), Length(max=31)], render_kw={"placeholder": "APELLIDO"})
    numDocument = StringField('numDocument', validators=[DataRequired(), Length(max=20)], render_kw={"placeholder": "NUMERO DE DOCUMENTO"})
    telephone = StringField('Telephone', validators=[DataRequired(), Length(max=20)], render_kw={"placeholder": "TELEFONO"})
    userName = StringField('UserName', validators=[DataRequired(), Length(max=20)], render_kw={"placeholder": "INSTAGRAM"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "CORREO ELECTRONICO"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "CONTRASENA"})
    password2 = PasswordField('Password2', validators=[DataRequired()], render_kw={"placeholder": "CONFIRMAR CONTRASENA"})
    submit = SubmitField('REGISTRARSE')

class EditForm(FlaskForm):
    name = StringField('First Name', validators=[DataRequired(), Length(max=64)], render_kw={"placeholder": "NOMBREw"})
    lastName = StringField('Last Name', validators=[DataRequired(), Length(max=31)], render_kw={"placeholder": "APELLIDOw"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "CORREO ELECTRONICOw"})
    instagram = StringField('Instagram', validators=[DataRequired(), Length(max=15)], render_kw={"placeholder": "INSTAGRAMw"})
    numDocument = StringField('numDocument', validators=[DataRequired(), Length(max=20)], render_kw={"placeholder": "NUMERO DE DOCUMENTOw"})
    telephone = StringField('Telephone', validators=[DataRequired(), Length(max=20)], render_kw={"placeholder": "TELEFONOw"})
    address = StringField('Address', validators=[DataRequired(), Length(max=20)], render_kw={"placeholder": "DIRECCIONw"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "CONTRASENAw"})
    submit = SubmitField('Editar')

class PasswordForm(FlaskForm):
    password1 = PasswordField('Password1', validators=[DataRequired()], render_kw={"placeholder": "CONTRASENA ANTIGUA"})
    password2 = PasswordField('Password2', validators=[DataRequired()], render_kw={"placeholder": "NUEVA CONTRASENA"})
    password3 = PasswordField('Password3', validators=[DataRequired()], render_kw={"placeholder": "CONFIRMAR NUEVA CONTRASENA"})
    submit = SubmitField('Cambiar')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=128)])
    title_slug = StringField('Slug title', validators=[Length(max=128)])
    content = StringField('Content')
    submit = SubmitField('Send')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()], render_kw={"placeholder": "CORREO ELECTRONICO"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "CONTRASENA"})
    remember_me = BooleanField('Remember me')
    submit = SubmitField('INICIAR SESION')