#!/usr/bin/env python3
"""
MMMUT Admission Help Desk - Main Application Entry Point
A modern AI-powered chatbot for MMMUT admission queries
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    """Main function to run the MMMUT Admission Help Desk"""
    try:
        print("🎓 MMMUT Admission Help Desk")
        print("=" * 50)
        print("Starting AI-powered admission assistant...")
        print()
        
        # Import and run web integration
        from integration import main as web_main
        web_main()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please make sure all dependencies are installed.")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Goodbye! Thanks for using MMMUT Admission Help Desk")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
