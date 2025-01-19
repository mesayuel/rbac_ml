# RBAC Application with ML-Based Intent Detection

Aplikasi Role-Based Access Control (RBAC) sederhana dengan deteksi intent menggunakan Machine Learning. Aplikasi ini menggunakan Flask sebagai web framework dan SQLite sebagai database.

### Fitur

- Role-Based Access Control (RBAC)
- Machine Learning untuk deteksi intent dari input teks
- RESTful API endpoints
- SQLite database
- Unit testing

### Struktur Folder

rbac_ml_app/

├── app.py # Aplikasi Flask utama

├── models.py # Model database

├── ml.py # Komponen Machine Learning

├── requirements.txt # Dependensi

└── test_app.py # Unit tests


## Instalasi

#### 1. Clone repository
  python -m venv venv

#### 2. Buat virtual environtment

#### Windows
  venv\Scripts\activate

#### macOS/Linux
  source venv/bin/activate

#### 3. Install dependencies:
  pip install -r requirements.txt

#### 4. Jalankan aplikasi
  python app.py

Aplikasi akan berjalan di http://localhost:5000

### Komponen Machine Learning
Aplikasi menggunakan kombinasi spaCy dan scikit-learn untuk deteksi intent:

spaCy: Untuk pemrosesan bahasa alami

scikit-learn: Untuk klasifikasi teks menggunakan TF-IDF dan Naive Bayes

Intent yang didukung:
- edit_document
- view_document
- delete_document
  
#### Database Schema

- Users:
id (Primary Key)
username (Unique)
- Roles:
id (Primary Key)
name (Unique)
- Permissions:
id (Primary Key)
name (Unique)
- Relationships:
user_roles (Many-to-Many)
role_permissions (Many-to-Many)

#### 5. Jalankan test
python -m unittest test_app.py -v
