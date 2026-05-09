FoodTech Blockchain System (Django Project)
🚀 Project Overview

This is a Food Technology Blockchain-based web application built using Django.
It focuses on improving transparency, security, and traceability in food supply chains using blockchain concepts.

🛠️ Tech Stack
Python 🐍
Django 🌐
SQLite / PostgreSQL 🗄️
HTML, CSS, JavaScript 🎨
Blockchain (custom implementation)
OpenCV (if used in biometric modules)
Gunicorn (deployment)
Whitenoise (static files)
📁 Project Structure
FoodTech/
│
├── FoodTech/          # Django project settings
├── FoodTechApp/       # Main application
│   ├── views.py
│   ├── urls.py
│   ├── models.py
│   └── templates/
│
├── Blockchain.py      # Custom blockchain logic
├── manage.py
└── requirements.txt
⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/your-username/foodtech-blockchain.git
cd foodtech-blockchain
2️⃣ Create virtual environment
python -m venv venv

Activate:

venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Run migrations
python manage.py migrate
5️⃣ Start development server
python manage.py runserver

Open:

http://127.0.0.1:8000/
🌐 Deployment (Render)

Deployed using Render

Start Command:
gunicorn FoodTech.wsgi:application
🔐 Features
Blockchain-based food tracking
Secure data storage
User authentication system
Admin dashboard
Transaction verification system
📦 Requirements

Main dependencies:

Django
gunicorn
whitenoise
pyaes
pbkdf2
pypng
opencv-python-headless
numpy
Pillow
⚠️ Known Issues
Some dependencies must be installed manually (pyaes, pbkdf2, pypng)
SQLite not recommended for production
Better to use PostgreSQL for deployment
🚀 Future Improvements
AI-based food quality detection
Mobile app integration
Smart contract integration
Real-time tracking system
👨‍💻 Author

Sreelatha Budda

📌 License

This project is for educational purposes.
