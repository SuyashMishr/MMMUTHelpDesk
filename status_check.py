#!/usr/bin/env python3
"""
Status check script for MMMUT chatbot deployment
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def check_file_exists(file_path, description):
    """Check if a file exists"""
    if Path(file_path).exists():
        print(f"✓ {description}: {file_path}")
        return True
    else:
        print(f"✗ {description}: {file_path} (MISSING)")
        return False

def check_data_files():
    """Check if all data files exist"""
    print("Checking Data Files:")
    print("-" * 30)
    
    files_to_check = [
        ("data/structured_data.json", "Structured Data"),
        ("data/organized_data.json", "Organized Data"),
        ("data/training/training_data.json", "Training Data"),
        ("data/training/knowledge_base.json", "Knowledge Base"),
        ("data/training/intent_patterns.json", "Intent Patterns")
    ]
    
    all_exist = True
    for file_path, description in files_to_check:
        if not check_file_exists(file_path, description):
            all_exist = False
    
    return all_exist

def check_config_files():
    """Check configuration files"""
    print("\nChecking Configuration Files:")
    print("-" * 30)
    
    files_to_check = [
        (".env", "Environment Variables"),
        ("config/settings.py", "Settings Configuration"),
        ("config/chatbot_config.py", "Chatbot Configuration")
    ]
    
    all_exist = True
    for file_path, description in files_to_check:
        if not check_file_exists(file_path, description):
            all_exist = False
    
    return all_exist

def check_source_files():
    """Check source code files"""
    print("\nChecking Source Files:")
    print("-" * 30)
    
    files_to_check = [
        ("src/chatbot.py", "Main Chatbot"),
        ("src/data_extraction.py", "Data Extraction"),
        ("src/data_organization.py", "Data Organization"),
        ("src/train_chatbot.py", "Training Module"),
        ("src/integration.py", "Web Integration"),
        ("src/testing.py", "Testing Module")
    ]
    
    all_exist = True
    for file_path, description in files_to_check:
        if not check_file_exists(file_path, description):
            all_exist = False
    
    return all_exist

def check_runner_files():
    """Check runner scripts"""
    print("\nChecking Runner Scripts:")
    print("-" * 30)
    
    files_to_check = [
        ("run_chatbot.py", "CLI Runner"),
        ("run_web.py", "Web Runner"),
        ("initialize.py", "Initialization Script"),
        ("install_dependencies.py", "Dependency Installer")
    ]
    
    all_exist = True
    for file_path, description in files_to_check:
        if not check_file_exists(file_path, description):
            all_exist = False
    
    return all_exist

def check_data_content():
    """Check data file contents"""
    print("\nChecking Data Content:")
    print("-" * 30)
    
    try:
        # Check structured data
        with open("data/structured_data.json", 'r') as f:
            structured_data = json.load(f)
        
        courses_count = len(structured_data.get("courses", {}).get("undergraduate", {}).get("btech", []))
        faq_count = len(structured_data.get("faq", []))
        
        print(f"✓ Structured Data: {courses_count} courses, {faq_count} FAQs")
        
        # Check organized data
        with open("data/organized_data.json", 'r') as f:
            organized_data = json.load(f)
        
        categories_count = len(organized_data.get("categories", {}))
        keywords_count = len(organized_data.get("search_index", {}))
        
        print(f"✓ Organized Data: {categories_count} categories, {keywords_count} keywords")
        
        return True
        
    except Exception as e:
        print(f"✗ Data Content Check Failed: {str(e)}")
        return False

def check_api_key():
    """Check if API key is configured"""
    print("\nChecking API Configuration:")
    print("-" * 30)
    
    try:
        with open(".env", 'r') as f:
            env_content = f.read()
        
        if "GEMINI_API_KEY" in env_content and "AIzaSyAh9YFINFypPDH3i5adUIxlfkv6Fydkzgg" in env_content:
            print("✓ Gemini API Key: Configured")
            return True
        else:
            print("✗ Gemini API Key: Not found or incorrect")
            return False
            
    except Exception as e:
        print(f"✗ API Key Check Failed: {str(e)}")
        return False

def test_import():
    """Test if modules can be imported"""
    print("\nTesting Module Imports:")
    print("-" * 30)
    
    modules_to_test = [
        ("src.chatbot", "Chatbot Module"),
        ("src.integration", "Integration Module"),
        ("src.data_extraction", "Data Extraction"),
        ("src.data_organization", "Data Organization"),
        ("src.train_chatbot", "Training Module")
    ]
    
    all_imported = True
    sys.path.insert(0, str(Path.cwd()))
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✓ {description}: Import successful")
        except Exception as e:
            print(f"✗ {description}: Import failed - {str(e)}")
            all_imported = False
    
    return all_imported

def generate_status_report():
    """Generate comprehensive status report"""
    print("MMMUT Chatbot - System Status Check")
    print("=" * 50)
    print(f"Check Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Run all checks
    checks = [
        ("Data Files", check_data_files()),
        ("Configuration Files", check_config_files()),
        ("Source Files", check_source_files()),
        ("Runner Scripts", check_runner_files()),
        ("Data Content", check_data_content()),
        ("API Configuration", check_api_key()),
        ("Module Imports", test_import())
    ]
    
    # Summary
    print("\n" + "=" * 50)
    print("STATUS SUMMARY")
    print("=" * 50)
    
    passed_checks = 0
    total_checks = len(checks)
    
    for check_name, result in checks:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{check_name:20}: {status}")
        if result:
            passed_checks += 1
    
    print("-" * 50)
    print(f"Overall Status: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("🎉 ALL SYSTEMS READY!")
        print("\nYou can now run:")
        print("  python3 run_chatbot.py    # CLI interface")
        print("  python3 run_web.py        # Web interface")
        return True
    else:
        print("⚠️  SOME ISSUES FOUND!")
        print("\nPlease fix the failed checks before deployment.")
        print("Run: python3 initialize.py to reinitialize if needed.")
        return False

def main():
    """Main function"""
    try:
        success = generate_status_report()
        return 0 if success else 1
    except Exception as e:
        print(f"Status check failed: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())