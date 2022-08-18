from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms import DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class PesananOutForm(FlaskForm):
    pelanggan = SelectField('Pelanggan')
    tanggal = DateField()
    jatuh_tempo = DateField()
    submit = SubmitField()