#!/usr/bin/env python3
"""
Final comprehensive test for MMMUT chatbot
"""

import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def comprehensive_test():
    """Run comprehensive tests on the chatbot"""
    try:
        print("MMMUT Admission Chatbot - Comprehensive Test")
        print("=" * 60)
        
        from chatbot import AdmissionChatbot
        
        # Initialize chatbot
        print("Initializing chatbot...")
        chatbot = AdmissionChatbot()
        print("✓ Chatbot initialized successfully")
        
        # Test queries covering all categories
        test_queries = [
            # Greeting
            "Hello, I need help with MMMUT admission",
            
            # University info
            "Tell me about MMMUT university",
            "Where is MMMUT located?",
            "When was MMMUT established?",
            
            # Courses
            "What courses are offered at MMMUT?",
            "Tell me about Computer Science Engineering",
            "How many seats are available in CSE?",
            "What specializations are available in IT?",
            
            # Eligibility
            "What are the eligibility criteria for B.Tech?",
            "What percentage is required for admission?",
            "Is JEE Main required for admission?",
            
            # Fees
            "What is the fee structure for B.Tech?",
            "How much is the hostel fee?",
            "What is the total cost for 4 years?",
            "Are scholarships available?",
            
            # Admission process
            "What is the admission process?",
            "What documents are required?",
            "When do applications start?",
            
            # Facilities
            "What facilities are available on campus?",
            "Tell me about the library",
            "Are hostels available?",
            
            # Placement
            "What is the placement record?",
            "Which companies visit for placement?",
            "What is the average package?",
            
            # Contact
            "How can I contact the admission office?",
            "What is the phone number?",
            "What is the email address?"
        ]
        
        print(f"\nRunning {len(test_queries)} test queries...")
        print("-" * 60)
        
        successful_responses = 0
        ai_responses = 0
        quick_responses = 0
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n{i:2d}. Query: '{query}'")
            
            try:
                response = chatbot.process_query(query)
                
                # Get response text
                if isinstance(response['response'], list):
                    response_text = response['response'][0]
                else:
                    response_text = response['response']
                
                # Display response (truncated)
                display_text = response_text[:100] + "..." if len(response_text) > 100 else response_text
                print(f"    Response: {display_text}")
                print(f"    Type: {response['response_type']}")
                print(f"    Confidence: {response['confidence']:.2f}")
                
                # Count response types
                if response['response_type'] == 'ai_generated':
                    ai_responses += 1
                elif response['response_type'] == 'quick':
                    quick_responses += 1
                
                successful_responses += 1
                
            except Exception as e:
                print(f"    ✗ Error: {str(e)}")
        
        # Display statistics
        print("\n" + "=" * 60)
        print("Test Results Summary:")
        print(f"✓ Total queries tested: {len(test_queries)}")
        print(f"✓ Successful responses: {successful_responses}")
        print(f"✓ AI-generated responses: {ai_responses}")
        print(f"✓ Quick responses: {quick_responses}")
        print(f"✓ Success rate: {(successful_responses/len(test_queries)*100):.1f}%")
        
        # Get chatbot statistics
        print("\nChatbot Statistics:")
        stats = chatbot.get_statistics()
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        print("\n" + "=" * 60)
        print("✓ Comprehensive test completed successfully!")
        
        return successful_responses == len(test_queries)
        
    except Exception as e:
        print(f"✗ Error during comprehensive test: {str(e)}")
        return False

def test_web_integration():
    """Test web integration"""
    try:
        print("\nTesting Web Integration...")
        print("-" * 30)
        
        from integration import ChatbotIntegration
        
        # Initialize web integration
        web_chatbot = ChatbotIntegration()
        print("✓ Web integration initialized")
        
        # Test API-style query
        test_query = "What courses are offered?"
        response = web_chatbot.get_response(test_query)
        
        print(f"Test query: '{test_query}'")
        print(f"Response: {response['response'][:100]}...")
        print(f"Status: {response['status']}")
        
        print("✓ Web integration test passed")
        return True
        
    except Exception as e:
        print(f"✗ Web integration test failed: {str(e)}")
        return False

def main():
    """Main test function"""
    print("Starting Final Comprehensive Test")
    print("=" * 60)
    
    # Test 1: Comprehensive chatbot test
    chatbot_success = comprehensive_test()
    
    # Test 2: Web integration test
    web_success = test_web_integration()
    
    # Final results
    print("\n" + "=" * 60)
    print("FINAL TEST RESULTS")
    print("=" * 60)
    print(f"Chatbot Test: {'✓ PASSED' if chatbot_success else '✗ FAILED'}")
    print(f"Web Integration Test: {'✓ PASSED' if web_success else '✗ FAILED'}")
    
    overall_success = chatbot_success and web_success
    print(f"\nOverall Result: {'✓ ALL TESTS PASSED' if overall_success else '✗ SOME TESTS FAILED'}")
    
    if overall_success:
        print("\n🎉 MMMUT Admission Chatbot is ready for deployment!")
        print("\nNext steps:")
        print("1. Run: python run_chatbot.py (for CLI)")
        print("2. Run: python run_web.py (for web interface)")
        print("3. Deploy to your preferred hosting platform")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)