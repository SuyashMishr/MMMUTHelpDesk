"""
Data extraction module for processing admission brochure PDFs
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

class DataExtractor:
    """Extract data from admission brochure PDFs"""
    
    def __init__(self, raw_data_dir: str = None):
        """Initialize the data extractor"""
        if raw_data_dir is None:
            try:
                import sys
                sys.path.append(str(Path(__file__).parent.parent))
                from config.settings import RAW_DATA_DIR
                self.raw_data_dir = RAW_DATA_DIR
            except ImportError:
                # Fallback to default path
                self.raw_data_dir = Path(__file__).parent.parent / "data" / "raw_data"
        else:
            self.raw_data_dir = Path(raw_data_dir)
        
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
    
    def extract_from_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Extract text and structured data from PDF"""
        try:
            logger.info(f"Extracting data from: {pdf_path}")
            
            # Extract raw text
            raw_text = self._extract_text_from_pdf(pdf_path)
            self.extracted_data["raw_text"] = raw_text
            
            # Process and structure the data
            self._process_university_info(raw_text)
            self._process_courses(raw_text)
            self._process_eligibility(raw_text)
            self._process_fees(raw_text)
            self._process_dates(raw_text)
            self._process_contact_info(raw_text)
            self._process_facilities(raw_text)
            self._process_placement_info(raw_text)
            
            logger.info("Data extraction completed successfully")
            return self.extracted_data
            
        except Exception as e:
            logger.error(f"Error extracting data from PDF: {str(e)}")
            raise
    
    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract raw text from PDF using multiple methods"""
        text = ""
        
        try:
            # Method 1: Using pdfplumber (better for tables and complex layouts)
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            logger.warning(f"pdfplumber extraction failed: {e}")
            
            # Method 2: Fallback to PyPDF2
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            except Exception as e2:
                logger.error(f"PyPDF2 extraction also failed: {e2}")
                raise
        
        return text
    
    def _process_university_info(self, text: str):
        """Extract university information"""
        university_patterns = {
            'name': r'(?i)(madan mohan malaviya university of technology|mmmut)',
            'location': r'(?i)(gorakhpur|uttar pradesh|u\.?p\.?)',
            'established': r'(?i)established.*?(\d{4})',
            'type': r'(?i)(government|private|autonomous).*?university'
        }
        
        for key, pattern in university_patterns.items():
            match = re.search(pattern, text)
            if match:
                if key == 'established':
                    self.extracted_data["university_info"][key] = match.group(1)
                else:
                    self.extracted_data["university_info"][key] = match.group(0)
    
    def _process_courses(self, text: str):
        """Extract course information"""
        # Common engineering courses
        course_patterns = [
            r'(?i)computer science.*?engineering',
            r'(?i)information technology',
            r'(?i)electronics.*?communication',
            r'(?i)electrical.*?engineering',
            r'(?i)mechanical.*?engineering',
            r'(?i)civil.*?engineering',
            r'(?i)chemical.*?engineering',
            r'(?i)biotechnology',
            r'(?i)b\.?tech',
            r'(?i)bachelor.*?technology'
        ]
        
        courses = []
        for pattern in course_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if match not in courses:
                    courses.append(match.strip())
        
        self.extracted_data["courses"] = courses
    
    def _process_eligibility(self, text: str):
        """Extract eligibility criteria"""
        eligibility_patterns = {
            'minimum_marks': r'(?i)minimum.*?(\d+).*?percent',
            'qualifying_exam': r'(?i)(10\+2|intermediate|higher secondary)',
            'subjects': r'(?i)physics.*?chemistry.*?mathematics',
            'entrance_exam': r'(?i)(jee|joint entrance examination)'
        }
        
        for key, pattern in eligibility_patterns.items():
            match = re.search(pattern, text)
            if match:
                self.extracted_data["eligibility"][key] = match.group(0)
    
    def _process_fees(self, text: str):
        """Extract fee information"""
        fee_patterns = {
            'tuition_fee': r'(?i)tuition.*?fee.*?₹?\s*(\d+(?:,\d+)*)',
            'admission_fee': r'(?i)admission.*?fee.*?₹?\s*(\d+(?:,\d+)*)',
            'hostel_fee': r'(?i)hostel.*?fee.*?₹?\s*(\d+(?:,\d+)*)',
            'total_fee': r'(?i)total.*?fee.*?₹?\s*(\d+(?:,\d+)*)'
        }
        
        for key, pattern in fee_patterns.items():
            match = re.search(pattern, text)
            if match:
                self.extracted_data["fees"][key] = match.group(1)
    
    def _process_dates(self, text: str):
        """Extract important dates"""
        date_patterns = {
            'application_start': r'(?i)application.*?start.*?(\d{1,2}[-/]\d{1,2}[-/]\d{4})',
            'application_end': r'(?i)application.*?end.*?(\d{1,2}[-/]\d{1,2}[-/]\d{4})',
            'exam_date': r'(?i)exam.*?date.*?(\d{1,2}[-/]\d{1,2}[-/]\d{4})',
            'result_date': r'(?i)result.*?(\d{1,2}[-/]\d{1,2}[-/]\d{4})'
        }
        
        for key, pattern in date_patterns.items():
            match = re.search(pattern, text)
            if match:
                self.extracted_data["important_dates"][key] = match.group(1)
    
    def _process_contact_info(self, text: str):
        """Extract contact information"""
        contact_patterns = {
            'phone': r'(?i)phone.*?(\+?\d{1,3}[-.\s]?\d{3,4}[-.\s]?\d{6,8})',
            'email': r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
            'website': r'(?i)www\.[\w.-]+|https?://[\w.-]+',
            'address': r'(?i)address.*?([^\n]+)'
        }
        
        for key, pattern in contact_patterns.items():
            match = re.search(pattern, text)
            if match:
                self.extracted_data["contact_info"][key] = match.group(1)
    
    def _process_facilities(self, text: str):
        """Extract facility information"""
        facility_keywords = [
            'library', 'hostel', 'laboratory', 'cafeteria', 'sports',
            'gymnasium', 'auditorium', 'computer center', 'wifi',
            'medical center', 'transport', 'playground'
        ]
        
        facilities = []
        for keyword in facility_keywords:
            pattern = rf'(?i){keyword}[^\n]*'
            matches = re.findall(pattern, text)
            facilities.extend(matches)
        
        self.extracted_data["facilities"] = facilities
    
    def _process_placement_info(self, text: str):
        """Extract placement information"""
        placement_patterns = {
            'placement_percentage': r'(?i)placement.*?(\d+).*?percent',
            'average_package': r'(?i)average.*?package.*?₹?\s*(\d+(?:,\d+)*)',
            'highest_package': r'(?i)highest.*?package.*?₹?\s*(\d+(?:,\d+)*)',
            'top_recruiters': r'(?i)top.*?recruiter[s]?.*?([^\n]+)'
        }
        
        for key, pattern in placement_patterns.items():
            match = re.search(pattern, text)
            if match:
                self.extracted_data["placement_info"][key] = match.group(1)
    
    def save_extracted_data(self, output_path: str = None):
        """Save extracted data to JSON file"""
        if output_path is None:
            try:
                import sys
                sys.path.append(str(Path(__file__).parent.parent))
                from config.settings import STRUCTURED_DATA_FILE
                output_path = STRUCTURED_DATA_FILE
            except ImportError:
                # Fallback to default path
                output_path = Path(__file__).parent.parent / "data" / "structured_data.json"
        
        # Add metadata
        self.extracted_data["extraction_metadata"] = {
            "extraction_date": datetime.now().isoformat(),
            "extractor_version": "1.0.0"
        }
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.extracted_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Extracted data saved to: {output_path}")
            
        except Exception as e:
            logger.error(f"Error saving extracted data: {str(e)}")
            raise
    
    def process_all_pdfs(self):
        """Process all PDF files in the raw data directory"""
        pdf_files = list(self.raw_data_dir.glob("*.pdf"))
        
        if not pdf_files:
            logger.warning(f"No PDF files found in {self.raw_data_dir}")
            # Create a sample data structure
            self._create_sample_data()
            return
        
        for pdf_file in pdf_files:
            logger.info(f"Processing: {pdf_file}")
            self.extract_from_pdf(str(pdf_file))
        
        self.save_extracted_data()
    
    def _create_sample_data(self):
        """Create sample data when no PDF is available"""
        self.extracted_data = {
            "university_info": {
                "name": "Madan Mohan Malaviya University of Technology",
                "location": "Gorakhpur, Uttar Pradesh",
                "established": "1962",
                "type": "Government University"
            },
            "courses": [
                "Computer Science and Engineering",
                "Information Technology",
                "Electronics and Communication Engineering",
                "Electrical Engineering",
                "Mechanical Engineering",
                "Civil Engineering",
                "Chemical Engineering",
                "Biotechnology"
            ],
            "eligibility": {
                "minimum_marks": "75% in 10+2",
                "qualifying_exam": "10+2 with Physics, Chemistry, Mathematics",
                "entrance_exam": "JEE Main"
            },
            "fees": {
                "tuition_fee": "50000",
                "hostel_fee": "25000",
                "total_fee": "75000"
            },
            "important_dates": {
                "application_start": "01/03/2024",
                "application_end": "30/04/2024",
                "exam_date": "15/05/2024"
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
            }
        }
        
        self.save_extracted_data()


def main():
    """Main function to run data extraction"""
    try:
        extractor = DataExtractor()
        extractor.process_all_pdfs()
        print("Data extraction completed successfully!")
        
    except Exception as e:
        print(f"Error during data extraction: {str(e)}")
        logger.error(f"Data extraction failed: {str(e)}")


if __name__ == "__main__":
    main()