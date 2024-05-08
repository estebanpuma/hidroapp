from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, DateField, SubmitField
from wtforms.validators import Email, DataRequired


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Ingresar")
    
    
class AddUserForm(FlaskForm):
    name = StringField("Noombre", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    role = StringField("Cargo", validators=[DataRequired()])
    birth = DateField("Fecha de nacimiento")
    submit = SubmitField("Registrar")