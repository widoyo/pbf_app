from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms import DateField, HiddenField
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
    
class PasswordForm(FlaskForm):
    username = StringField()
    new_password = StringField()
    
class UserForm(FlaskForm):
    username = StringField()
    password = PasswordField()
    role = SelectField(choices=[(1, 'Sales'),(2, 'Gudang'),(3, 'Adm/Kug')]) # 0 super, 1 sales, 2 gudang, 3 keuangan
    submit = SubmitField('Kirim')
    
