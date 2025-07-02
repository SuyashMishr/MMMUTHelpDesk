#!/usr/bin/env python3
"""
Install dependencies for MMMUT chatbot using system Python
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a single package"""
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "--user", "--break-system-packages", package
        ])
        return True
    except subprocess.CalledProcessError:
        try:
            # Fallback: try without --break-system-packages
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "--user", package
            ])
            return True
        except subprocess.CalledProcessError:
            return False

def main():
    """Main installation function"""
    print("Installing MMMUT Chatbot Dependencies")
    print("=" * 50)
    
    # List of required packages
    packages = [
        "google-generativeai==0.3.2",
        "python-dotenv==1.0.0",
        "flask==2.3.3",
        "flask-cors==4.0.0",
        "pandas==2.1.1",
        "numpy==1.24.3",
        "PyPDF2==3.0.1",
        "pdfplumber==0.9.0",
        "requests==2.31.0",
        "werkzeug==2.3.7"
    ]
    
    successful = 0
    failed = []
    
    for package in packages:
        print(f"Installing {package}...")
        if install_package(package):
            print(f"✓ {package} installed successfully")
            successful += 1
        else:
            print(f"✗ Failed to install {package}")
            failed.append(package)
    
    print("\n" + "=" * 50)
    print(f"Installation Summary:")
    print(f"✓ Successfully installed: {successful}/{len(packages)} packages")
    
    if failed:
        print(f"✗ Failed to install: {len(failed)} packages")
        print("Failed packages:")
        for pkg in failed:
            print(f"  - {pkg}")
        print("\nYou may need to install these manually or use a virtual environment.")
    else:
        print("✓ All dependencies installed successfully!")
        print("\nNext steps:")
        print("1. Run: python initialize.py")
        print("2. Then: python run_chatbot.py or python run_web.py")

if __name__ == "__main__":
    main()