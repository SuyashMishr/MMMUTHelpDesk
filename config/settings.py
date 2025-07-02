"""
Configuration settings for the MMMUT Admission Chatbot
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent.parent

# API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# File Paths
DATA_DIR = BASE_DIR / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw_data'
STRUCTURED_DATA_FILE = DATA_DIR / 'structured_data.json'

# Ensure directories exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///admission_chatbot.db')

# Flask Configuration
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Supported file formats
SUPPORTED_PDF_FORMATS = ['.pdf']
SUPPORTED_TEXT_FORMATS = ['.txt', '.md']

# Default responses
DEFAULT_RESPONSES = {
    'greeting': "Hello! I'm the MMMUT Admission Help Desk chatbot. How can I assist you with your admission queries today?",
    'fallback': "I'm sorry, I don't have specific information about that. Could you please rephrase your question or ask about admission procedures, eligibility criteria, fees, or important dates?",
    'error': "I apologize, but I'm experiencing some technical difficulties. Please try again in a moment."
}