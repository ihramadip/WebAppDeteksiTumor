from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError
from models import User # Import User model to check for existing username

class LoginForm(FlaskForm):
    """Form untuk login pengguna."""
    username = StringField(
        'Username',
        validators=[
            DataRequired(message="Username tidak boleh kosong."),
            Length(min=4, max=25, message="Username harus antara 4 dan 25 karakter."),
            # Memastikan username hanya berisi karakter yang aman
            Regexp('^[A-Za-z0-9_]+$', message="Username hanya boleh berisi huruf, angka, dan underscore.")
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password tidak boleh kosong."),
            Length(min=8, message="Password minimal harus 8 karakter.")
        ]
    )
    submit = SubmitField('Login')

class UserForm(FlaskForm):
    """Form untuk menambah pengguna baru dari panel admin."""
    username = StringField(
        'Username',
        validators=[
            DataRequired(message="Username tidak boleh kosong."),
            Length(min=4, max=25, message="Username harus antara 4 dan 25 karakter."),
            Regexp('^[A-Za-z0-9_]+$', message="Username hanya boleh berisi huruf, angka, dan underscore.")
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password tidak boleh kosong."),
            Length(min=8, message="Password minimal harus 8 karakter.")
        ]
    )
    confirm_password = PasswordField(
        'Konfirmasi Password',
        validators=[
            DataRequired(message="Konfirmasi password tidak boleh kosong."),
            EqualTo('password', message='Password harus sama.')
        ]
    )
    is_admin = BooleanField('Jadikan Admin')
    submit = SubmitField('Tambah Pengguna')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username sudah ada. Harap pilih username lain.')

class AdminUserEditForm(FlaskForm):
    """Form untuk mengedit pengguna dari panel admin (tanpa password wajib)."""
    username = StringField(
        'Username',
        validators=[
            DataRequired(message="Username tidak boleh kosong."),
            Length(min=4, max=25, message="Username harus antara 4 dan 25 karakter."),
            Regexp('^[A-Za-z0-9_]+$', message="Username hanya boleh berisi huruf, angka, dan underscore.")
        ]
    )
    password = PasswordField(
        'Password Baru (kosongkan jika tidak ingin mengubah)',
        validators=[
            Length(min=8, message="Password minimal harus 8 karakter.")
        ]
    )
    confirm_password = PasswordField(
        'Konfirmasi Password Baru',
        validators=[
            EqualTo('password', message='Password harus sama.')
        ]
    )
    is_admin = BooleanField('Jadikan Admin')
    submit = SubmitField('Simpan Perubahan')

    original_username = None # To store original username for validation

    def __init__(self, original_username=None, *args, **kwargs):
        super(AdminUserEditForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username sudah ada. Harap pilih username lain.')