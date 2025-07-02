"""
Chatbot-specific configuration settings
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Gemini AI Configuration
GEMINI_MODEL = "gemini-1.5-flash"
TEMPERATURE = float(os.getenv('TEMPERATURE', 0.7))
MAX_TOKENS = int(os.getenv('MAX_TOKENS', 1000))
TOP_P = 0.8
TOP_K = 40

# Safety Settings
SAFETY_SETTINGS = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
]

# Generation Configuration
GENERATION_CONFIG = {
    "temperature": TEMPERATURE,
    "top_p": TOP_P,
    "top_k": TOP_K,
    "max_output_tokens": MAX_TOKENS,
}

# System Prompt for the Chatbot
SYSTEM_PROMPT = """
You are an intelligent admission help desk chatbot for MMMUT (Madan Mohan Malaviya University of Technology), Gorakhpur. 
Your role is to assist prospective students with admission-related queries.

Guidelines:
1. Be helpful, friendly, and professional
2. Provide accurate information based on the admission brochure data
3. If you don't know something, admit it and suggest contacting the admission office
4. Keep responses concise but informative
5. Always maintain a positive and encouraging tone
6. Focus only on admission-related topics
7. If asked about non-admission topics, politely redirect to admission queries

Available information categories:
- Course details and eligibility criteria
- Admission procedures and important dates
- Fee structure and payment methods
- University facilities and infrastructure
- Placement information
- Contact details for admission office

Remember: You represent MMMUT, so maintain the university's reputation and values in all interactions.
"""

# Response Templates
RESPONSE_TEMPLATES = {
    'course_info': "Here's information about {course_name} at MMMUT:\n{details}",
    'eligibility': "The eligibility criteria for {course_name} are:\n{criteria}",
    'fees': "The fee structure for {course_name} is:\n{fee_details}",
    'dates': "Important dates for admission:\n{dates}",
    'contact': "You can contact the MMMUT admission office:\n{contact_details}"
}

# Query Categories for Intent Recognition
QUERY_CATEGORIES = {
    'courses': ['course', 'program', 'branch', 'stream', 'degree', 'btech', 'engineering'],
    'eligibility': ['eligibility', 'criteria', 'qualification', 'marks', 'percentage', 'requirement'],
    'fees': ['fee', 'cost', 'payment', 'scholarship', 'financial', 'money'],
    'dates': ['date', 'deadline', 'schedule', 'timeline', 'when', 'last date'],
    'admission': ['admission', 'apply', 'application', 'form', 'procedure', 'process'],
    'facilities': ['facility', 'hostel', 'library', 'lab', 'infrastructure', 'campus'],
    'placement': ['placement', 'job', 'career', 'company', 'recruitment', 'salary'],
    'contact': ['contact', 'phone', 'email', 'address', 'office', 'help']
}

# Confidence Thresholds
MIN_CONFIDENCE_THRESHOLD = 0.6
HIGH_CONFIDENCE_THRESHOLD = 0.8

# Rate Limiting
MAX_REQUESTS_PER_MINUTE = 30
MAX_REQUESTS_PER_HOUR = 500