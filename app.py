from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime, timedelta
from bson.objectid import ObjectId
import os

from config import config
from models import db_manager, Student, Question, Exam, Admin
from utils import (
    validate_email, validate_phone, calculate_score, 
    calculate_grade, sanitize_input, get_exam_status, format_datetime
)

# Initialize Flask app
app = Flask(__name__)

# Load configuration
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Database will connect lazily on first use (important for serverless deployment)

# ==================== HELPER FUNCTIONS ====================

def login_required(f):
    """Decorator to require student login"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'student_roll' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin login"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_username' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== INITIALIZATION ====================

_initialized = False

def ensure_initialized():
    """Ensure database is initialized (lazy initialization for serverless)"""
    global _initialized
    if not _initialized:
        try:
            db_manager.connect()
            Admin.ensure_default_admin()
            _initialized = True
        except Exception as e:
            print(f"Initialization warning: {e}")
            # Don't fail on initialization errors in serverless environment

@app.before_request
def before_request():
    """Run before each request"""
    ensure_initialized()

# ==================== MAIN ROUTES ====================

@app.route('/')
def index():
    """Landing page"""
    subjects = Question.get_subjects()
    return render_template('index.html', subjects=subjects)

# ==================== STUDENT ROUTES ====================

@app.route('/register')
def register_page():
    """Student registration page"""
    return render_template('register.html')

@app.route('/api/register', methods=['POST'])
def register():
    """Student registration API"""
    try:
        data = request.get_json()
        
        # Validate input
        name = sanitize_input(data.get('name', ''))
        email = sanitize_input(data.get('email', ''))
        password = data.get('password', '')
        phone = sanitize_input(data.get('phone', ''))
        
        # Validation
        if not all([name, email, password, phone]):
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        
        if not validate_email(email):
            return jsonify({'success': False, 'message': 'Invalid email format'}), 400
        
        if not validate_phone(phone):
            return jsonify({'success': False, 'message': 'Phone must be 10 digits'}), 400
        
        if len(password) < 6:
            return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400
        
        # Create student
        student, error = Student.create(name, email, password, phone)
        
        if error:
            return jsonify({'success': False, 'message': error}), 400
        
        return jsonify({
            'success': True,
            'message': 'Registration successful!',
            'roll_number': student['roll_number']
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/login')
def login_page():
    """Student login page"""
    if 'student_roll' in session:
        return redirect(url_for('subjects_page'))
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def login():
    """Student login API"""
    try:
        data = request.get_json()
        
        roll_number = sanitize_input(data.get('roll_number', ''))
        password = data.get('password', '')
        
        if not all([roll_number, password]):
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        
        # Authenticate student
        student = Student.authenticate(roll_number, password)
        
        if not student:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        
        # Check if already taken exam - REMOVED for multi-subject support
        # if student.get('exam_taken'):
        #     return jsonify({
        #         'success': False,
        #         'message': 'You have already taken the exam',
        #         'redirect': '/result/' + roll_number
        #     }), 403
        
        # Set session
        session['student_roll'] = roll_number
        session['student_name'] = student['name']
        session.permanent = True
        
        return jsonify({
            'success': True,
            'message': 'Login successful!',
            'redirect': '/subjects'
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/logout')
def logout():
    """Student logout"""
    session.pop('student_roll', None)
    session.pop('student_name', None)
    return redirect(url_for('index'))

# ==================== EXAM ROUTES ====================

@app.route('/subjects')
@login_required
def subjects_page():
    """Subjects selection page"""
    subjects = Question.get_subjects()
    return render_template('subjects.html', subjects=subjects)

@app.route('/exam/<subject>')
@login_required
def exam_page(subject):
    """Exam interface page"""
    student_roll = session.get('student_roll')
    
    # Check if exam already exists
    existing_exam = Exam.get_by_student(student_roll)
    
    if existing_exam and existing_exam['status'] == 'completed':
        return redirect(url_for('result_page', roll_number=student_roll))
    
    return render_template('exam.html', 
                         student_name=session.get('student_name'),
                         duration=app.config['EXAM_DURATION_MINUTES'],
                         subject=subject)

@app.route('/api/start_exam/<subject>', methods=['POST'])
@login_required
def start_exam(subject):
    """Start exam and get questions for a specific subject"""
    try:
        student_roll = session.get('student_roll')
        
        # Check if exam already exists for this subject
        existing_exam = Exam.get_by_student_and_subject(student_roll, subject)
        
        if existing_exam:
            if existing_exam['status'] == 'completed':
                return jsonify({
                    'success': False,
                    'message': 'Exam already completed for this subject',
                    'redirect': '/result/' + student_roll
                }), 403
            
            # Return existing exam
            questions = Question.get_all()
            question_map = {str(q['_id']): q for q in questions}
            
            exam_questions = []
            for q_id in existing_exam['questions']:
                if q_id in question_map:
                    q = question_map[q_id]
                    exam_questions.append({
                        'id': str(q['_id']),
                        'question': q['question'],
                        'options': q['options']
                    })
            
            # Calculate remaining time
            elapsed = (datetime.now() - existing_exam['start_time']).total_seconds()
            remaining = max(0, app.config['EXAM_DURATION_MINUTES'] * 60 - elapsed)
            
            return jsonify({
                'success': True,
                'questions': exam_questions,
                'remaining_time': int(remaining),
                'saved_answers': existing_exam.get('answers', {})
            }), 200
        
        # Get random questions by subject
        questions = Question.get_random_by_subject(subject, app.config['TOTAL_QUESTIONS'])
        
        if len(questions) < app.config['TOTAL_QUESTIONS']:
            return jsonify({
                'success': False,
                'message': f'Not enough questions in database for subject {subject}. Need {app.config["TOTAL_QUESTIONS"]}, found {len(questions)}'
            }), 500
        
        # Create exam
        exam, error = Exam.create(student_roll, subject, questions)
        
        if error:
            return jsonify({'success': False, 'message': error}), 400
        
        # Format questions for frontend (without correct answers)
        exam_questions = [{
            'id': str(q['_id']),
            'question': q['question'],
            'options': q['options']
        } for q in questions]
        
        return jsonify({
            'success': True,
            'questions': exam_questions,
            'remaining_time': app.config['EXAM_DURATION_MINUTES'] * 60,
            'saved_answers': {}
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/save_answer', methods=['POST'])
@login_required
def save_answer():
    """Save individual answer"""
    try:
        data = request.get_json()
        student_roll = session.get('student_roll')
        
        question_id = data.get('question_id')
        answer = data.get('answer')
        
        if not all([question_id, answer]):
            return jsonify({'success': False, 'message': 'Invalid data'}), 400
        
        Exam.save_answer(student_roll, question_id, answer)
        
        return jsonify({'success': True}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/submit_exam', methods=['POST'])
@login_required
def submit_exam():
    """Submit exam and calculate results"""
    try:
        student_roll = session.get('student_roll')
        
        # Get active exam
        exam = Exam.get_active_exam(student_roll)
        
        if not exam:
            return jsonify({'success': False, 'message': 'Exam not found'}), 404
        
        if exam['status'] == 'completed':
            return jsonify({'success': False, 'message': 'Exam already submitted'}), 400
        
        # Get all questions
        questions = Question.get_all()
        question_map = {str(q['_id']): q for q in questions}
        
        # Get exam questions
        exam_questions = [question_map[q_id] for q_id in exam['questions'] if q_id in question_map]
        
        # Calculate score
        score, total, percentage = calculate_score(exam_questions, exam.get('answers', {}))
        grade = calculate_grade(percentage)
        
        # Submit exam
        Exam.submit(student_roll, score, total, percentage, grade)
        
        return jsonify({
            'success': True,
            'message': 'Exam submitted successfully!',
            'redirect': '/result/' + student_roll
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== RESULT ROUTES ====================

@app.route('/result/<roll_number>')
def result_page(roll_number):
    """View result page"""
    try:
        # Get student
        student = Student.get_by_roll(roll_number)
        
        if not student:
            return render_template('error.html', message='Student not found'), 404
        
        # Get exams
        exams = Exam.get_by_student(roll_number)
        
        if not exams:
            return render_template('error.html', message='No exams found'), 404
        
        # Prepare result data
        results = []
        for exam in exams:
            if exam['status'] == 'completed':
                results.append({
                    'roll_number': roll_number,
                    'name': student['name'],
                    'email': student['email'],
                    'subject': exam.get('subject', 'Unknown'),
                    'score': exam['score'],
                    'total': exam['total'],
                    'percentage': exam['percentage'],
                    'grade': exam['grade'],
                    'exam_date': format_datetime(exam['submit_time']),
                    'status': 'PASS' if exam['percentage'] >= app.config['PASSING_MARKS'] else 'FAIL'
                })
        
        if not results:
             return render_template('error.html', message='Result not available yet'), 404

        return render_template('result.html', results=results, student=student)
        
    except Exception as e:
        return render_template('error.html', message=str(e)), 500

# ==================== ADMIN ROUTES ====================

@app.route('/admin/login')
def admin_login_page():
    """Admin login page"""
    if 'admin_username' in session:
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """Admin login API"""
    try:
        data = request.get_json()
        
        username = sanitize_input(data.get('username', ''))
        password = data.get('password', '')
        
        if not all([username, password]):
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        
        # Authenticate admin
        admin = Admin.authenticate(username, password)
        
        if not admin:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        
        # Set session
        session['admin_username'] = username
        session.permanent = True
        
        return jsonify({
            'success': True,
            'message': 'Login successful!',
            'redirect': '/admin/dashboard'
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_username', None)
    return redirect(url_for('admin_login_page'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    try:
        # Get statistics
        total_students = Student.count()
        total_exams = Exam.count_completed()
        total_questions = Question.count()
        
        # Get recent results
        recent_results = Exam.get_all_results(limit=10)
        
        # Enrich with student data
        for result in recent_results:
            student = Student.get_by_roll(result['student_roll'])
            result['student_name'] = student['name'] if student else 'Unknown'
            result['exam_date'] = format_datetime(result['submit_time'])
        
        stats = {
            'total_students': total_students,
            'total_exams': total_exams,
            'total_questions': total_questions,
            'recent_results': recent_results
        }
        
        return render_template('admin_dashboard.html', 
                             admin_username=session.get('admin_username'),
                             stats=stats)
        
    except Exception as e:
        return render_template('error.html', message=str(e)), 500

@app.route('/api/admin/students')
@admin_required
def get_students():
    """Get all students (API)"""
    try:
        page = int(request.args.get('page', 1))
        per_page = app.config['STUDENTS_PER_PAGE']
        
        students = Student.get_all(skip=(page-1)*per_page, limit=per_page)
        total = Student.count()
        
        # Format students
        student_list = []
        for student in students:
            student_list.append({
                'roll_number': student['roll_number'],
                'name': student['name'],
                'email': student['email'],
                'phone': student['phone'],
                'exam_taken': student.get('exam_taken', False),
                'registered_at': format_datetime(student['created_at'])
            })
        
        return jsonify({
            'success': True,
            'students': student_list,
            'total': total,
            'page': page,
            'pages': (total + per_page - 1) // per_page
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/admin/questions', methods=['GET'])
@admin_required
def get_questions():
    """Get all questions (API)"""
    try:
        page = int(request.args.get('page', 1))
        per_page = app.config['QUESTIONS_PER_PAGE']
        
        questions = Question.get_all_questions(skip=(page-1)*per_page, limit=per_page)
        total = Question.count()
        
        # Format questions
        question_list = []
        for q in questions:
            question_list.append({
                'id': str(q['_id']),
                'question': q['question'],
                'subject': q['subject'],
                'options': q['options'],
                'correct': q['correct']
            })
        
        return jsonify({
            'success': True,
            'questions': question_list,
            'total': total,
            'page': page,
            'pages': (total + per_page - 1) // per_page
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/admin/questions', methods=['POST'])
@admin_required
def add_question():
    """Add a new question (API)"""
    try:
        data = request.get_json()
        
        question_text = sanitize_input(data.get('question', ''))
        options = data.get('options', [])
        correct_answer = sanitize_input(data.get('correct', ''))
        subject = sanitize_input(data.get('subject', ''))
        
        if not all([question_text, options, correct_answer, subject]):
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        
        if len(options) != 4:
            return jsonify({'success': False, 'message': 'There must be 4 options'}), 400

        Question.create(question_text, options, correct_answer, subject)
        
        return jsonify({'success': True, 'message': 'Question added successfully'}), 201
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/admin/questions/<question_id>', methods=['DELETE'])
@admin_required
def delete_question(question_id):
    """Delete a question (API)"""
    try:
        if not ObjectId.is_valid(question_id):
            return jsonify({'success': False, 'message': 'Invalid Question ID'}), 400
        
        if Question.delete_question(question_id):
            return jsonify({'success': True, 'message': 'Question deleted successfully'}), 200
        else:
            return jsonify({'success': False, 'message': 'Question not found'}), 404
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/admin/reset_exam', methods=['POST'])
@admin_required
def reset_exam():
    """Reset exam for a student and subject"""
    try:
        data = request.get_json()
        student_roll = data.get('student_roll')
        subject = data.get('subject')
        
        if not all([student_roll, subject]):
            return jsonify({'success': False, 'message': 'Student Roll and Subject are required'}), 400
            
        if Exam.delete_exam(student_roll, subject):
            return jsonify({'success': True, 'message': 'Exam reset successfully'}), 200
        else:
            return jsonify({'success': False, 'message': 'Exam not found'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', message='Page not found'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', message='Internal server error'), 500

# ==================== RUN APP ====================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

