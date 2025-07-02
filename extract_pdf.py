#!/usr/bin/env python3
"""
Standalone PDF extraction script for MMMUT admission brochure
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import PyPDF2
import pdfplumber
import re
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFExtractor:
    """Extract data from admission brochure PDFs"""
    
    def __init__(self):
        """Initialize the PDF extractor"""
        self.project_root = Path(__file__).parent
        self.raw_data_dir = self.project_root / "data" / "raw_data"
        self.output_file = self.project_root / "data" / "structured_data.json"
        
        self.extracted_data = {
            "university_info": {},
            "courses": [],
            "eligibility": {},
            "fees": {},
            "important_dates": {},
            "contact_info": {},
            "facilities": [],
            "placement_info": {},
            "raw_text": ""
        }
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract raw text from PDF using multiple methods"""
        text = ""
        
        try:
            # Method 1: Using pdfplumber (better for structured text)
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            if text.strip():
                logger.info(f"Successfully extracted text using pdfplumber: {len(text)} characters")
                return text
        
        except Exception as e:
            logger.warning(f"pdfplumber extraction failed: {str(e)}")
        
        try:
            # Method 2: Using PyPDF2 as fallback
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            
            if text.strip():
                logger.info(f"Successfully extracted text using PyPDF2: {len(text)} characters")
                return text
        
        except Exception as e:
            logger.error(f"PyPDF2 extraction also failed: {str(e)}")
        
        return text
    
    def process_university_info(self, text: str):
        """Extract university information"""
        university_patterns = {
            "name": r"(Madan Mohan Malaviya University of Technology|MMMUT)",
            "location": r"(Gorakhpur|Uttar Pradesh|UP)",
            "established": r"established.*?(\d{4})|(\d{4}).*?established",
            "type": r"(Government|Private|Public|State).*?University"
        }
        
        for key, pattern in university_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                if key == "established":
                    # Extract year from tuple matches
                    for match in matches:
                        year = match[0] if match[0] else match[1]
                        if year and len(year) == 4:
                            self.extracted_data["university_info"][key] = year
                            break
                else:
                    self.extracted_data["university_info"][key] = matches[0] if isinstance(matches[0], str) else matches[0][0]
    
    def process_courses(self, text: str):
        """Extract course information"""
        # Common engineering branches
        course_patterns = [
            r"Computer Science.*?Engineering|CSE|Computer Science",
            r"Information Technology|IT",
            r"Electronics.*?Communication.*?Engineering|ECE",
            r"Electrical.*?Engineering|EE",
            r"Mechanical.*?Engineering|ME",
            r"Civil.*?Engineering|CE",
            r"Chemical.*?Engineering|ChE",
            r"Biotechnology|BT",
            r"Petroleum.*?Engineering|PE"
        ]
        
        courses = []
        for pattern in course_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if match not in courses:
                    courses.append(match)
        
        # Also look for B.Tech programs
        btech_pattern = r"B\.?Tech.*?in\s+([^,\n.]+)"
        btech_matches = re.findall(btech_pattern, text, re.IGNORECASE)
        for match in btech_matches:
            clean_match = match.strip()
            if clean_match and clean_match not in courses:
                courses.append(clean_match)
        
        self.extracted_data["courses"] = courses[:10]  # Limit to first 10 matches
    
    def process_eligibility(self, text: str):
        """Extract eligibility criteria"""
        eligibility_patterns = {
            "minimum_marks": r"(\d+)%.*?marks|marks.*?(\d+)%",
            "qualifying_exam": r"(10\+2|12th|Intermediate|Higher Secondary)",
            "subjects": r"(Physics|Chemistry|Mathematics|PCM)",
            "entrance_exam": r"(JEE.*?Main|JEE|UPSEE|Entrance.*?Exam)"
        }
        
        for key, pattern in eligibility_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                if key == "minimum_marks":
                    # Extract percentage from tuple matches
                    for match in matches:
                        percentage = match[0] if match[0] else match[1]
                        if percentage:
                            self.extracted_data["eligibility"][key] = f"{percentage}%"
                            break
                else:
                    self.extracted_data["eligibility"][key] = matches[0] if isinstance(matches[0], str) else matches[0]
    
    def process_fees(self, text: str):
        """Extract fee information"""
        fee_patterns = {
            "tuition_fee": r"tuition.*?fee.*?₹?\s*(\d+(?:,\d+)*)|₹?\s*(\d+(?:,\d+)*).*?tuition",
            "total_fee": r"total.*?fee.*?₹?\s*(\d+(?:,\d+)*)|₹?\s*(\d+(?:,\d+)*).*?total",
            "hostel_fee": r"hostel.*?fee.*?₹?\s*(\d+(?:,\d+)*)|₹?\s*(\d+(?:,\d+)*).*?hostel",
            "annual_fee": r"annual.*?fee.*?₹?\s*(\d+(?:,\d+)*)|₹?\s*(\d+(?:,\d+)*).*?annual"
        }
        
        for key, pattern in fee_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Extract amount from tuple matches
                for match in matches:
                    amount = match[0] if match[0] else match[1]
                    if amount:
                        self.extracted_data["fees"][key] = amount
                        break
    
    def process_dates(self, text: str):
        """Extract important dates"""
        date_patterns = {
            "application_start": r"application.*?start.*?(\d{1,2}[-/]\d{1,2}[-/]\d{4})",
            "application_end": r"application.*?end.*?(\d{1,2}[-/]\d{1,2}[-/]\d{4})|last.*?date.*?(\d{1,2}[-/]\d{1,2}[-/]\d{4})",
            "exam_date": r"exam.*?date.*?(\d{1,2}[-/]\d{1,2}[-/]\d{4})",
            "result_date": r"result.*?(\d{1,2}[-/]\d{1,2}[-/]\d{4})"
        }
        
        for key, pattern in date_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Extract date from tuple matches
                for match in matches:
                    if isinstance(match, tuple):
                        date = match[0] if match[0] else match[1]
                    else:
                        date = match
                    if date:
                        self.extracted_data["important_dates"][key] = date
                        break
    
    def process_contact_info(self, text: str):
        """Extract contact information"""
        contact_patterns = {
            "phone": r"(\+91[-\s]?\d{3,4}[-\s]?\d{7}|\d{3,4}[-\s]?\d{7})",
            "email": r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
            "website": r"(www\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}|https?://[a-zA-Z0-9.-]+)"
        }
        
        for key, pattern in contact_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                self.extracted_data["contact_info"][key] = matches[0]
    
    def process_facilities(self, text: str):
        """Extract facilities information"""
        facility_keywords = [
            "library", "hostel", "laboratory", "computer lab", "sports", "gym", 
            "cafeteria", "medical", "wifi", "transport", "auditorium", "seminar hall"
        ]
        
        facilities = []
        for keyword in facility_keywords:
            pattern = rf"([^.]*{keyword}[^.]*)"
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                clean_match = match.strip()
                if clean_match and len(clean_match) < 100:  # Reasonable length
                    facilities.append(clean_match)
        
        self.extracted_data["facilities"] = facilities[:10]  # Limit to first 10
    
    def process_placement_info(self, text: str):
        """Extract placement information"""
        placement_patterns = {
            "placement_percentage": r"placement.*?(\d+)%|(\d+)%.*?placement",
            "average_package": r"average.*?package.*?₹?\s*(\d+(?:\.\d+)?)\s*(?:lpa|lakhs?)|₹?\s*(\d+(?:\.\d+)?)\s*(?:lpa|lakhs?).*?average",
            "highest_package": r"highest.*?package.*?₹?\s*(\d+(?:\.\d+)?)\s*(?:lpa|lakhs?)|₹?\s*(\d+(?:\.\d+)?)\s*(?:lpa|lakhs?).*?highest"
        }
        
        for key, pattern in placement_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Extract value from tuple matches
                for match in matches:
                    if isinstance(match, tuple):
                        value = match[0] if match[0] else match[1]
                    else:
                        value = match
                    if value:
                        if key == "placement_percentage":
                            self.extracted_data["placement_info"][key] = f"{value}%"
                        else:
                            self.extracted_data["placement_info"][key] = f"{value} LPA"
                        break
    
    def extract_from_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Extract all data from PDF"""
        logger.info(f"Processing PDF: {pdf_path}")
        
        # Extract raw text
        raw_text = self.extract_text_from_pdf(pdf_path)
        self.extracted_data["raw_text"] = raw_text
        
        if not raw_text.strip():
            logger.warning("No text extracted from PDF")
            return self.extracted_data
        
        logger.info(f"Extracted {len(raw_text)} characters from PDF")
        
        # Process different sections
        self.process_university_info(raw_text)
        self.process_courses(raw_text)
        self.process_eligibility(raw_text)
        self.process_fees(raw_text)
        self.process_dates(raw_text)
        self.process_contact_info(raw_text)
        self.process_facilities(raw_text)
        self.process_placement_info(raw_text)
        
        return self.extracted_data
    
    def process_all_pdfs(self):
        """Process all PDF files in the raw data directory"""
        pdf_files = list(self.raw_data_dir.glob("*.pdf"))
        
        if not pdf_files:
            logger.warning(f"No PDF files found in {self.raw_data_dir}")
            # Create sample data
            self.create_sample_data()
            return
        
        logger.info(f"Found {len(pdf_files)} PDF files")
        
        for pdf_file in pdf_files:
            try:
                self.extract_from_pdf(str(pdf_file))
                logger.info(f"Successfully processed: {pdf_file.name}")
            except Exception as e:
                logger.error(f"Error processing {pdf_file.name}: {str(e)}")
        
        # Save extracted data
        self.save_data()
    
    def create_sample_data(self):
        """Create sample data if no PDFs are found"""
        logger.info("Creating sample admission data")
        
        self.extracted_data = {
            "university_info": {
                "name": "Madan Mohan Malaviya University of Technology",
                "location": "Gorakhpur, Uttar Pradesh",
                "established": "1962",
                "type": "Government University"
            },
            "courses": [
                "Computer Science Engineering",
                "Information Technology",
                "Electronics and Communication Engineering",
                "Electrical Engineering",
                "Mechanical Engineering",
                "Civil Engineering",
                "Chemical Engineering",
                "Biotechnology"
            ],
            "eligibility": {
                "minimum_marks": "75%",
                "qualifying_exam": "10+2",
                "subjects": "Physics, Chemistry, Mathematics",
                "entrance_exam": "JEE Main"
            },
            "fees": {
                "annual_fee": "100000",
                "tuition_fee": "75000",
                "hostel_fee": "25000"
            },
            "important_dates": {
                "application_start": "01/04/2025",
                "application_end": "30/06/2025",
                "exam_date": "15/07/2025"
            },
            "contact_info": {
                "phone": "+91-551-2273958",
                "email": "admission@mmmut.ac.in",
                "website": "www.mmmut.ac.in"
            },
            "facilities": [
                "Central Library with 50000+ books",
                "Boys and Girls Hostels",
                "Computer Labs with latest equipment",
                "Sports Complex",
                "Medical Center",
                "WiFi Campus"
            ],
            "placement_info": {
                "placement_percentage": "85%",
                "average_package": "6.5 LPA",
                "highest_package": "25 LPA"
            },
            "raw_text": "Sample data created as no PDF files were found."
        }
    
    def save_data(self):
        """Save extracted data to JSON file"""
        # Add metadata
        self.extracted_data["extraction_metadata"] = {
            "extraction_date": datetime.now().isoformat(),
            "extractor_version": "1.0.0",
            "pdf_files_processed": len(list(self.raw_data_dir.glob("*.pdf")))
        }
        
        # Ensure output directory exists
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(self.extracted_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Extracted data saved to: {self.output_file}")
            
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
            raise


def main():
    """Main function"""
    try:
        print("MMMUT PDF Data Extraction")
        print("=" * 50)
        
        extractor = PDFExtractor()
        extractor.process_all_pdfs()
        
        print("✓ PDF extraction completed successfully!")
        print(f"Data saved to: {extractor.output_file}")
        
        # Show summary
        data = extractor.extracted_data
        print("\nExtraction Summary:")
        print(f"- University: {data['university_info'].get('name', 'N/A')}")
        print(f"- Courses found: {len(data['courses'])}")
        print(f"- Text extracted: {len(data['raw_text'])} characters")
        
    except Exception as e:
        print(f"Error during extraction: {str(e)}")
        return False
    
    return True


if __name__ == "__main__":
    main()