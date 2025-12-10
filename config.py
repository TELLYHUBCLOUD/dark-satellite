import os
from datetime import timedelta
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
class Config:
    """Base configuration class for the exam portal"""
    
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # MongoDB Configuration
    # For local development
    MONGO_URI_LOCAL = os.environ.get('MONGO_URI_LOCAL') or 'mongodb://localhost:27017/olevel_exam'
    
    # For production (MongoDB Atlas) - MUST BE SET IN VERCEL ENVIRONMENT VARIABLES
    MONGO_URI = os.environ.get('MONGO_URI')
    
    # Use Atlas if available, otherwise local
    if not MONGO_URI:
        MONGO_URI = MONGO_URI_LOCAL
        print("ℹ️  INFO: Using local MongoDB (Offline Mode)")
    else:
        print("✅ INFO: Using production MongoDB")
    
    # Database name
    DB_NAME = 'olevel_exam'
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=3)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Exam settings
    EXAM_DURATION_MINUTES = 100
    TOTAL_QUESTIONS = 20
    PASSING_MARKS = 40
    
    # Pagination
    STUDENTS_PER_PAGE = 20
    
    # File upload settings (for future enhancements)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Admin credentials (default - should be changed)
    DEFAULT_ADMIN_USERNAME = 'admin'
    DEFAULT_ADMIN_PASSWORD = 'admin123'
    
    # Grade boundaries
    GRADE_BOUNDARIES = {
        'A+': 90,
        'A': 80,
        'B': 70,
        'C': 60,
        'D': 50,
        'E': 40,
        'F': 0
    }
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    MONGO_URI = 'mongodb://localhost:27017/olevel_exam_test'
# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
