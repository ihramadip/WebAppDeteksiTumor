import os
import uuid
from functools import wraps
from werkzeug.utils import secure_filename
from flask import (Flask, request, jsonify, render_template, redirect, url_for, flash, session, send_from_directory)
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv

# Muat environment variables dari .env file
load_dotenv()

# Import dari file lokal
from config import Config
from models import db, bcrypt, User
from forms import LoginForm, UserForm, AdminUserEditForm
from tumor_detector import predict_tumor # <-- Mengganti model analisis

# Import keamanan
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Inisialisasi Aplikasi Flask
app = Flask(__name__)
app.config.from_object(Config)

# Konfigurasi folder upload
# Pastikan path ini ada atau dibuat saat aplikasi dimulai
app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Inisialisasi ekstensi
db.init_app(app)
bcrypt.init_app(app)
csrf = CSRFProtect(app)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# Konfigurasi Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Harap login untuk mengakses halaman ini."
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Helper & Dekorator ---

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Anda tidak memiliki izin untuk mengakses halaman ini.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# --- Rute Otentikasi & Sesi (Tidak Berubah) ---

@app.before_request
def check_concurrent_login():
    if current_user.is_authenticated and request.endpoint not in ['static', 'uploads']:
        if 'current_session_id' in session and current_user.current_session_id != session['current_session_id']:
            logout_user()
            flash('Anda telah login dari lokasi lain. Sesi Anda telah diakhiri.', 'info')
            return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute", error_message="Terlalu banyak percobaan login, coba lagi nanti.")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            new_session_id = str(uuid.uuid4())
            user.current_session_id = new_session_id
            db.session.add(user)
            db.session.commit()
            session['current_session_id'] = new_session_id
            login_user(user)
            flash('Login berhasil!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login gagal. Periksa kembali username dan password Anda.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        current_user.current_session_id = None
        db.session.add(current_user)
        db.session.commit()
    logout_user()
    flash('Anda telah berhasil logout.', 'success')
    return redirect(url_for('login'))

# --- Rute Aplikasi Utama ---

@app.route('/')
@login_required
def index():
    return render_template('index.html')

# --- RUTE API BARU UNTUK DETEKSI TUMOR ---
@app.route('/api/detect_tumor', methods=['POST'])
@login_required
def detect_tumor_api():
    if 'file' not in request.files:
        return jsonify({'error': 'Tidak ada file yang diunggah'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nama file kosong'}), 400

    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            # Tambahkan UUID untuk memastikan nama file unik
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)

            # Panggil model prediksi (saat ini masih placeholder)
            prediction_results = predict_tumor(filepath)
            
            # Tambahkan URL gambar untuk ditampilkan di frontend
            prediction_results['image_url'] = url_for('uploads', filename=unique_filename)

            return jsonify(prediction_results)
        except Exception as e:
            app.logger.error(f"Error during prediction: {e}")
            return jsonify({'error': f'Terjadi kesalahan saat memproses gambar: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Format file tidak valid. Harap unggah file .png, .jpg, atau .jpeg'}), 400

# Rute untuk menyajikan gambar yang diunggah
@app.route('/uploads/<filename>')
@login_required
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# --- Rute Panel Admin (Tidak Berubah) ---
@app.route('/admin')
@admin_required
def admin_dashboard():
    users = User.query.all()
    return render_template('admin/dashboard.html', users=users)

@app.route('/admin/users')
@admin_required
def admin_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/users/add', methods=['GET', 'POST'])
@admin_required
def admin_add_user():
    form = UserForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, is_admin=form.is_admin.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Pengguna {new_user.username} berhasil ditambahkan!', 'success')
        return redirect(url_for('admin_users'))
    return render_template('admin/add_user.html', form=form)

@app.route('/admin/users/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = AdminUserEditForm(original_username=user.username)
    if form.validate_on_submit():
        user.username = form.username.data
        user.is_admin = form.is_admin.data
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash(f'Pengguna {user.username} berhasil diperbarui!', 'success')
        return redirect(url_for('admin_users'))
    elif request.method == 'GET':
        form.username.data = user.username
        form.is_admin.data = user.is_admin
    return render_template('admin/edit_user.html', form=form, user=user)

@app.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Anda tidak bisa menghapus akun Anda sendiri!', 'danger')
        return redirect(url_for('admin_users'))
    db.session.delete(user)
    db.session.commit()
    flash(f'Pengguna {user.username} berhasil dihapus!', 'success')
    return redirect(url_for('admin_users'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
