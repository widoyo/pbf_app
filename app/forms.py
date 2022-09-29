from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms import DateField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class AbsenForm(FlaskForm):
    username = HiddenField()
    ll = StringField('LatLon')
    radius = StringField('Radius')
    keterangan = StringField(validators=[DataRequired()])
    submit = SubmitField('Klik')
    
class MovingForm(FlaskForm):
    username = HiddenField()
    aktifitas = StringField()
    submit = SubmitField('Simpan')
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class PesananInForm(FlaskForm):
    pelanggan = SelectField('Pelanggan')
    tanggal = DateField()
    jatuh_tempo = DateField()
    submit = SubmitField()
    
class PasswordForm(FlaskForm):
    username = HiddenField()
    new_password = StringField()
    
class UserForm(FlaskForm):
    username = StringField()
    password = PasswordField()
    role = SelectField(choices=[(1, 'Sales'),(2, 'Gudang'),(3, 'Adm/Kug'),(0, 'Manager')]) # 0 super, 1 sales, 2 gudang, 3 keuangan
    submit = SubmitField('Tambah User')
    
