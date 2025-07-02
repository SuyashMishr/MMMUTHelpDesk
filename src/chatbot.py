"""
Main chatbot module using Google Gemini AI for MMMUT admission queries
"""

import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import google.generativeai as genai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdmissionChatbot:
    """MMMUT Admission Chatbot using Google Gemini AI"""
    
    def __init__(self):
        """Initialize the chatbot"""
        self._setup_gemini()
        self._load_data()
        self._setup_conversation_history()
        
        logger.info("MMMUT Admission Chatbot initialized successfully")
    
    def _setup_gemini(self):
        """Setup Google Gemini AI"""
        try:
            from config.settings import GEMINI_API_KEY
            from config.chatbot_config import (
                GEMINI_MODEL, GENERATION_CONFIG, SAFETY_SETTINGS, SYSTEM_PROMPT
            )
            
            # Configure Gemini
            genai.configure(api_key=GEMINI_API_KEY)
            
            # Initialize the model
            self.model = genai.GenerativeModel(
                model_name=GEMINI_MODEL,
                generation_config=GENERATION_CONFIG,
                safety_settings=SAFETY_SETTINGS
            )
            
            # Start chat session with system prompt
            self.chat = self.model.start_chat(history=[])
            self.system_prompt = SYSTEM_PROMPT
            
            logger.info("Gemini AI configured successfully")
            
        except Exception as e:
            logger.error(f"Error setting up Gemini AI: {str(e)}")
            raise
    
    def _load_data(self):
        """Load organized admission data"""
        try:
            from config.settings import DATA_DIR
            
            # Try to load organized data first
            organized_data_path = DATA_DIR / "organized_data.json"
            if organized_data_path.exists():
                with open(organized_data_path, 'r', encoding='utf-8') as f:
                    self.organized_data = json.load(f)
            else:
                # Fallback to structured data
                structured_data_path = DATA_DIR / "structured_data.json"
                with open(structured_data_path, 'r', encoding='utf-8') as f:
                    raw_data = json.load(f)
                
                # Create basic organized structure
                self.organized_data = self._create_basic_organized_data(raw_data)
            
            # Load quick responses
            self.quick_responses = self.organized_data.get("quick_responses", {})
            self.faqs = self.organized_data.get("faq", [])
            
            logger.info("Admission data loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            # Create minimal fallback data
            self._create_fallback_data()
    
    def _create_basic_organized_data(self, raw_data: Dict) -> Dict:
        """Create basic organized data structure from raw data"""
        return {
            "categories": {
                "university": {"data": raw_data.get("university_info", {})},
                "courses": {"data": {"undergraduate": {"engineering": raw_data.get("courses", [])}}},
                "eligibility": {"data": raw_data.get("eligibility", {})},
                "fees": {"data": raw_data.get("fees", {})},
                "important_dates": {"data": raw_data.get("important_dates", {})},
                "facilities": {"data": raw_data.get("facilities", [])},
                "placement": {"data": raw_data.get("placement_info", {})},
                "contact": {"data": raw_data.get("contact_info", {})}
            },
            "quick_responses": {
                "greeting": "Hello! Welcome to MMMUT Admission Help Desk. How can I assist you today?",
                "fallback": "I'm sorry, I don't have specific information about that. Could you please ask about courses, eligibility, fees, or other admission-related topics?"
            },
            "faq": []
        }
    
    def _create_fallback_data(self):
        """Create minimal fallback data when no data files are available"""
        self.organized_data = {
            "categories": {
                "university": {
                    "data": {
                        "name": "Madan Mohan Malaviya University of Technology",
                        "location": "Gorakhpur, Uttar Pradesh"
                    }
                }
            },
            "quick_responses": {
                "greeting": "Hello! Welcome to MMMUT Admission Help Desk. How can I assist you today?",
                "fallback": "I'm sorry, I'm experiencing some technical difficulties. Please try again later or contact the admission office directly."
            },
            "faq": []
        }
        self.quick_responses = self.organized_data["quick_responses"]
        self.faqs = self.organized_data["faq"]
    
    def _setup_conversation_history(self):
        """Setup conversation history tracking"""
        self.conversation_history = []
        self.session_start_time = datetime.now()
        self.query_count = 0
    
    def process_query(self, user_query: str, user_id: str = None) -> Dict[str, Any]:
        """Process user query and return response"""
        try:
            self.query_count += 1
            
            # Log the query
            logger.info(f"Processing query: {user_query[:100]}...")
            
            # Preprocess the query
            processed_query = self._preprocess_query(user_query)
            
            # Check for quick responses
            quick_response = self._check_quick_responses(processed_query)
            if quick_response:
                response_data = {
                    "response": quick_response,
                    "response_type": "quick",
                    "confidence": 0.9,
                    "sources": ["quick_responses"],
                    "timestamp": datetime.now().isoformat()
                }
            else:
                # Generate AI response
                response_data = self._generate_ai_response(processed_query)
            
            # Add to conversation history
            self._add_to_history(user_query, response_data["response"])
            
            # Add metadata
            response_data.update({
                "query_id": f"q_{self.query_count}_{int(datetime.now().timestamp())}",
                "user_id": user_id,
                "session_duration": str(datetime.now() - self.session_start_time)
            })
            
            return response_data
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return self._create_error_response(str(e))
    
    def _preprocess_query(self, query: str) -> str:
        """Enhanced preprocessing for better query understanding"""
        # Basic cleaning
        query = query.strip()
        if not query:
            return query

        # Preserve original case for proper nouns but create lowercase version for processing
        original_query = query
        query_lower = query.lower()

        # Remove extra spaces and normalize punctuation
        query_lower = re.sub(r'\s+', ' ', query_lower)
        query_lower = re.sub(r'[^\w\s\-\.]', ' ', query_lower)

        # Handle common abbreviations and expansions
        abbreviations = {
            'cse': 'computer science engineering',
            'ece': 'electronics and communication engineering',
            'eee': 'electrical and electronics engineering',
            'ee': 'electrical engineering',
            'me': 'mechanical engineering',
            'ce': 'civil engineering',
            'it': 'information technology',
            'btech': 'bachelor of technology',
            'b.tech': 'bachelor of technology',
            'mtech': 'master of technology',
            'm.tech': 'master of technology',
            'phd': 'doctor of philosophy',
            'ph.d': 'doctor of philosophy',
            'mmmut': 'madan mohan malaviya university of technology',
            'gorakhpur': 'gorakhpur uttar pradesh',
            'up': 'uttar pradesh'
        }

        # Apply abbreviation expansions
        for abbr, full_form in abbreviations.items():
            query_lower = re.sub(r'\b' + re.escape(abbr) + r'\b', full_form, query_lower)

        # Handle common question patterns
        question_patterns = {
            r'\bwhat\s+is\s+the\s+': 'tell me about the ',
            r'\bhow\s+much\s+': 'what is the cost of ',
            r'\bwhen\s+is\s+': 'what are the dates for ',
            r'\bwhere\s+is\s+': 'what is the location of ',
            r'\bcan\s+i\s+': 'am i eligible for ',
            r'\bdo\s+you\s+have\s+': 'does mmmut offer '
        }

        for pattern, replacement in question_patterns.items():
            query_lower = re.sub(pattern, replacement, query_lower)

        # Return processed query while preserving some original formatting
        return query_lower
    
    def _check_quick_responses(self, query: str) -> Optional[str]:
        """Check if query matches any quick response patterns with improved matching"""
        # Enhanced greeting patterns
        greeting_patterns = [
            'hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening',
            'namaste', 'greetings', 'start', 'begin', 'help me'
        ]
        if any(pattern in query for pattern in greeting_patterns):
            return self.quick_responses.get("greeting",
                "Hello! Welcome to MMMUT Admission Help Desk. I'm here to assist you with all your admission-related queries. How can I help you today?")

        # Enhanced category-specific patterns with better matching
        category_patterns = {
            'courses': [
                'course', 'program', 'branch', 'stream', 'what courses', 'engineering',
                'btech', 'b.tech', 'degree', 'specialization', 'department'
            ],
            'eligibility': [
                'eligibility', 'criteria', 'qualification', 'requirement', 'marks',
                'percentage', 'cutoff', 'cut off', 'minimum marks', 'qualify'
            ],
            'fees': [
                'fee', 'cost', 'payment', 'how much', 'price', 'tuition',
                'scholarship', 'financial aid', 'installment', 'money'
            ],
            'dates': [
                'date', 'deadline', 'when', 'schedule', 'timeline', 'last date',
                'application date', 'admission date', 'important dates'
            ],
            'contact': [
                'contact', 'phone', 'email', 'address', 'reach', 'office',
                'helpline', 'support', 'call', 'write'
            ],
            'facilities': [
                'facility', 'hostel', 'library', 'lab', 'infrastructure',
                'campus', 'accommodation', 'mess', 'wifi', 'sports'
            ],
            'placement': [
                'placement', 'job', 'career', 'salary', 'package', 'company',
                'recruitment', 'internship', 'employment'
            ],
            'location': [
                'where', 'location', 'address', 'situated', 'gorakhpur',
                'how to reach', 'directions'
            ]
        }

        # Score-based matching for better accuracy
        best_match = None
        best_score = 0

        for category, patterns in category_patterns.items():
            score = sum(1 for pattern in patterns if pattern in query)
            if score > best_score:
                best_score = score
                best_match = category

        if best_match and best_score > 0:
            response = self.quick_responses.get(best_match)
            if response:
                return response

        return None
    
    def _generate_ai_response(self, query: str) -> Dict[str, Any]:
        """Generate response using Gemini AI"""
        try:
            # Create context from organized data
            context = self._create_context_for_query(query)
            
            # Prepare the prompt
            prompt = self._create_prompt(query, context)
            
            # Generate response using Gemini
            response = self.chat.send_message(prompt)
            
            # Process the response
            ai_response = response.text.strip()
            
            return {
                "response": ai_response,
                "response_type": "ai_generated",
                "confidence": 0.8,
                "sources": ["gemini_ai", "admission_data"],
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating AI response: {str(e)}")
            return {
                "response": self.quick_responses.get("fallback", "I'm sorry, I'm having trouble processing your request right now."),
                "response_type": "fallback",
                "confidence": 0.1,
                "sources": ["fallback"],
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
    def _create_context_for_query(self, query: str) -> str:
        """Create relevant context from organized data for the query"""
        context_parts = []
        
        # Add university info
        university_data = self.organized_data.get("categories", {}).get("university", {}).get("data", {})
        if university_data:
            context_parts.append(f"University Information: {json.dumps(university_data, indent=2)}")
        
        # Determine relevant categories based on query keywords
        relevant_categories = self._identify_relevant_categories(query)
        
        for category in relevant_categories:
            category_data = self.organized_data.get("categories", {}).get(category, {}).get("data", {})
            if category_data:
                context_parts.append(f"{category.title()} Information: {json.dumps(category_data, indent=2)}")
        
        # Add relevant FAQs
        relevant_faqs = self._find_relevant_faqs(query)
        if relevant_faqs:
            faq_text = "\n".join([f"Q: {faq['question']}\nA: {faq['answer']}" for faq in relevant_faqs[:3]])
            context_parts.append(f"Relevant FAQs:\n{faq_text}")
        
        return "\n\n".join(context_parts)
    
    def _identify_relevant_categories(self, query: str) -> List[str]:
        """Identify relevant data categories based on query"""
        category_keywords = {
            'courses': ['course', 'program', 'branch', 'engineering', 'btech', 'computer science', 'mechanical'],
            'eligibility': ['eligibility', 'criteria', 'qualification', 'marks', 'percentage', 'requirement'],
            'fees': ['fee', 'cost', 'payment', 'money', 'scholarship', 'financial'],
            'important_dates': ['date', 'deadline', 'when', 'schedule', 'timeline', 'last date'],
            'facilities': ['facility', 'hostel', 'library', 'lab', 'infrastructure', 'campus'],
            'placement': ['placement', 'job', 'career', 'salary', 'package', 'company'],
            'contact': ['contact', 'phone', 'email', 'address', 'office', 'reach']
        }
        
        relevant_categories = []
        query_words = query.split()
        
        for category, keywords in category_keywords.items():
            if any(keyword in query for keyword in keywords):
                relevant_categories.append(category)
        
        # If no specific category found, include general categories
        if not relevant_categories:
            relevant_categories = ['courses', 'eligibility', 'fees']
        
        return relevant_categories
    
    def _find_relevant_faqs(self, query: str) -> List[Dict]:
        """Find relevant FAQs based on query"""
        relevant_faqs = []
        query_words = set(query.split())
        
        for faq in self.faqs:
            question_words = set(faq['question'].lower().split())
            # Calculate word overlap
            overlap = len(query_words.intersection(question_words))
            if overlap > 0:
                relevant_faqs.append((faq, overlap))
        
        # Sort by relevance and return top matches
        relevant_faqs.sort(key=lambda x: x[1], reverse=True)
        return [faq[0] for faq in relevant_faqs[:5]]
    
    def _create_prompt(self, query: str, context: str) -> str:
        """Create enhanced prompt for Gemini AI with better structure"""
        # Analyze query intent for better response formatting
        query_intent = self._analyze_query_intent(query)
        query_complexity = "comprehensive and detailed" if len(query.split()) > 8 else "clear and focused"

        prompt = f"""
{self.system_prompt}

CONVERSATION CONTEXT:
You are assisting a prospective student with MMMUT admission queries. Provide helpful, accurate, and encouraging responses.

KNOWLEDGE BASE:
{context}

STUDENT'S QUESTION: "{query}"

RESPONSE GUIDELINES:
🎯 **Intent**: {query_intent}
📝 **Style**: {query_complexity}
✅ **Requirements**:
   • Start with a direct answer to their specific question
   • Use emojis and formatting to make responses engaging and easy to read
   • Provide specific details (numbers, dates, requirements) when available
   • Structure information with bullet points or numbered lists for clarity
   • Include practical next steps or actionable advice
   • If information is incomplete, guide them to official sources
   • End with an encouraging note and offer to help with related questions

FORMATTING EXAMPLES:
- Use **bold** for important information
- Use bullet points (•) for lists
- Use emojis to make content more engaging
- Use clear section headers when covering multiple topics

RESPONSE TONE:
- Professional yet friendly and approachable
- Encouraging and supportive
- Confident in providing accurate information
- Helpful in guiding next steps

Please provide a comprehensive, well-formatted response:
"""
        return prompt

    def _analyze_query_intent(self, query: str) -> str:
        """Analyze the primary intent of the user's query"""
        query_lower = query.lower()

        intent_keywords = {
            'course_inquiry': ['course', 'program', 'branch', 'engineering', 'btech'],
            'eligibility_check': ['eligibility', 'qualify', 'marks', 'percentage', 'criteria'],
            'fee_information': ['fee', 'cost', 'payment', 'scholarship', 'financial'],
            'admission_process': ['admission', 'apply', 'application', 'procedure', 'form'],
            'deadline_inquiry': ['date', 'deadline', 'when', 'last date', 'timeline'],
            'facility_information': ['hostel', 'library', 'lab', 'facility', 'campus'],
            'placement_inquiry': ['placement', 'job', 'career', 'company', 'salary'],
            'contact_request': ['contact', 'phone', 'email', 'address', 'reach'],
            'general_information': ['about', 'university', 'college', 'mmmut']
        }

        for intent, keywords in intent_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return intent.replace('_', ' ').title()

        return "General Inquiry"
    
    def _add_to_history(self, query: str, response: str):
        """Add query and response to conversation history"""
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response,
            "query_number": self.query_count
        })
        
        # Keep only last 10 conversations to manage memory
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create error response"""
        return {
            "response": "I apologize, but I'm experiencing some technical difficulties. Please try again in a moment or contact the admission office directly.",
            "response_type": "error",
            "confidence": 0.0,
            "sources": ["error_handler"],
            "timestamp": datetime.now().isoformat(),
            "error": error_message
        }
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
        self.query_count = 0
        self.session_start_time = datetime.now()
        
        # Reset chat session
        self.chat = self.model.start_chat(history=[])
        
        logger.info("Conversation reset")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get chatbot usage statistics"""
        return {
            "total_queries": self.query_count,
            "session_duration": str(datetime.now() - self.session_start_time),
            "session_start": self.session_start_time.isoformat(),
            "conversation_length": len(self.conversation_history),
            "data_categories": len(self.organized_data.get("categories", {})),
            "available_faqs": len(self.faqs)
        }


def main():
    """Main function for testing the chatbot"""
    try:
        # Initialize chatbot
        chatbot = AdmissionChatbot()
        
        print("MMMUT Admission Chatbot")
        print("=" * 50)
        print("Type 'quit' to exit, 'reset' to reset conversation, 'stats' for statistics")
        print()
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'reset':
                chatbot.reset_conversation()
                print("Conversation reset!")
                continue
            elif user_input.lower() == 'stats':
                stats = chatbot.get_statistics()
                print(f"Statistics: {json.dumps(stats, indent=2)}")
                continue
            elif not user_input:
                continue
            
            # Process query
            response_data = chatbot.process_query(user_input)
            
            # Display response
            print(f"Bot: {response_data['response']}")
            print(f"[Type: {response_data['response_type']}, Confidence: {response_data['confidence']:.2f}]")
            print()
    
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Error: {str(e)}")
        logger.error(f"Main function error: {str(e)}")


if __name__ == "__main__":
    main()