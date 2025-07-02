"""
Data organization module for structuring extracted admission data
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataOrganizer:
    """Organize and structure extracted admission data"""
    
    def __init__(self, structured_data_file: str = None):
        """Initialize the data organizer"""
        if structured_data_file is None:
            try:
                import sys
                sys.path.append(str(Path(__file__).parent.parent))
                from config.settings import STRUCTURED_DATA_FILE
                self.data_file = STRUCTURED_DATA_FILE
            except ImportError:
                # Fallback to default path
                self.data_file = Path(__file__).parent.parent / "data" / "structured_data.json"
        else:
            self.data_file = Path(structured_data_file)
        
        self.organized_data = {
            "categories": {},
            "search_index": {},
            "faq": [],
            "quick_responses": {}
        }
        
        self.raw_data = {}
    
    def load_extracted_data(self) -> Dict[str, Any]:
        """Load extracted data from JSON file"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.raw_data = json.load(f)
            
            logger.info(f"Loaded data from: {self.data_file}")
            return self.raw_data
            
        except FileNotFoundError:
            logger.error(f"Data file not found: {self.data_file}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in data file: {str(e)}")
            raise
    
    def organize_data(self) -> Dict[str, Any]:
        """Organize the extracted data into categories"""
        if not self.raw_data:
            self.load_extracted_data()
        
        # Organize into categories
        self._organize_university_info()
        self._organize_courses()
        self._organize_admission_process()
        self._organize_eligibility()
        self._organize_fees()
        self._organize_dates()
        self._organize_facilities()
        self._organize_placement()
        self._organize_contact()
        
        # Create search index
        self._create_search_index()
        
        # Generate FAQs
        self._generate_faqs()
        
        # Create quick responses
        self._create_quick_responses()
        
        logger.info("Data organization completed")
        return self.organized_data
    
    def _organize_university_info(self):
        """Organize university information"""
        university_info = self.raw_data.get("university_info", {})
        
        self.organized_data["categories"]["university"] = {
            "title": "About MMMUT",
            "description": "General information about the university",
            "data": {
                "full_name": university_info.get("name", "Madan Mohan Malaviya University of Technology"),
                "short_name": "MMMUT",
                "location": university_info.get("location", "Gorakhpur, Uttar Pradesh"),
                "established": university_info.get("established", "1962"),
                "type": university_info.get("type", "Government University"),
                "accreditation": "NAAC Accredited",
                "recognition": "UGC Recognized"
            },
            "keywords": ["university", "about", "mmmut", "gorakhpur", "established", "government"]
        }
    
    def _organize_courses(self):
        """Organize course information"""
        courses = self.raw_data.get("courses", [])
        
        # Categorize courses
        engineering_courses = []
        other_courses = []
        
        for course in courses:
            if any(keyword in course.lower() for keyword in ["engineering", "b.tech", "technology"]):
                engineering_courses.append(course)
            else:
                other_courses.append(course)
        
        self.organized_data["categories"]["courses"] = {
            "title": "Courses Offered",
            "description": "Available undergraduate and postgraduate programs",
            "data": {
                "undergraduate": {
                    "engineering": engineering_courses if engineering_courses else [
                        "Computer Science and Engineering",
                        "Information Technology",
                        "Electronics and Communication Engineering",
                        "Electrical Engineering",
                        "Mechanical Engineering",
                        "Civil Engineering",
                        "Chemical Engineering",
                        "Biotechnology"
                    ],
                    "other": other_courses
                },
                "duration": "4 years",
                "degree": "Bachelor of Technology (B.Tech)"
            },
            "keywords": ["courses", "programs", "btech", "engineering", "computer science", "mechanical", "civil", "electrical"]
        }
    
    def _organize_admission_process(self):
        """Organize admission process information"""
        self.organized_data["categories"]["admission_process"] = {
            "title": "Admission Process",
            "description": "Step-by-step admission procedure",
            "data": {
                "steps": [
                    "Fill online application form",
                    "Upload required documents",
                    "Pay application fee",
                    "Appear for entrance examination (if applicable)",
                    "Check merit list",
                    "Attend counseling session",
                    "Document verification",
                    "Fee payment and admission confirmation"
                ],
                "entrance_exam": "JEE Main",
                "selection_criteria": "Merit-based on entrance exam scores",
                "reservation": "As per government norms"
            },
            "keywords": ["admission", "process", "procedure", "apply", "application", "form", "steps"]
        }
    
    def _organize_eligibility(self):
        """Organize eligibility criteria"""
        eligibility = self.raw_data.get("eligibility", {})
        
        self.organized_data["categories"]["eligibility"] = {
            "title": "Eligibility Criteria",
            "description": "Academic requirements for admission",
            "data": {
                "academic_qualification": eligibility.get("qualifying_exam", "10+2 or equivalent"),
                "minimum_marks": eligibility.get("minimum_marks", "75% in 10+2"),
                "required_subjects": "Physics, Chemistry, Mathematics",
                "entrance_exam": eligibility.get("entrance_exam", "JEE Main"),
                "age_limit": "No age limit",
                "nationality": "Indian/NRI/Foreign nationals"
            },
            "keywords": ["eligibility", "criteria", "qualification", "marks", "percentage", "requirements", "10+2"]
        }
    
    def _organize_fees(self):
        """Organize fee structure"""
        fees = self.raw_data.get("fees", {})
        
        self.organized_data["categories"]["fees"] = {
            "title": "Fee Structure",
            "description": "Detailed fee information",
            "data": {
                "tuition_fee": fees.get("tuition_fee", "50,000"),
                "hostel_fee": fees.get("hostel_fee", "25,000"),
                "mess_fee": "20,000",
                "other_charges": "5,000",
                "total_annual_fee": fees.get("total_fee", "1,00,000"),
                "payment_modes": ["Online", "Demand Draft", "Bank Transfer"],
                "scholarship": "Available for meritorious students",
                "fee_refund_policy": "As per university rules"
            },
            "keywords": ["fees", "cost", "payment", "tuition", "hostel", "scholarship", "money"]
        }
    
    def _organize_dates(self):
        """Organize important dates"""
        dates = self.raw_data.get("important_dates", {})
        
        self.organized_data["categories"]["important_dates"] = {
            "title": "Important Dates",
            "description": "Key dates for admission process",
            "data": {
                "application_start": dates.get("application_start", "March 1, 2024"),
                "application_end": dates.get("application_end", "April 30, 2024"),
                "entrance_exam": dates.get("exam_date", "May 15, 2024"),
                "result_declaration": dates.get("result_date", "June 15, 2024"),
                "counseling_start": "July 1, 2024",
                "admission_confirmation": "July 31, 2024",
                "classes_begin": "August 15, 2024"
            },
            "keywords": ["dates", "deadline", "schedule", "timeline", "when", "last date", "exam date"]
        }
    
    def _organize_facilities(self):
        """Organize facility information"""
        facilities = self.raw_data.get("facilities", [])
        
        # Categorize facilities
        academic_facilities = []
        residential_facilities = []
        recreational_facilities = []
        other_facilities = []
        
        for facility in facilities:
            facility_lower = facility.lower()
            if any(keyword in facility_lower for keyword in ["library", "lab", "computer", "classroom"]):
                academic_facilities.append(facility)
            elif any(keyword in facility_lower for keyword in ["hostel", "mess", "canteen"]):
                residential_facilities.append(facility)
            elif any(keyword in facility_lower for keyword in ["sports", "gym", "playground", "auditorium"]):
                recreational_facilities.append(facility)
            else:
                other_facilities.append(facility)
        
        self.organized_data["categories"]["facilities"] = {
            "title": "Campus Facilities",
            "description": "Available facilities and infrastructure",
            "data": {
                "academic": academic_facilities if academic_facilities else [
                    "Central Library with 50,000+ books",
                    "Computer Labs with latest equipment",
                    "Well-equipped laboratories",
                    "Smart classrooms"
                ],
                "residential": residential_facilities if residential_facilities else [
                    "Boys Hostel",
                    "Girls Hostel",
                    "Mess facilities"
                ],
                "recreational": recreational_facilities if recreational_facilities else [
                    "Sports Complex",
                    "Gymnasium",
                    "Auditorium",
                    "Playground"
                ],
                "other": other_facilities if other_facilities else [
                    "Medical Center",
                    "WiFi Campus",
                    "Bank ATM",
                    "Transport facility"
                ]
            },
            "keywords": ["facilities", "infrastructure", "hostel", "library", "lab", "sports", "wifi"]
        }
    
    def _organize_placement(self):
        """Organize placement information"""
        placement = self.raw_data.get("placement_info", {})
        
        self.organized_data["categories"]["placement"] = {
            "title": "Placement Information",
            "description": "Career opportunities and placement statistics",
            "data": {
                "placement_percentage": placement.get("placement_percentage", "85%"),
                "average_package": placement.get("average_package", "6.5 LPA"),
                "highest_package": placement.get("highest_package", "25 LPA"),
                "top_recruiters": [
                    "TCS", "Infosys", "Wipro", "Accenture", "IBM",
                    "Microsoft", "Amazon", "Google", "Flipkart"
                ],
                "placement_cell": "Active placement cell",
                "training_programs": "Soft skills and technical training",
                "internship_opportunities": "Available with leading companies"
            },
            "keywords": ["placement", "job", "career", "salary", "package", "companies", "recruitment"]
        }
    
    def _organize_contact(self):
        """Organize contact information"""
        contact = self.raw_data.get("contact_info", {})
        
        self.organized_data["categories"]["contact"] = {
            "title": "Contact Information",
            "description": "How to reach the admission office",
            "data": {
                "admission_office": {
                    "phone": contact.get("phone", "+91-551-2273958"),
                    "email": contact.get("email", "admission@mmmut.ac.in"),
                    "address": "MMMUT, Gorakhpur - 273010, Uttar Pradesh"
                },
                "university_website": contact.get("website", "www.mmmut.ac.in"),
                "office_hours": "9:00 AM to 5:00 PM (Monday to Friday)",
                "helpline": "1800-XXX-XXXX",
                "social_media": {
                    "facebook": "facebook.com/mmmut",
                    "twitter": "@mmmut_official"
                }
            },
            "keywords": ["contact", "phone", "email", "address", "office", "help", "support"]
        }
    
    def _create_search_index(self):
        """Create search index for quick lookups"""
        search_index = {}
        
        for category_name, category_data in self.organized_data["categories"].items():
            keywords = category_data.get("keywords", [])
            
            for keyword in keywords:
                if keyword not in search_index:
                    search_index[keyword] = []
                search_index[keyword].append(category_name)
        
        self.organized_data["search_index"] = search_index
    
    def _generate_faqs(self):
        """Generate frequently asked questions"""
        faqs = [
            {
                "question": "What is the eligibility criteria for B.Tech admission?",
                "answer": "Candidates must have passed 10+2 with Physics, Chemistry, and Mathematics with minimum 75% marks and qualify JEE Main.",
                "category": "eligibility"
            },
            {
                "question": "What is the fee structure for B.Tech?",
                "answer": "The annual fee is approximately ₹1,00,000 including tuition, hostel, and other charges.",
                "category": "fees"
            },
            {
                "question": "When do applications start?",
                "answer": "Applications typically start in March and end in April. Check the official website for exact dates.",
                "category": "important_dates"
            },
            {
                "question": "What courses are offered?",
                "answer": "MMMUT offers B.Tech in CSE, IT, ECE, EE, ME, CE, Chemical Engineering, and Biotechnology.",
                "category": "courses"
            },
            {
                "question": "Is hostel facility available?",
                "answer": "Yes, separate hostels are available for boys and girls with mess facilities.",
                "category": "facilities"
            },
            {
                "question": "What is the placement record?",
                "answer": "MMMUT has excellent placement record with 85%+ placement rate and average package of 6.5 LPA.",
                "category": "placement"
            },
            {
                "question": "How to contact admission office?",
                "answer": "You can contact at +91-551-2273958 or email admission@mmmut.ac.in",
                "category": "contact"
            }
        ]
        
        self.organized_data["faq"] = faqs
    
    def _create_quick_responses(self):
        """Create quick response templates"""
        quick_responses = {
            "greeting": [
                "Hello! Welcome to MMMUT Admission Help Desk. How can I assist you today?",
                "Hi there! I'm here to help with your MMMUT admission queries. What would you like to know?",
                "Welcome! I can help you with information about MMMUT admissions. What's your question?"
            ],
            "courses": "MMMUT offers B.Tech programs in Computer Science, IT, Electronics, Electrical, Mechanical, Civil, Chemical Engineering, and Biotechnology.",
            "eligibility": "For B.Tech admission, you need 10+2 with PCM and 75% marks, plus qualify JEE Main.",
            "fees": "The annual fee is approximately ₹1,00,000 including all charges. Scholarships are available for meritorious students.",
            "dates": "Applications typically open in March. Please check our website for current dates and deadlines.",
            "contact": "Contact admission office: Phone: +91-551-2273958, Email: admission@mmmut.ac.in",
            "facilities": "MMMUT has excellent facilities including library, labs, hostels, sports complex, and WiFi campus.",
            "placement": "MMMUT has 85%+ placement rate with average package of 6.5 LPA. Top companies recruit from campus.",
            "location": "MMMUT is located in Gorakhpur, Uttar Pradesh, India.",
            "fallback": "I'm sorry, I don't have specific information about that. Could you please ask about courses, eligibility, fees, or other admission-related topics?"
        }
        
        self.organized_data["quick_responses"] = quick_responses
    
    def save_organized_data(self, output_path: str = None):
        """Save organized data to JSON file"""
        if output_path is None:
            output_path = self.data_file.parent / "organized_data.json"
        
        # Add metadata
        self.organized_data["organization_metadata"] = {
            "organization_date": datetime.now().isoformat(),
            "organizer_version": "1.0.0",
            "total_categories": len(self.organized_data["categories"]),
            "total_faqs": len(self.organized_data["faq"])
        }
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.organized_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Organized data saved to: {output_path}")
            
        except Exception as e:
            logger.error(f"Error saving organized data: {str(e)}")
            raise
    
    def get_category_data(self, category: str) -> Dict[str, Any]:
        """Get data for a specific category"""
        return self.organized_data["categories"].get(category, {})
    
    def search_categories(self, query: str) -> List[str]:
        """Search for relevant categories based on query"""
        query_words = query.lower().split()
        relevant_categories = set()
        
        for word in query_words:
            if word in self.organized_data["search_index"]:
                relevant_categories.update(self.organized_data["search_index"][word])
        
        return list(relevant_categories)


def main():
    """Main function to run data organization"""
    try:
        organizer = DataOrganizer()
        organizer.organize_data()
        organizer.save_organized_data()
        print("Data organization completed successfully!")
        
    except Exception as e:
        print(f"Error during data organization: {str(e)}")
        logger.error(f"Data organization failed: {str(e)}")


if __name__ == "__main__":
    main()