# Menggunakan Python 3.11 sebagai dasar
FROM python:3.11-slim

# Menetapkan direktori kerja di dalam kontainer
WORKDIR /app

# Menyalin file dependensi
COPY requirements.txt requirements.txt

# Menginstal dependensi
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin semua kode aplikasi ke dalam kontainer
COPY . .

# Memberi tahu Koyeb port mana yang akan digunakan oleh aplikasi
EXPOSE 8000

# Perintah untuk menjalankan aplikasi menggunakan Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "app:app"]
