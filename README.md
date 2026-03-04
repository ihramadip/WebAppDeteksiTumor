# Web App Deteksi Tumor Otak (Brain Tumor Detection)

Aplikasi web berbasis Flask yang dirancang untuk mendeteksi tumor otak dari hasil pemindaian MRI menggunakan model Deep Learning. Sistem ini mengklasifikasikan gambar ke dalam empat kategori: **Glioma, Meningioma, Pituitary, atau Tanpa Tumor**.

## 🚀 Fitur Utama

- **Deteksi Otomatis:** Menggunakan model Convolutional Neural Network (CNN) untuk analisis citra MRI yang akurat.
- **Analisis Real-time:** Fitur unggah gambar dengan hasil instan menggunakan API internal tanpa perlu memuat ulang halaman (AJAX).
- **Sistem Autentikasi:** Manajemen login dan registrasi pengguna yang aman.
- **Panel Admin:** Dashboard khusus untuk mengelola akun pengguna (Tambah, Edit, Hapus).
- **Keamanan:** Dilengkapi dengan proteksi CSRF, Rate Limiting, dan manajemen sesi untuk mencegah login ganda.
- **Antarmuka Responsif:** Tampilan modern berbasis Bootstrap yang optimal di berbagai perangkat.

## 🛠️ Teknologi yang Digunakan

- **Backend:** Python & Flask
- **AI/ML:** TensorFlow & Keras (Model: `brain_tumor_model.h5`)
- **Database:** SQLAlchemy (Mendukung SQLite & PostgreSQL)
- **Frontend:** HTML5, CSS3 (Bootstrap), JavaScript (Vanilla)
- **Keamanan:** Flask-WTF (CSRF), Flask-Limiter, Flask-Login

## 📂 Struktur Proyek Utama

- `app.py`: Titik masuk aplikasi dan manajemen rute (API & Web).
- `tumor_detector.py`: Logika inti pemrosesan citra dan prediksi AI.
- `models.py`: Definisi skema database pengguna.
- `forms.py`: Validasi formulir input.
- `manage_users.py`: Alat baris perintah (CLI) untuk manajemen admin.
- `static/`: Berisi file aset seperti CSS dan JavaScript API.
- `templates/`: Kumpulan template HTML untuk UI aplikasi.

## ⚙️ Cara Instalasi

1. **Clone Repository:**
   ```bash
   git clone https://github.com/ihramadip/WebAppDeteksiTumor.git
   cd WebAppDeteksiTumor
   ```

2. **Setup Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Untuk Windows: venv\Scripts\activate
   ```

3. **Instal Dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Konfigurasi Lingkungan:**
   Salin `.env.example` menjadi `.env` dan sesuaikan `SECRET_KEY` serta database.

5. **Jalankan Aplikasi:**
   ```bash
   python app.py
   ```

## 📖 Cara Penggunaan

1. Daftar akun baru atau masuk menggunakan akun yang ada.
2. Masuk ke halaman utama "Deteksi".
3. Pilih file gambar MRI (format JPG/PNG).
4. Klik tombol analisis dan tunggu hasil prediksi serta tingkat kepercayaan (confidence score) muncul di layar.
5. Admin dapat mengakses panel `/admin/dashboard` untuk mengelola pengguna.

---
Dikembangkan dengan ❤️ untuk mendukung diagnosis medis berbasis teknologi.
