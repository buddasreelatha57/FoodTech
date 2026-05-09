# 🍽️ FoodTech Blockchain System

A secure and transparent food supply chain management system built using Django and Blockchain technology.  
This project ensures data integrity, traceability, and security across the food distribution process.

---

## 🚀 Features

- 🔗 Blockchain-based data integrity system  
- 🔐 Secure user authentication system  
- 📦 Food supply tracking module  
- 🧾 Transaction history verification  
- 🖥️ Admin dashboard for management  
- 🌐 Web-based interface using Django  

---

## 🛠️ Tech Stack

- Backend: Django (Python)  
- Frontend: HTML, CSS, JavaScript  
- Database: SQLite (development) / PostgreSQL (production)  
- Blockchain: Custom Python implementation  
- Server: Gunicorn  
- Static Files: Whitenoise  

---

## 📁 Project Structure
FoodTech/
│
├── FoodTech/ # Django project settings
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
│
├── FoodTechApp/ # Main application
│ ├── views.py
│ ├── urls.py
│ ├── models.py
│ ├── templates/
│ └── static/
│
├── Blockchain.py # Blockchain logic
├── manage.py
└── requirements.txt


---

## ⚙️ Installation & Setup

### 1. Clone the repository

git clone https://github.com/your-username/FoodTech.git

cd FoodTech


### 2. Create virtual environment

python -m venv venv


Activate:

venv\Scripts\activate (Windows)
source venv/bin/activate (Mac/Linux)


### 3. Install dependencies

pip install -r requirements.txt


### 4. Run migrations

python manage.py migrate


### 5. Run server

python manage.py runserver


Open:

http://127.0.0.1:8000/


---

## 🌍 Deployment

Deployed using Render  
Start command:

gunicorn FoodTech.wsgi:application


---

## 📦 Dependencies


Django
gunicorn
whitenoise
pyaes
pbkdf2
pypng
opencv-python-headless
numpy
Pillow


---

## ⚠️ Notes

- Use PostgreSQL for production
- Run collectstatic before deployment
- Ensure all dependencies are installed

---

## 🚀 Future Improvements

- AI-based food quality detection  
- Smart contract integration  
- Mobile app support  
- Real-time tracking system  

---

## 👨‍💻 Developer

Sreelatha Budda

---

## 📜 License

This project is for educational purposes only.
