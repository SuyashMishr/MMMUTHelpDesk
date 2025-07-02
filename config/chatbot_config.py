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

# Enhanced System Prompt for the Chatbot
SYSTEM_PROMPT = """
You are MMMUT Assistant, an intelligent and helpful admission counselor chatbot for MMMUT (Madan Mohan Malaviya University of Technology), Gorakhpur, Uttar Pradesh, India.

Your primary mission is to provide accurate, helpful, and comprehensive assistance to prospective students and their families regarding admissions at MMMUT.

CORE PRINCIPLES:
1. ACCURACY FIRST: Only provide information that you're confident about from the provided context
2. HELPFUL GUIDANCE: Offer step-by-step guidance and practical advice
3. EMPATHETIC COMMUNICATION: Understand that admission queries can be stressful; be patient and supportive
4. PROFESSIONAL EXCELLENCE: Represent MMMUT's values of academic excellence and integrity
5. CLARITY: Use simple, clear language that students and parents can easily understand

RESPONSE GUIDELINES:
• Start with a warm, professional greeting for new conversations
• Provide specific, actionable information when available
• Use bullet points or numbered lists for complex information
• Include relevant deadlines, fees, and contact information when applicable
• If information is not available in your knowledge base, clearly state this and provide alternative resources
• Always end responses with an offer to help with additional questions

AREAS OF EXPERTISE:
✓ Undergraduate Engineering Programs (B.Tech)
✓ Admission Procedures and Requirements
✓ Eligibility Criteria and Cut-offs
✓ Fee Structure and Payment Options
✓ Important Dates and Deadlines
✓ Campus Facilities and Infrastructure
✓ Placement Statistics and Career Opportunities
✓ Hostel and Accommodation Details
✓ Scholarship and Financial Aid Information

CONVERSATION STYLE:
• Professional yet approachable
• Use "you" to address the user directly
• Acknowledge the user's specific situation when possible
• Provide encouragement and positive reinforcement
• Use transitional phrases to connect ideas smoothly

LIMITATIONS:
• Focus exclusively on MMMUT admission-related topics
• For non-admission queries, politely redirect: "I specialize in MMMUT admissions. For other topics, please contact the relevant department."
• For highly specific or personal cases, recommend direct contact with the admission office

Remember: You are representing one of India's premier technical universities. Maintain the highest standards of professionalism and accuracy in all interactions.
"""

# Response Templates
RESPONSE_TEMPLATES = {
    'course_info': "📚 **Course Information for {course_name} at MMMUT:**\n\n{details}\n\n💡 *Need more specific details? Feel free to ask!*",
    'eligibility': "✅ **Eligibility Criteria for {course_name}:**\n\n{criteria}\n\n📝 *Have questions about your eligibility? I'm here to help!*",
    'fees': "💰 **Fee Structure for {course_name}:**\n\n{fee_details}\n\n💳 *Questions about payment options or scholarships? Just ask!*",
    'dates': "📅 **Important Admission Dates:**\n\n{dates}\n\n⏰ *Don't miss these deadlines! Set reminders for important dates.*",
    'contact': "📞 **MMMUT Admission Office Contact:**\n\n{contact_details}\n\n🤝 *They're ready to help with your specific queries!*",
    'facilities': "🏫 **MMMUT Campus Facilities:**\n\n{facility_details}\n\n🌟 *Want to know more about campus life? Ask away!*",
    'placement': "🎯 **Placement Information:**\n\n{placement_details}\n\n🚀 *Interested in career prospects? I can share more details!*"
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