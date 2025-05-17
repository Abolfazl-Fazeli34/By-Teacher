Teacher Voting System
Welcome to Teacher Voting System — a simple, secure, and fully Persian-language web platform built with Python, Django, HTML, CSS, and Bootstrap, backed by a MySQL database.

🚀 Project Overview
This project enables users to register, verify their email via a security code, and vote fairly for their favorite teachers. The system enforces a strict limit — each user can vote for up to 3 different teachers, and cannot vote multiple times for the same teacher.

Key Features:

Easy and secure user registration with two-step email verification

Vote restriction to a maximum of 3 different teachers

No duplicate votes allowed per teacher

Clean, responsive, and user-friendly Persian interface

Robust security measures for safe and reliable use

🛠 Technologies Used
Python 3.x

Django 5.2.1

HTML5 & CSS3

Bootstrap 5 (for responsive UI)

MySQL (database)

Required Python packages (see requirements.txt):

asgiref==3.8.1

Django==5.2.1

sqlparse==0.5.3

tzdata==2025.2

📥 Installation and Setup
Clone the repository

bash
Copy
Edit
git clone https://your-repo-url.git
cd your-project-folder
Create and activate a virtual environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Configure MySQL database

Create a MySQL database (e.g., teacher_voting_db)

Update settings.py with your MySQL credentials:

python
Copy
Edit
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'teacher_voting_db',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
Apply migrations

bash
Copy
Edit
python manage.py migrate
Run the development server

bash
Copy
Edit
python manage.py runserver
Access the site

Open your browser and navigate to:

cpp
Copy
Edit
http://127.0.0.1:8000/
🔐 Important Notes
Please register with a valid email that has two-step verification enabled.

Your votes are limited to 3 different teachers and duplicates are not allowed.

The system is designed to ensure fairness and security throughout the voting process.

🎉 Join Us!
Become part of this community and help select the best teachers by casting your votes responsibly. Share with friends and make a real difference!

📞 Contact
For questions or support, please contact the project maintainer.

Enjoy voting!
— The Teacher Voting System Team

If you want, I can also generate a requirements.txt file or help with setup instructions for email verification or deployment. Just let me know!
