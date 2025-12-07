# O Level Exam Portal - Oxford Group of Institution

A comprehensive web-based Online Examination System designed for NIELIT O Level certification practice. This portal allows students to register, take subject-specific exams, and view instant results in an official certificate format. It also includes a robust Admin Panel for student and question management.

**Made By:** Ravi Kumar

## 🌟 Key Features

### 🎓 Student Features
*   **Secure Authentication**: Student Registration and Login with DOB verification.
*   **Modern Dashboard**: clean, responsive interface with a sliding sidebar menu.
*   **Exam Interface**:
    *   Subject selection (M1-R5, M2-R5, etc.).
    *   Real-time timer.
    *   Interactive question navigation.
    *   Instant submission and grading.
*   **Official Result**: Generates a result sheet matching the official NIELIT O Level certificate format.
*   **Typing Effects**: Engaging typing animations on the home page.

### 🛡️ Admin Features
*   **Secure Admin Login**: Dedicated admin authentication.
*   **Dashboard**: Overview of total students, exams taken, and questions.
*   **Student Management**: View all registered students, their passwords (hashed/truncated), and delete registrations.
*   **Question Management**: Add, view, and delete exam questions.
*   **Exam Resets**: Ability to reset a student's exam status.

### 👨‍💻 Developer Portfolio
*   **Dedicated Page**: Accessible via `/portfolio` or the Sidebar.
*   **Profile**: Showcases the developer's skills, experience, and contact details.

## 🛠️ Technology Stack

*   **Backend**: Python (Flask)
*   **Database**: MongoDB (Atlas/Local)
*   **Frontend**: HTML5, CSS3 (Glassmorphism), JavaScript (Vanilla)
*   **Deployment**: Vercel-ready

## 🚀 Installation & Setup

### Prerequisites
*   Python 3.x
*   MongoDB Connection String

### 1. Clone the Repository
```bash
git clone <repository-url>
cd dark-satellite
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file or set environment variables:
```bash
MONGO_URI="your_mongodb_connection_string"
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY="your_secret_key"
```

### 4. Run the Application
```bash
python app.py
```
Access the portal at `http://localhost:5000`.

## 📖 Usage Guide

### For Students
1.  **Register**: Create a new account with your Roll Number, Email, and DOB.
2.  **Login**: Use your Roll Number, Password, and DOB to log in.
3.  **Start Exam**: Select a subject from the home page or dashboard and click "Start Exam".
4.  **View Result**: After submitting, your graded result sheet will be displayed instantly.

### For Admins
1.  **Login**: Go to `/admin/login`.
2.  **Default Credentials**: (Check `config.py` or database for initial setup, usually `admin`/`admin123` if configured as default).
3.  **Manage**: Use the dashboard to oversee the system.

## 📂 Project Structure
```
dark-satellite/
├── app.py              # Main Flask Application
├── models.py           # Database Models (Student, Exam, Question)
├── config.py           # Configuration Settings
├── utils.py            # Utility Functions
├── templates/          # HTML Templates (index, exam, result, admin)
├── static/             # CSS, JS, Images
│   ├── css/style.css
│   └── js/main.js
└── requirements.txt    # Python Dependencies
```

---
*© 2025 Oxford Group of Institution. Developed by Ravi Kumar.*
