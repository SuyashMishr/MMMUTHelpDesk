#!/usr/bin/env python3
"""
Create comprehensive sample data for MMMUT admission chatbot
"""

import json
from pathlib import Path
from datetime import datetime

def create_comprehensive_mmmut_data():
    """Create comprehensive MMMUT admission data"""
    
    data = {
        "university_info": {
            "name": "Madan Mohan Malaviya University of Technology",
            "short_name": "MMMUT",
            "location": "Gorakhpur, Uttar Pradesh, India",
            "established": "1962",
            "type": "Government University",
            "affiliation": "UGC Recognized",
            "ranking": "NIRF Ranking 2024: 101-150 (Engineering Category)",
            "campus_area": "341 acres",
            "motto": "Knowledge is Power"
        },
        
        "courses": {
            "undergraduate": {
                "btech": [
                    {
                        "name": "Computer Science and Engineering",
                        "code": "CSE",
                        "duration": "4 years",
                        "seats": 120,
                        "specializations": ["AI & ML", "Data Science", "Cyber Security"]
                    },
                    {
                        "name": "Information Technology",
                        "code": "IT",
                        "duration": "4 years",
                        "seats": 60,
                        "specializations": ["Software Engineering", "Web Technologies"]
                    },
                    {
                        "name": "Electronics and Communication Engineering",
                        "code": "ECE",
                        "duration": "4 years",
                        "seats": 120,
                        "specializations": ["VLSI Design", "Communication Systems"]
                    },
                    {
                        "name": "Electrical Engineering",
                        "code": "EE",
                        "duration": "4 years",
                        "seats": 120,
                        "specializations": ["Power Systems", "Control Systems"]
                    },
                    {
                        "name": "Mechanical Engineering",
                        "code": "ME",
                        "duration": "4 years",
                        "seats": 120,
                        "specializations": ["Thermal Engineering", "Design Engineering"]
                    },
                    {
                        "name": "Civil Engineering",
                        "code": "CE",
                        "duration": "4 years",
                        "seats": 120,
                        "specializations": ["Structural Engineering", "Environmental Engineering"]
                    },
                    {
                        "name": "Chemical Engineering",
                        "code": "ChE",
                        "duration": "4 years",
                        "seats": 60,
                        "specializations": ["Process Engineering", "Petrochemicals"]
                    },
                    {
                        "name": "Biotechnology",
                        "code": "BT",
                        "duration": "4 years",
                        "seats": 30,
                        "specializations": ["Industrial Biotechnology", "Medical Biotechnology"]
                    }
                ]
            },
            "postgraduate": {
                "mtech": [
                    "Computer Science and Engineering",
                    "Electronics and Communication Engineering",
                    "Mechanical Engineering",
                    "Civil Engineering"
                ],
                "mba": {
                    "name": "Master of Business Administration",
                    "duration": "2 years",
                    "seats": 60
                }
            }
        },
        
        "eligibility": {
            "btech": {
                "academic_qualification": "10+2 or equivalent with Physics, Chemistry, and Mathematics",
                "minimum_marks": {
                    "general": "75%",
                    "obc": "68%",
                    "sc_st": "65%"
                },
                "entrance_exam": "JEE Main",
                "age_limit": "25 years (30 years for SC/ST)",
                "counseling": "UP State Counseling (UPSEE) / JoSAA Counseling"
            },
            "mtech": {
                "academic_qualification": "B.Tech/B.E. in relevant discipline",
                "minimum_marks": "60% (55% for SC/ST)",
                "entrance_exam": "GATE",
                "valid_gate_score": "Required"
            }
        },
        
        "fees": {
            "btech": {
                "tuition_fee_per_year": 75000,
                "development_fee": 10000,
                "examination_fee": 2000,
                "library_fee": 1000,
                "total_academic_fee_per_year": 88000,
                "hostel_fee_per_year": 25000,
                "mess_fee_per_year": 30000,
                "total_with_hostel_per_year": 143000,
                "total_course_fee_4_years": 352000,
                "total_with_hostel_4_years": 572000
            },
            "mtech": {
                "tuition_fee_per_year": 85000,
                "total_academic_fee_per_year": 95000,
                "hostel_fee_per_year": 25000,
                "total_with_hostel_per_year": 120000
            },
            "payment_modes": ["Online", "DD", "Bank Transfer"],
            "scholarship_available": "Yes - Merit and Need-based scholarships available"
        },
        
        "important_dates": {
            "2025": {
                "application_start": "01-04-2025",
                "application_end": "30-06-2025",
                "jee_main_exam": "24-01-2025 to 31-01-2025 (Session 1), 01-04-2025 to 15-04-2025 (Session 2)",
                "counseling_start": "15-07-2025",
                "admission_start": "01-08-2025",
                "classes_begin": "15-08-2025",
                "last_date_fee_payment": "31-08-2025"
            }
        },
        
        "admission_process": {
            "steps": [
                "Fill JEE Main Application Form",
                "Appear for JEE Main Examination",
                "Check JEE Main Results",
                "Participate in UP State Counseling/JoSAA Counseling",
                "Choice Filling and Locking",
                "Seat Allotment",
                "Document Verification",
                "Fee Payment",
                "Admission Confirmation"
            ],
            "required_documents": [
                "JEE Main Scorecard",
                "10th Mark Sheet",
                "12th Mark Sheet",
                "Transfer Certificate",
                "Character Certificate",
                "Caste Certificate (if applicable)",
                "Income Certificate (if applicable)",
                "Passport Size Photographs",
                "Aadhar Card",
                "Medical Certificate"
            ]
        },
        
        "contact_info": {
            "admission_office": {
                "phone": "+91-551-2273958",
                "email": "admission@mmmut.ac.in",
                "timings": "9:00 AM to 5:00 PM (Monday to Friday)"
            },
            "university_office": {
                "phone": "+91-551-2270011",
                "fax": "+91-551-2270011",
                "email": "registrar@mmmut.ac.in"
            },
            "address": {
                "full_address": "Madan Mohan Malaviya University of Technology, Deoria Road, Gorakhpur - 273010, Uttar Pradesh, India",
                "city": "Gorakhpur",
                "state": "Uttar Pradesh",
                "pincode": "273010",
                "country": "India"
            },
            "website": "https://www.mmmut.ac.in",
            "social_media": {
                "facebook": "https://www.facebook.com/mmmutofficial",
                "twitter": "@mmmutofficial",
                "linkedin": "madan-mohan-malaviya-university-of-technology"
            }
        },
        
        "facilities": {
            "academic": [
                "Central Library with 1,50,000+ books and journals",
                "Digital Library with e-resources",
                "Well-equipped Laboratories for all departments",
                "Computer Centers with high-speed internet",
                "Seminar Halls and Conference Rooms",
                "Smart Classrooms with modern teaching aids"
            ],
            "residential": [
                "Separate hostels for boys and girls",
                "Hostel capacity: 2000+ students",
                "24x7 security and medical facilities",
                "Common rooms with TV and indoor games",
                "Mess facilities with nutritious food",
                "WiFi connectivity in all hostels"
            ],
            "recreational": [
                "Sports Complex with indoor and outdoor facilities",
                "Gymnasium and fitness center",
                "Swimming pool",
                "Cricket ground and football field",
                "Basketball and volleyball courts",
                "Cultural center and auditorium"
            ],
            "other": [
                "Medical center with qualified doctors",
                "Bank and ATM facilities on campus",
                "Cafeteria and food courts",
                "Transportation facility",
                "Guest house for visitors",
                "Shopping complex"
            ]
        },
        
        "placement_info": {
            "2024_statistics": {
                "placement_percentage": "85%",
                "total_offers": 650,
                "companies_visited": 120,
                "highest_package": "45 LPA",
                "average_package": "8.5 LPA",
                "median_package": "6.2 LPA"
            },
            "top_recruiters": [
                "TCS", "Infosys", "Wipro", "Accenture", "Cognizant",
                "Microsoft", "Amazon", "Google", "Adobe", "Oracle",
                "L&T", "BHEL", "NTPC", "ONGC", "ISRO",
                "Flipkart", "Paytm", "Zomato", "Ola", "Uber"
            ],
            "placement_support": [
                "Dedicated Training & Placement Cell",
                "Pre-placement training programs",
                "Soft skills development workshops",
                "Technical interview preparation",
                "Resume building assistance",
                "Mock interviews and group discussions"
            ]
        },
        
        "departments": {
            "engineering": [
                {
                    "name": "Computer Science and Engineering",
                    "hod": "Dr. Rajesh Kumar",
                    "faculty_strength": 25,
                    "research_areas": ["AI/ML", "Data Science", "IoT", "Blockchain"]
                },
                {
                    "name": "Electronics and Communication Engineering",
                    "hod": "Dr. Priya Sharma",
                    "faculty_strength": 20,
                    "research_areas": ["VLSI", "Signal Processing", "Communication Systems"]
                },
                {
                    "name": "Mechanical Engineering",
                    "hod": "Dr. Amit Singh",
                    "faculty_strength": 22,
                    "research_areas": ["Thermal Engineering", "Manufacturing", "Robotics"]
                }
            ]
        },
        
        "faq": [
            {
                "question": "What is the admission process for B.Tech at MMMUT?",
                "answer": "Admission to B.Tech at MMMUT is through JEE Main followed by UP State Counseling or JoSAA counseling based on your JEE Main rank.",
                "category": "admission"
            },
            {
                "question": "What are the eligibility criteria for B.Tech admission?",
                "answer": "You need 10+2 with PCM, minimum 75% marks (68% for OBC, 65% for SC/ST), and a valid JEE Main score.",
                "category": "eligibility"
            },
            {
                "question": "What is the fee structure for B.Tech?",
                "answer": "The annual academic fee is ₹88,000. With hostel and mess, it comes to approximately ₹1,43,000 per year.",
                "category": "fees"
            },
            {
                "question": "Which companies visit MMMUT for placements?",
                "answer": "Top companies like TCS, Infosys, Microsoft, Amazon, Google, L&T, BHEL, and many more visit for placements.",
                "category": "placement"
            },
            {
                "question": "What facilities are available on campus?",
                "answer": "MMMUT has excellent facilities including library, labs, hostels, sports complex, medical center, and WiFi campus.",
                "category": "facilities"
            },
            {
                "question": "How is the placement record of MMMUT?",
                "answer": "MMMUT has an excellent placement record with 85% placement rate, highest package of 45 LPA, and average package of 8.5 LPA.",
                "category": "placement"
            },
            {
                "question": "What courses are offered at MMMUT?",
                "answer": "MMMUT offers B.Tech in 8 branches: CSE, IT, ECE, EE, ME, CE, Chemical, and Biotechnology. M.Tech and MBA are also available.",
                "category": "courses"
            }
        ],
        
        "quick_responses": {
            "greeting": [
                "Hello! Welcome to MMMUT Admission Help Desk. How can I assist you today?",
                "Hi there! I'm here to help with your MMMUT admission queries. What would you like to know?",
                "Welcome! I can help you with information about MMMUT admissions. What's your question?"
            ],
            "courses": "MMMUT offers B.Tech programs in Computer Science, IT, Electronics, Electrical, Mechanical, Civil, Chemical Engineering, and Biotechnology. M.Tech and MBA programs are also available.",
            "fees": "The annual B.Tech fee is ₹88,000 (academic) + ₹55,000 (hostel & mess) = ₹1,43,000 total per year.",
            "eligibility": "For B.Tech: 10+2 with PCM, 75% marks (68% OBC, 65% SC/ST), and JEE Main qualification required.",
            "location": "MMMUT is located in Gorakhpur, Uttar Pradesh, India.",
            "contact": "Contact: +91-551-2273958, Email: admission@mmmut.ac.in, Website: www.mmmut.ac.in",
            "placement": "MMMUT has 85% placement rate with highest package of 45 LPA and average package of 8.5 LPA.",
            "facilities": "MMMUT offers excellent facilities including library, labs, hostels, sports complex, medical center, and full WiFi campus.",
            "fallback": "I'm sorry, I don't have specific information about that. Could you please ask about courses, eligibility, fees, placement, or other admission-related topics?"
        },
        
        "extraction_metadata": {
            "data_source": "Comprehensive MMMUT Admission Information 2025",
            "creation_date": datetime.now().isoformat(),
            "version": "2.0.0",
            "last_updated": "2025-07-02"
        }
    }
    
    return data

def main():
    """Create and save comprehensive MMMUT data"""
    print("Creating Comprehensive MMMUT Admission Data")
    print("=" * 50)
    
    # Create data
    data = create_comprehensive_mmmut_data()
    
    # Save to structured_data.json
    output_file = Path(__file__).parent / "data" / "structured_data.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Comprehensive data saved to: {output_file}")
    print(f"✓ Data includes {len(data['courses']['undergraduate']['btech'])} B.Tech courses")
    print(f"✓ Data includes {len(data['faq'])} FAQ entries")
    print(f"✓ Data includes placement info and facilities")
    
    return True

if __name__ == "__main__":
    main()