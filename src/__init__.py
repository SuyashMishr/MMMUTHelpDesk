"""
MMMUT Help Desk - Admission Chatbot
A comprehensive chatbot system for MMMUT admission queries.
"""

__version__ = "1.0.0"
__author__ = "Suyash Mishra"
__email__ = "your-email@example.com"

# Import main classes for easy access
from .chatbot import AdmissionChatbot
from .data_extraction import DataExtractor
from .data_organization import DataOrganizer

__all__ = [
    'AdmissionChatbot',
    'DataExtractor', 
    'DataOrganizer'
]