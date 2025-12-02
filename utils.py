import bcrypt
import random
import string
from datetime import datetime
from config import Config

def hash_password(password):
    """Hash a password using bcrypt"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(password, hashed_password):
    """Verify a password against its hash"""
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def generate_roll_number():
    """Generate a unique roll number for students"""
    # Format: OL2025XXXX (OL = O Level, 2025 = year, XXXX = random)
    year = datetime.now().year
    random_part = ''.join(random.choices(string.digits, k=4))
    return f"OL{year}{random_part}"

def calculate_score(questions, answers):
    """
    Calculate exam score
    
    Args:
        questions: List of question documents from database
        answers: Dict of {question_id: selected_option}
    
    Returns:
        tuple: (score, total, percentage)
    """
    score = 0
    total = len(questions)
    
    for question in questions:
        q_id = str(question['_id'])
        if q_id in answers and answers[q_id] == question['correct']:
            score += 1
    
    percentage = (score / total * 100) if total > 0 else 0
    return score, total, round(percentage, 2)

def calculate_grade(percentage):
    """Calculate grade based on percentage"""
    for grade, boundary in Config.GRADE_BOUNDARIES.items():
        if percentage >= boundary:
            return grade
    return 'F'

def format_duration(seconds):
    """Format duration in seconds to readable format"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"

def validate_email(email):
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Basic phone validation (10 digits)"""
    import re
    pattern = r'^\d{10}$'
    return re.match(pattern, phone) is not None

def get_exam_status(start_time, submit_time, duration_minutes):
    """
    Determine exam status
    
    Returns: 'completed', 'in_progress', or 'expired'
    """
    if submit_time:
        return 'completed'
    
    if start_time:
        elapsed = (datetime.now() - start_time).total_seconds()
        if elapsed > duration_minutes * 60:
            return 'expired'
        return 'in_progress'
    
    return 'not_started'

def sanitize_input(text):
    """Sanitize user input to prevent XSS"""
    import html
    return html.escape(str(text).strip())

def format_datetime(dt):
    """Format datetime for display"""
    if isinstance(dt, datetime):
        return dt.strftime('%d-%m-%Y %I:%M %p')
    return str(dt)
