import os
import numpy as np
import tensorflow as tf
import requests

# =====================================================================================
# Konfigurasi Model
# =====================================================================================

# GANTI DENGAN URL UNDUHAN LANGSUNG DARI GOOGLE DRIVE
# Ini adalah placeholder, Anda perlu menggantinya dengan link yang benar.
# MODEL_URL = 'https://github.com/hasibullah-aman/Brain-Tumor-Classification-DataSet/blob/main/brain_tumor_classification.h5?raw=true' # Contoh link langsung dari GitHub

# Path untuk menyimpan model secara lokal di dalam folder instance
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(PROJECT_ROOT, 'instance', 'model')
MODEL_PATH = os.path.join(MODEL_DIR, 'brain_tumor_model.h5')

# Pastikan direktori model ada
os.makedirs(MODEL_DIR, exist_ok=True)

# Spesifikasi yang diasumsikan untuk model
IMAGE_SIZE = (224, 224)
CLASS_LABELS = ['glioma', 'meningioma', 'notumor', 'pituitary']

# =====================================================================================
# Fungsi Helper
# =====================================================================================


def preprocess_image(image_path):
    """
    Memuat dan memproses gambar untuk input model.
    1. Memuat gambar dari path.
    2. Mengubah ukuran ke IMAGE_SIZE.
    3. Mengonversi ke array numpy.
    4. Melakukan normalisasi nilai piksel (membagi dengan 255).
    5. Menambahkan dimensi batch.
    """
    img = tf.keras.utils.load_img(image_path, target_size=IMAGE_SIZE)
    img_array = tf.keras.utils.img_to_array(img)
    img_array = img_array / 255.0  # Normalisasi
    img_batch = np.expand_dims(img_array, axis=0) # Menambah dimensi batch
    return img_batch

# =====================================================================================
# Fungsi Prediksi Utama
# =====================================================================================

def predict_tumor(image_path):
    """
    Fungsi utama untuk melakukan prediksi tumor otak dari sebuah gambar.
    """
    try:
        # Langkah 1: Muat seluruh model (arsitektur dan bobot) dari file .h5
        if not os.path.exists(MODEL_PATH) or os.path.getsize(MODEL_PATH) == 0:
            raise FileNotFoundError(f"File model tidak ditemukan atau kosong di {MODEL_PATH}. Pastikan model sudah ada secara lokal.")
        
        model = tf.keras.models.load_model(MODEL_PATH)

        # Langkah 3: Pra-pemrosesan gambar
        processed_image = preprocess_image(image_path)

        # Langkah 4: Lakukan prediksi
        prediction_scores = model.predict(processed_image)
        
        # Langkah 5: Terjemahkan hasil prediksi (untuk model multi-kelas)
        predicted_class_index = np.argmax(prediction_scores, axis=1)[0]
        predicted_class_label = CLASS_LABELS[predicted_class_index]
        confidence = float(prediction_scores[0][predicted_class_index] * 100) # Ambil probabilitas kelas tertinggi

        # Sesuaikan label untuk tampilan yang lebih baik
        if predicted_class_label == 'notumor':
            predicted_class = "Tidak Ada Tumor"
        else:
            predicted_class = predicted_class_label.replace('_', ' ').title() + " Terdeteksi"

        print(f"Prediksi: Kelas = {predicted_class}, Kepercayaan = {confidence:.2f}")

        return {
            "prediction": predicted_class, # Use the adjusted predicted_class directly
            "confidence": confidence,
            "model_used": "Trained CNN Model" # Updated model name
        }

    except Exception as e:
        print(f"Terjadi kesalahan saat prediksi: {e}")
        # Mengembalikan pesan error yang akan ditampilkan di frontend
        return {
            'error': True,
            'message': str(e)
        }
