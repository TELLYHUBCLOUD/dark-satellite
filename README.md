# O Level Exam Portal

A comprehensive Python-based examination portal for O Level Computer Science students with MongoDB database integration, featuring student registration, timed MCQ exams, admin management, and result viewing with premium print layout.

## 🎯 Features

- ✅ **Student Registration** - Secure registration with auto-generated roll numbers
- ✅ **Student Login** - Authentication system with session management
- ✅ **100 MCQ Exam** - Computer Science questions with 100-minute timer
- ✅ **Auto-Save** - Answers saved automatically during exam
- ✅ **Admin Portal** - Complete dashboard with statistics and student management
- ✅ **Result Viewing** - Premium result card with print functionality
- ✅ **Responsive Design** - Works on desktop, tablet, and mobile
- ✅ **Premium UI** - Modern glassmorphism design with smooth animations

## 📋 Requirements

- Python 3.8 or higher
- MongoDB (local or MongoDB Atlas)
- Modern web browser

## 🚀 Local Installation

### Step 1: Install MongoDB

**Windows:**
1. Download MongoDB Community Server from [mongodb.com](https://www.mongodb.com/try/download/community)
2. Install and start MongoDB service
3. MongoDB will run on `mongodb://localhost:27017`

**Alternative:** Use MongoDB Atlas (cloud) - [Sign up free](https://www.mongodb.com/cloud/atlas/register)

### Step 2: Clone/Download Project

```bash
cd dark-satellite
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-this
MONGO_URI=mongodb://localhost:27017/olevel_exam
PORT=5000
```

### Step 5: Seed Database

Populate the database with 100 questions and default admin:

```bash
python seed_data.py
```

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`

⚠️ **IMPORTANT:** Change these credentials after first login!

### Step 6: Run Application

```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## 🌐 Vercel Deployment

### Prerequisites

1. Create a [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register) account (free tier)
2. Create a cluster and get your connection string
3. Install [Vercel CLI](https://vercel.com/download): `npm i -g vercel`

### Deployment Steps

1. **Set up MongoDB Atlas:**
   - Create a new cluster
   - Add database user
   - Whitelist all IPs (0.0.0.0/0) for Vercel
   - Get connection string (format: `mongodb+srv://username:password@cluster.mongodb.net/olevel_exam`)

2. **Seed MongoDB Atlas:**
   
   Update `.env` with Atlas connection string:
   ```env
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/olevel_exam
   ```
   
   Run seed script:
   ```bash
   python seed_data.py
   ```

3. **Deploy to Vercel:**

   ```bash
   vercel
   ```

   Follow the prompts and set environment variables:
   - `FLASK_ENV`: `production`
   - `SECRET_KEY`: (generate a strong random key)
   - `MONGO_URI`: (your MongoDB Atlas connection string)

4. **Access your deployed app:**
   
   Vercel will provide a URL like: `https://your-app.vercel.app`

## 📁 Project Structure

```
dark-satellite/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── models.py              # Database models
├── utils.py               # Utility functions
├── seed_data.py           # Database seeding script
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel deployment config
├── .env.example          # Environment variables template
├── templates/            # HTML templates
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── exam.html
│   ├── result.html
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   └── error.html
└── static/               # Static assets
    ├── css/
    │   └── style.css     # Premium CSS styles
    └── js/
        └── main.js       # JavaScript utilities
```

## 🎓 Usage Guide

### For Students

1. **Register:**
   - Go to `/register`
   - Fill in your details
   - Save your roll number (e.g., OL20251234)

2. **Take Exam:**
   - Login at `/login` with your roll number and password
   - Exam starts automatically
   - Answer all 100 questions within 100 minutes
   - Answers are auto-saved
   - Submit when done

3. **View Result:**
   - After submission, view your result card
   - Print or download your result

### For Admins

1. **Login:**
   - Go to `/admin/login`
   - Use admin credentials

2. **Dashboard:**
   - View statistics (total students, exams, questions)
   - See recent exam results
   - Manage all registered students
   - View detailed results

## 🔒 Security Features

- Password hashing with bcrypt
- Session management
- Input validation and sanitization
- CSRF protection
- Secure admin authentication
- Exam integrity (one attempt per student)

## 🎨 Design Features

- Modern glassmorphism UI
- Smooth gradient backgrounds
- Animated components
- Responsive design
- Print-optimized result cards
- Dark theme with vibrant accents

## 📊 Database Schema

### Collections

- **students** - Student registration data
- **questions** - MCQ question bank (100 questions)
- **exams** - Exam sessions and answers
- **admins** - Admin users

## 🛠️ Troubleshooting

### MongoDB Connection Error

- Ensure MongoDB is running: `mongod --version`
- Check connection string in `.env`
- For Atlas: Verify IP whitelist and credentials

### Port Already in Use

Change port in `.env`:
```env
PORT=5001
```

### Vercel Deployment Issues

- Ensure all environment variables are set in Vercel dashboard
- Check MongoDB Atlas IP whitelist includes 0.0.0.0/0
- Verify connection string format

## 📝 Exam Information

- **Total Questions:** 100
- **Duration:** 100 minutes
- **Format:** Multiple Choice (A, B, C, D)
- **Passing Marks:** 40%
- **Subjects Covered:**
  - Computer Fundamentals (20 questions)
  - Programming Concepts (20 questions)
  - Database Concepts (15 questions)
  - Networking (15 questions)
  - Operating Systems (10 questions)
  - Web Technologies (10 questions)
  - Security & Ethics (10 questions)

## 🔄 Grade Boundaries

- **A+:** 90% and above
- **A:** 80-89%
- **B:** 70-79%
- **C:** 60-69%
- **D:** 50-59%
- **E:** 40-49%
- **F:** Below 40% (Fail)

## 📞 Support

For issues or questions:
1. Check this README
2. Review error messages
3. Check MongoDB connection
4. Verify environment variables

## 📄 License

This project is created for educational purposes.

## 🎉 Credits

Developed for O Level Computer Science examination.

---

**Made with ❤️ for students**
