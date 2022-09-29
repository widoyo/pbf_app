import datetime
from flask import Flask, render_template, redirect, url_for, flash
from flask import send_from_directory, request, abort
from werkzeug.urls import url_parse
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_cors import CORS

from config import Config

from app.forms import LoginForm, PesananInForm, AbsenForm, MovingForm
from app.models import db, User, Pelanggan, Obat, Jual, Absen, Moving

login_manager = LoginManager()    
login_manager.login_view = 'login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    login_manager.init_app(app)
    db.init_app(app)
    CORS(app, resource={r"/api/*": {"origins": "*"}})

    from app import user, absen
    from app import api
    from app import pelanggan, pesanan, penjualan
    from app import obat
    
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.get_by_id(user_id)
        except:
            return None

    @app.before_request
    def before_request():
        if current_user.is_authenticated:
            current_user.last_seen = datetime.datetime.utcnow()
            current_user.save()
    
    app.register_blueprint(user.bp, url_prefix='/user')
    app.register_blueprint(pelanggan.bp, url_prefix='/pelanggan')
    app.register_blueprint(api.bp, url_prefix='/api')
    app.register_blueprint(pesanan.bp, url_prefix='/pesanan')
    app.register_blueprint(penjualan.bp, url_prefix='/penjualan')
    app.register_blueprint(obat.bp, url_prefix='/obat')
    app.register_blueprint(absen.bp, url_prefix='/absen')
    

    @app.route('/password/<username>', methods=['GET', 'POST'])
    @login_required
    def password_user(username):
        if current_user.role != 0:
            abort(403)
        user = User.get(User.username==username)
        if request.method == 'POST':
            user.set_password(request.form.get('password'))
            user.save()
            flash('Passsword telah diganti')
            return redirect('/user')
        return render_template('set_password.html', user=user)

    @app.route('/password', methods=['GET', 'POST'])
    @login_required
    def password():
        user = current_user
        if request.method == 'POST':
            user.set_password(request.form.get('password'))
            user.save()
            flash('Passsword telah diganti')
            return redirect('/')
        return render_template('set_password.html', user=user)

    @app.route('/panduan')
    @login_required
    def panduan():
        return render_template('/panduan.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        next_page = request.args.get('next')
        if form.validate_on_submit():
            try:
                user = User.get(User.username==form.username.data)
            except User.DoesNotExist:
                flash('Invalid username or password')
                return redirect(url_for('login'))
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            
            
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('homepage')
            return redirect(next_page)
        return render_template('login.html', title='Sign In', form=form, next=next_page)
    
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect('/')    

    @app.route('/')
    def homepage():
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        if current_user.role == 1: # Sales
            pelanggans = Pelanggan.select()
            obats = Obat.select()
            form_pesanan_in = PesananInForm()
            form_pesanan_in.pelanggan.choices = [(p.id, p.nama) for p in Pelanggan.select().order_by(Pelanggan.nama)]
            return render_template('index_sales.html', pelanggans=pelanggans, form_pesanan_in=form_pesanan_in)
        elif current_user.role == 0:
            juals = Jual.select().order_by(Jual.tanggal.desc())
        return render_template('index.html', juals=Jual.select())
    
    return app