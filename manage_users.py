import sys
from getpass import getpass

# Impor komponen aplikasi Flask yang diperlukan
from app import app
from models import db, User

def add_user(username, password, is_admin=False):
    """Fungsi untuk menambahkan pengguna baru ke database."""
    # Menjalankan dalam konteks aplikasi untuk mengakses database
    with app.app_context():
        # Periksa apakah pengguna sudah ada
        if User.query.filter_by(username=username).first():
            print(f"Error: Pengguna '{username}' sudah ada.")
            return

        # Buat pengguna baru dan set password (sudah di-hash oleh model)
        new_user = User(username=username, is_admin=is_admin) # Set is_admin here
        new_user.set_password(password)
        
        # Tambahkan ke database
        db.session.add(new_user)
        db.session.commit()
        print(f"Pengguna '{username}' berhasil ditambahkan.")

def delete_user(username):
    """Fungsi untuk menghapus pengguna dari database."""
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"Error: Pengguna '{username}' tidak ditemukan.")
            return
        
        db.session.delete(user)
        db.session.commit()
        print(f"Pengguna '{username}' berhasil dihapus.")

def main():
    """Fungsi utama untuk menjalankan perintah dari terminal."""
    if len(sys.argv) < 2:
        print("Penggunaan: python manage_users.py [perintah]")
        print("Perintah yang tersedia: adduser, deleteuser")
        return

    command = sys.argv[1].lower()

    if command == 'adduser':
        if len(sys.argv) < 3:
            print("Penggunaan: python manage_users.py adduser <username> [--admin]")
            return
        
        username = sys.argv[2]
        is_admin_flag = '--admin' in sys.argv
        
        password = getpass(f"Masukkan password untuk {username}: ")
        password_confirm = getpass("Konfirmasi password: ")

        if password != password_confirm:
            print("Error: Password tidak cocok.")
            return
        
        add_user(username, password, is_admin=is_admin_flag)
    elif command == 'deleteuser':
        if len(sys.argv) < 3:
            print("Penggunaan: python manage_users.py deleteuser <username>")
            return
        
        username = sys.argv[2]
        delete_user(username)
    else:
        print(f"Perintah '{command}' tidak dikenal.")

if __name__ == '__main__':
    main()