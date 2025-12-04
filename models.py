from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
import os
from config import Config
from utils import hash_password, verify_password, generate_roll_number

class Database:
    """Database connection manager"""
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def connect(self, mongo_uri=None):
        """Connect to MongoDB"""
        if self._client is None:
            uri = mongo_uri or Config.MONGO_URI
            # Serverless-friendly settings with shorter timeouts
            self._client = MongoClient(
                uri,
                serverSelectionTimeoutMS=5000,  # 5 seconds
                connectTimeoutMS=5000,
                socketTimeoutMS=5000,
                maxPoolSize=1  # Limit connections for serverless
            )
            self._db = self._client[Config.DB_NAME]
        return self._db
    
    def get_db(self):
        """Get database instance"""
        if self._db is None:
            self.connect()
        return self._db
    
    def close(self):
        """Close database connection"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None

# Initialize database
db_manager = Database()

class Student:
    """Student model"""
    
    @staticmethod
    def create(name, email, password, phone):
        """Create a new student"""
        db = db_manager.get_db()
        
        # Check if email already exists
        if db.students.find_one({'email': email}):
            return None, "Email already registered"
        
        # Generate unique roll number
        while True:
            roll_number = generate_roll_number()
            if not db.students.find_one({'roll_number': roll_number}):
                break
        
        student = {
            'roll_number': roll_number,
            'name': name,
            'email': email,
            'password': hash_password(password),
            'phone': phone,
            'created_at': datetime.now(),
            'exam_taken': False
        }
        
        result = db.students.insert_one(student)
        student['_id'] = result.inserted_id
        return student, None
    
    @staticmethod
    def authenticate(roll_number, password):
        """Authenticate student"""
        db = db_manager.get_db()
        student = db.students.find_one({'roll_number': roll_number})
        
        if student and verify_password(password, student['password']):
            return student
        return None
    
    @staticmethod
    def get_by_roll(roll_number):
        """Get student by roll number"""
        db = db_manager.get_db()
        return db.students.find_one({'roll_number': roll_number})
    
    @staticmethod
    def get_by_id(student_id):
        """Get student by ID"""
        db = db_manager.get_db()
        return db.students.find_one({'_id': ObjectId(student_id)})
    
    @staticmethod
    def get_all(skip=0, limit=20):
        """Get all students with pagination"""
        db = db_manager.get_db()
        return list(db.students.find().skip(skip).limit(limit))
    
    @staticmethod
    def count():
        """Count total students"""
        db = db_manager.get_db()
        return db.students.count_documents({})
    
    @staticmethod
    def mark_exam_taken(roll_number):
        """Mark that student has taken exam"""
        db = db_manager.get_db()
        db.students.update_one(
            {'roll_number': roll_number},
            {'$set': {'exam_taken': True}}
        )

class Question:
    """Question model"""
    
    @staticmethod
    def create(question_text, options, correct_answer, subject):
        """Create a new question"""
        db = db_manager.get_db()
        
        question = {
            'question': question_text,
            'options': options,  # List of 4 options
            'correct': correct_answer,  # 'A', 'B', 'C', or 'D'
            'subject': subject,
            'created_at': datetime.now()
        }
        
        result = db.questions.insert_one(question)
        return result.inserted_id
    
    @staticmethod
    def get_all():
        """Get all questions"""
        db = db_manager.get_db()
        return list(db.questions.find())
    
    @staticmethod
    def get_random(count=100):
        """Get random questions for exam"""
        db = db_manager.get_db()
        return list(db.questions.aggregate([{'$sample': {'size': count}}]))
    
    @staticmethod
    def get_subjects():
        """Get a list of distinct subjects"""
        db = db_manager.get_db()
        return db.questions.distinct('subject')

    @staticmethod
    def get_random_by_subject(subject, count=100):
        """Get random questions for a specific subject"""
        db = db_manager.get_db()
        return list(db.questions.aggregate([
            {'$match': {'subject': subject}},
            {'$sample': {'size': count}}
        ]))
    
    @staticmethod
    def get_all_questions(skip=0, limit=20):
        """Get all questions with pagination"""
        db = db_manager.get_db()
        return list(db.questions.find().skip(skip).limit(limit))

    @staticmethod
    def delete_question(question_id):
        """Delete a question by its ID"""
        db = db_manager.get_db()
        result = db.questions.delete_one({'_id': ObjectId(question_id)})
        return result.deleted_count > 0
    
    @staticmethod
    def count():
        """Count total questions"""
        db = db_manager.get_db()
        return db.questions.count_documents({})

class Exam:
    """Exam model"""
    
    @staticmethod
    def create(student_roll, questions):
        """Create a new exam session"""
        db = db_manager.get_db()
        
        # Check if student already has an exam
        existing = db.exams.find_one({'student_roll': student_roll})
        if existing:
            return existing, "Exam already taken"
        
        exam = {
            'student_roll': student_roll,
            'questions': [str(q['_id']) for q in questions],  # Store question IDs
            'answers': {},  # Will store {question_id: selected_option}
            'start_time': datetime.now(),
            'submit_time': None,
            'score': None,
            'total': len(questions),
            'percentage': None,
            'grade': None,
            'status': 'in_progress'
        }
        
        result = db.exams.insert_one(exam)
        exam['_id'] = result.inserted_id
        return exam, None
    
    @staticmethod
    def get_by_student(student_roll):
        """Get exam by student roll number"""
        db = db_manager.get_db()
        return db.exams.find_one({'student_roll': student_roll})
    
    @staticmethod
    def save_answer(student_roll, question_id, answer):
        """Save a single answer"""
        db = db_manager.get_db()
        db.exams.update_one(
            {'student_roll': student_roll},
            {'$set': {f'answers.{question_id}': answer}}
        )
    
    @staticmethod
    def submit(student_roll, score, total, percentage, grade):
        """Submit exam and calculate results"""
        db = db_manager.get_db()
        
        result = db.exams.update_one(
            {'student_roll': student_roll},
            {'$set': {
                'submit_time': datetime.now(),
                'score': score,
                'total': total,
                'percentage': percentage,
                'grade': grade,
                'status': 'completed'
            }}
        )
        
        # Mark student as having taken exam
        Student.mark_exam_taken(student_roll)
        
        return result.modified_count > 0
    
    @staticmethod
    def get_all_results(skip=0, limit=20):
        """Get all exam results with pagination"""
        db = db_manager.get_db()
        return list(db.exams.find({'status': 'completed'}).skip(skip).limit(limit))
    
    @staticmethod
    def count_completed():
        """Count completed exams"""
        db = db_manager.get_db()
        return db.exams.count_documents({'status': 'completed'})

class Admin:
    """Admin model"""
    
    @staticmethod
    def create(username, password, role='admin'):
        """Create admin user"""
        db = db_manager.get_db()
        
        # Check if admin exists
        if db.admins.find_one({'username': username}):
            return None, "Admin already exists"
        
        admin = {
            'username': username,
            'password': hash_password(password),
            'role': role,
            'created_at': datetime.now()
        }
        
        result = db.admins.insert_one(admin)
        return result.inserted_id, None
    
    @staticmethod
    def authenticate(username, password):
        """Authenticate admin"""
        db = db_manager.get_db()
        admin = db.admins.find_one({'username': username})
        
        if admin and verify_password(password, admin['password']):
            return admin
        return None
    
    @staticmethod
    def ensure_default_admin():
        """Ensure default admin exists"""
        try:
            db = db_manager.get_db()
            
            if db.admins.count_documents({}) == 0:
                Admin.create(Config.DEFAULT_ADMIN_USERNAME, Config.DEFAULT_ADMIN_PASSWORD)
        except Exception as e:
            # In serverless environments, this might fail on cold start
            # The admin will be created on first successful connection
            print(f"Could not ensure default admin: {e}")
            pass
