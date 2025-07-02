"""
Setup script for MMMUT Help Desk Chatbot
"""

import os
import sys
import subprocess
from pathlib import Path

def create_virtual_environment():
    """Create a virtual environment"""
    print("Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✓ Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to create virtual environment: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    
    # Determine the correct pip path based on OS
    if os.name == 'nt':  # Windows
        pip_path = "venv/Scripts/pip"
        python_path = "venv/Scripts/python"
    else:  # Unix/Linux/macOS
        pip_path = "venv/bin/pip"
        python_path = "venv/bin/python"
    
    try:
        # Upgrade pip first
        subprocess.run([python_path, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        
        # Install requirements
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False

def initialize_data():
    """Initialize data extraction and organization"""
    print("Initializing data...")
    
    # Determine the correct python path
    if os.name == 'nt':  # Windows
        python_path = "venv/Scripts/python"
    else:  # Unix/Linux/macOS
        python_path = "venv/bin/python"
    
    try:
        # Run data extraction
        print("  - Running data extraction...")
        subprocess.run([python_path, "src/data_extraction.py"], check=True)
        
        # Run data organization
        print("  - Running data organization...")
        subprocess.run([python_path, "src/data_organization.py"], check=True)
        
        # Run chatbot training
        print("  - Running chatbot training...")
        subprocess.run([python_path, "src/train_chatbot.py"], check=True)
        
        print("✓ Data initialization completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to initialize data: {e}")
        return False

def run_tests():
    """Run basic tests"""
    print("Running tests...")
    
    # Determine the correct python path
    if os.name == 'nt':  # Windows
        python_path = "venv/Scripts/python"
    else:  # Unix/Linux/macOS
        python_path = "venv/bin/python"
    
    try:
        subprocess.run([python_path, "src/testing.py"], check=True)
        print("✓ Tests completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Some tests failed: {e}")
        return False

def main():
    """Main setup function"""
    print("MMMUT Help Desk Chatbot Setup")
    print("=" * 50)
    
    # Check if .env file exists
    if not Path(".env").exists():
        print("✗ .env file not found. Please create it with your Gemini API key.")
        return False
    
    success_count = 0
    total_steps = 4
    
    # Step 1: Create virtual environment
    if create_virtual_environment():
        success_count += 1
    
    # Step 2: Install dependencies
    if install_dependencies():
        success_count += 1
    
    # Step 3: Initialize data
    if initialize_data():
        success_count += 1
    
    # Step 4: Run tests
    if run_tests():
        success_count += 1
    
    print("\n" + "=" * 50)
    print(f"Setup completed: {success_count}/{total_steps} steps successful")
    
    if success_count == total_steps:
        print("✓ Setup completed successfully!")
        print("\nNext steps:")
        print("1. Activate virtual environment:")
        if os.name == 'nt':
            print("   venv\\Scripts\\activate")
        else:
            print("   source venv/bin/activate")
        print("2. Run the chatbot:")
        print("   python src/chatbot.py")
        print("3. Or start the web interface:")
        print("   python src/integration.py")
    else:
        print("✗ Setup completed with some issues. Check the error messages above.")
    
    return success_count == total_steps

if __name__ == "__main__":
    main()