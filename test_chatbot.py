#!/usr/bin/env python3
"""
Test script for MMMUT chatbot
"""

import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_chatbot():
    """Test the chatbot with sample queries"""
    try:
        print("Testing MMMUT Admission Chatbot...")
        print("=" * 50)
        
        from chatbot import AdmissionChatbot
        
        # Initialize chatbot
        chatbot = AdmissionChatbot()
        
        # Test queries
        test_queries = [
            "Hello",
            "What courses are offered?",
            "What is the fee structure?",
            "What are the eligibility criteria?",
            "Where is MMMUT located?"
        ]
        
        print("Running test queries:")
        print("-" * 30)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n{i}. Query: '{query}'")
            try:
                response = chatbot.process_query(query)
                print(f"   Response: {response['response'][:100]}...")
                print(f"   Type: {response['response_type']}")
                print(f"   Confidence: {response['confidence']:.2f}")
            except Exception as e:
                print(f"   Error: {str(e)}")
        
        # Get statistics
        print("\n" + "=" * 50)
        print("Chatbot Statistics:")
        stats = chatbot.get_statistics()
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        print("\n✓ Chatbot test completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Error testing chatbot: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_chatbot()
    sys.exit(0 if success else 1)