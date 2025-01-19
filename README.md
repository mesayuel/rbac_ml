# RBAC Application with ML-Based Intent Detection

Aplikasi Role-Based Access Control (RBAC) sederhana dengan deteksi intent menggunakan Machine Learning. Aplikasi ini menggunakan Flask sebagai web framework dan SQLite sebagai database.

### Fitur

- Role-Based Access Control (RBAC)
- Machine Learning untuk deteksi intent dari input teks
- RESTful API endpoints
- SQLite database
- Unit testing

### Struktur Folder

rbac_app/
├── app.py # Aplikasi Flask utama
├── models.py # Model database
├── ml.py # Komponen Machine Learning
├── requirements.txt # Dependensi
└── test_app.py # Unit tests


## Instalasi

1. Clone repository
python -m venv venv

2. Buat virtual environtment

### Windows
venv\Scripts\activate

### macOS/Linux
source venv/bin/activate

3. Install dependencies:
pip install -r requirements.txt
python -m spacy download en_core_web_sm

4. Jalankan aplikasi
python app.py

Aplikasi akan berjalan di http://localhost:5000

5. Jalankan test
python -m unittest test_app.py