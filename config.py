import os

# Direktori dasar aplikasi
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Kunci rahasia untuk keamanan sesi, sangat penting!
    # Diambil dari environment variable. Pastikan untuk mengatur ini di lingkungan produksi!
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-hard-to-guess-string-for-dev'
    
    # Konfigurasi database SQLite (dinonaktifkan)
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'instance', 'app.db')

    # Konfigurasi database PostgreSQL
    # Ganti 'YOUR_PASSWORD' dengan password yang Anda atur saat instalasi PostgreSQL.
    # Nama database 'analisis_data_db' adalah contoh, Anda perlu membuatnya terlebih dahulu.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:ihramadi@localhost:5432/analisis_data_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Pengaturan Keamanan Kuki Sesi
    # Set menjadi True di produksi (jika menggunakan HTTPS)
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
