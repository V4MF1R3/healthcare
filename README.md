# Healthcare Backend

## 🩺 Overview
This project is a backend system for managing healthcare-related data such as patients, doctors, and their associations. Built with **Django**, **Django REST Framework**, and **PostgreSQL**, it supports JWT-based user authentication and RESTful APIs for healthcare operations.

## 🚀 Features
- User registration and login (JWT authentication)
- Patient management (CRUD)
- Doctor management (CRUD)
- Patient-doctor assignment
- Secure API access for authenticated users

## 🧰 Tech Stack
- Python
- Django
- Django REST Framework
- PostgreSQL
- JWT (via `djangorestframework-simplejwt`)

---

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/V4MF1R3/healthcare.git
cd healthcare
```

### 2. Create & Activate Virtual Environment
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL
Create a PostgreSQL database and user:
```bash
CREATE DATABASE healthcare_db;
CREATE USER healthcare_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE healthcare_db TO healthcare_user;
```

### 5. Configure Environment Variables
Create a .env file in the root directory:
```bash
SECRET_KEY=your_django_secret_key
DEBUG=True
DB_NAME=healthcare_db
DB_USER=healthcare_user
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```
Update settings.py to load these using python-decouple or os.environ.

### 6. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Run Development Server
```bash
python manage.py runserver
```

## License
This project is licensed under the [MIT License](LICENSE).

## Contact
For questions or support, please contact [pantvaibhav16@gmail.com].
