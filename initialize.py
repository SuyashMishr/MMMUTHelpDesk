#!/usr/bin/env python3
"""
Initialize the MMMUT chatbot data without virtual environment
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def initialize_data():
    """Initialize the chatbot data"""
    print("MMMUT Chatbot Data Initialization")
    print("=" * 50)
    
    try:
        # Step 1: Data Extraction
        print("1. Running data extraction...")
        from data_extraction import main as extract_main
        extract_main()
        print("✓ Data extraction completed")
        
        # Step 2: Data Organization
        print("\n2. Running data organization...")
        from data_organization import main as organize_main
        organize_main()
        print("✓ Data organization completed")
        
        # Step 3: Chatbot Training
        print("\n3. Running chatbot training...")
        from train_chatbot import main as train_main
        train_main()
        print("✓ Chatbot training completed")
        
        print("\n" + "=" * 50)
        print("✓ Initialization completed successfully!")
        print("\nYou can now run:")
        print("- python run_chatbot.py (for command line interface)")
        print("- python run_web.py (for web interface)")
        
        return True
        
    except Exception as e:
        print(f"✗ Error during initialization: {e}")
        print("\nPlease check:")
        print("1. Your .env file contains the correct Gemini API key")
        print("2. All required dependencies are installed")
        return False

def main():
    """Main function"""
    success = initialize_data()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()