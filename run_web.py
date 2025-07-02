#!/usr/bin/env python3
"""
Simple script to run the MMMUT chatbot web interface
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    """Main function to run the web interface"""
    try:
        print("Starting MMMUT Admission Chatbot Web Interface...")
        print("=" * 50)
        
        # Import and run web integration
        from integration import main as web_main
        web_main()
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please make sure all dependencies are installed.")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting web interface: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()