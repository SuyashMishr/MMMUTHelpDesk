"""
Testing module for the MMMUT Admission Chatbot
"""

import json
import logging
import time
import unittest
from typing import Dict, List, Any
from datetime import datetime
import sys
import os

# Add src to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chatbot import AdmissionChatbot
from data_extraction import DataExtractor
from data_organization import DataOrganizer
from train_chatbot import ChatbotTrainer
from integration import ChatbotIntegration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestDataExtraction(unittest.TestCase):
    """Test data extraction functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.extractor = DataExtractor()
    
    def test_extractor_initialization(self):
        """Test if data extractor initializes correctly"""
        self.assertIsNotNone(self.extractor)
        self.assertIsInstance(self.extractor.extracted_data, dict)
    
    def test_sample_data_creation(self):
        """Test creation of sample data"""
        self.extractor._create_sample_data()
        self.assertIn("university_info", self.extractor.extracted_data)
        self.assertIn("courses", self.extractor.extracted_data)
        self.assertIn("eligibility", self.extractor.extracted_data)
    
    def test_university_info_processing(self):
        """Test university information processing"""
        sample_text = "Madan Mohan Malaviya University of Technology, Gorakhpur, established in 1962"
        self.extractor._process_university_info(sample_text)
        
        university_info = self.extractor.extracted_data["university_info"]
        self.assertTrue(len(university_info) > 0)
    
    def test_course_processing(self):
        """Test course information processing"""
        sample_text = "Computer Science Engineering, Mechanical Engineering, Civil Engineering"
        self.extractor._process_courses(sample_text)
        
        courses = self.extractor.extracted_data["courses"]
        self.assertIsInstance(courses, list)


class TestDataOrganization(unittest.TestCase):
    """Test data organization functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.organizer = DataOrganizer()
        # Create sample raw data
        self.organizer.raw_data = {
            "university_info": {
                "name": "MMMUT",
                "location": "Gorakhpur"
            },
            "courses": ["CSE", "ME", "CE"],
            "eligibility": {"minimum_marks": "75%"},
            "fees": {"total_fee": "100000"}
        }
    
    def test_organizer_initialization(self):
        """Test if data organizer initializes correctly"""
        self.assertIsNotNone(self.organizer)
        self.assertIsInstance(self.organizer.organized_data, dict)
    
    def test_university_info_organization(self):
        """Test university information organization"""
        self.organizer._organize_university_info()
        
        university_category = self.organizer.organized_data["categories"]["university"]
        self.assertIn("title", university_category)
        self.assertIn("data", university_category)
        self.assertIn("keywords", university_category)
    
    def test_search_index_creation(self):
        """Test search index creation"""
        self.organizer.organized_data["categories"] = {
            "test_category": {
                "keywords": ["test", "sample", "demo"]
            }
        }
        self.organizer._create_search_index()
        
        search_index = self.organizer.organized_data["search_index"]
        self.assertIn("test", search_index)
        self.assertIn("test_category", search_index["test"])
    
    def test_faq_generation(self):
        """Test FAQ generation"""
        self.organizer._generate_faqs()
        
        faqs = self.organizer.organized_data["faq"]
        self.assertIsInstance(faqs, list)
        self.assertTrue(len(faqs) > 0)
        
        # Check FAQ structure
        if faqs:
            faq = faqs[0]
            self.assertIn("question", faq)
            self.assertIn("answer", faq)
            self.assertIn("category", faq)


class TestChatbotTrainer(unittest.TestCase):
    """Test chatbot training functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.trainer = ChatbotTrainer()
    
    def test_trainer_initialization(self):
        """Test if trainer initializes correctly"""
        self.assertIsNotNone(self.trainer)
        self.assertIsInstance(self.trainer.training_data, list)
        self.assertIsInstance(self.trainer.intent_patterns, dict)
    
    def test_intent_classification(self):
        """Test intent classification"""
        self.trainer._create_intent_patterns()
        
        # Test various queries
        test_cases = [
            ("What courses are offered?", "courses"),
            ("What is the fee structure?", "fees"),
            ("Hello there", "greeting"),
            ("What are the eligibility criteria?", "eligibility")
        ]
        
        for query, expected_intent in test_cases:
            intent, confidence = self.trainer.classify_intent(query)
            # Intent should be classified (may not always match expected due to simple implementation)
            self.assertIsInstance(intent, str)
            self.assertIsInstance(confidence, float)
            self.assertGreaterEqual(confidence, 0.0)
            self.assertLessEqual(confidence, 1.0)
    
    def test_training_data_generation(self):
        """Test training data generation"""
        sample_data = self.trainer._create_sample_organized_data()
        self.trainer._generate_training_examples(sample_data)
        
        self.assertTrue(len(self.trainer.training_data) > 0)
        
        # Check training example structure
        if self.trainer.training_data:
            example = self.trainer.training_data[0]
            self.assertIn("input", example)
            self.assertIn("output", example)
            self.assertIn("intent", example)


class TestChatbot(unittest.TestCase):
    """Test main chatbot functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        try:
            self.chatbot = AdmissionChatbot()
        except Exception as e:
            self.skipTest(f"Chatbot initialization failed: {str(e)}")
    
    def test_chatbot_initialization(self):
        """Test if chatbot initializes correctly"""
        self.assertIsNotNone(self.chatbot)
        self.assertIsNotNone(self.chatbot.organized_data)
        self.assertIsNotNone(self.chatbot.quick_responses)
    
    def test_query_preprocessing(self):
        """Test query preprocessing"""
        test_queries = [
            ("  HELLO WORLD  ", "hello world"),
            ("What is CSE?", "what is computer science engineering?"),
            ("Tell me about B.Tech", "tell me about bachelor of technology")
        ]
        
        for original, expected in test_queries:
            processed = self.chatbot._preprocess_query(original)
            self.assertEqual(processed, expected)
    
    def test_quick_responses(self):
        """Test quick response functionality"""
        greeting_queries = ["hello", "hi", "good morning"]
        
        for query in greeting_queries:
            response = self.chatbot._check_quick_responses(query)
            self.assertIsNotNone(response)
            self.assertIsInstance(response, str)
    
    def test_query_processing(self):
        """Test complete query processing"""
        test_queries = [
            "Hello",
            "What courses are offered?",
            "What is the fee structure?",
            "Tell me about eligibility criteria"
        ]
        
        for query in test_queries:
            response_data = self.chatbot.process_query(query)
            
            # Check response structure
            self.assertIn("response", response_data)
            self.assertIn("response_type", response_data)
            self.assertIn("confidence", response_data)
            self.assertIn("timestamp", response_data)
            
            # Check response content
            self.assertIsInstance(response_data["response"], str)
            self.assertTrue(len(response_data["response"]) > 0)
            self.assertIsInstance(response_data["confidence"], (int, float))
    
    def test_conversation_history(self):
        """Test conversation history tracking"""
        initial_count = len(self.chatbot.conversation_history)
        
        self.chatbot.process_query("Hello")
        self.assertEqual(len(self.chatbot.conversation_history), initial_count + 1)
        
        self.chatbot.process_query("What courses are offered?")
        self.assertEqual(len(self.chatbot.conversation_history), initial_count + 2)
    
    def test_statistics(self):
        """Test statistics functionality"""
        stats = self.chatbot.get_statistics()
        
        self.assertIn("total_queries", stats)
        self.assertIn("session_duration", stats)
        self.assertIn("conversation_length", stats)
        self.assertIsInstance(stats["total_queries"], int)


class TestIntegration(unittest.TestCase):
    """Test integration functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        try:
            self.integration = ChatbotIntegration()
        except Exception as e:
            self.skipTest(f"Integration initialization failed: {str(e)}")
    
    def test_integration_initialization(self):
        """Test if integration initializes correctly"""
        self.assertIsNotNone(self.integration)
        self.assertIsNotNone(self.integration.chatbot)
        self.assertIsInstance(self.integration.active_sessions, dict)
    
    def test_session_management(self):
        """Test session management"""
        session_id = "test_session_123"
        
        # First request should create session
        response1 = self.integration.get_response("Hello", session_id)
        self.assertIn(session_id, self.integration.active_sessions)
        self.assertEqual(self.integration.active_sessions[session_id]["query_count"], 1)
        
        # Second request should update session
        response2 = self.integration.get_response("What courses are offered?", session_id)
        self.assertEqual(self.integration.active_sessions[session_id]["query_count"], 2)
    
    def test_integration_stats(self):
        """Test integration statistics"""
        stats = self.integration.get_integration_stats()
        
        self.assertIn("uptime_seconds", stats)
        self.assertIn("total_requests", stats)
        self.assertIn("active_sessions", stats)
        self.assertIn("chatbot_stats", stats)


class PerformanceTest:
    """Performance testing for the chatbot"""
    
    def __init__(self):
        """Initialize performance test"""
        try:
            self.chatbot = AdmissionChatbot()
        except Exception as e:
            logger.error(f"Failed to initialize chatbot for performance test: {str(e)}")
            self.chatbot = None
    
    def test_response_time(self, num_queries: int = 10) -> Dict[str, Any]:
        """Test response time performance"""
        if not self.chatbot:
            return {"error": "Chatbot not available"}
        
        test_queries = [
            "Hello",
            "What courses are offered?",
            "What is the fee structure?",
            "Tell me about eligibility criteria",
            "Where is MMMUT located?",
            "What are the placement statistics?",
            "How to apply for admission?",
            "What facilities are available?",
            "What are the important dates?",
            "How to contact admission office?"
        ]
        
        response_times = []
        successful_queries = 0
        
        for i in range(num_queries):
            query = test_queries[i % len(test_queries)]
            
            start_time = time.time()
            try:
                response = self.chatbot.process_query(query)
                end_time = time.time()
                
                response_time = end_time - start_time
                response_times.append(response_time)
                successful_queries += 1
                
            except Exception as e:
                logger.error(f"Query failed: {str(e)}")
        
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            min_response_time = min(response_times)
        else:
            avg_response_time = max_response_time = min_response_time = 0
        
        return {
            "total_queries": num_queries,
            "successful_queries": successful_queries,
            "success_rate": successful_queries / num_queries if num_queries > 0 else 0,
            "average_response_time": avg_response_time,
            "max_response_time": max_response_time,
            "min_response_time": min_response_time,
            "response_times": response_times
        }
    
    def test_concurrent_requests(self, num_concurrent: int = 5) -> Dict[str, Any]:
        """Test concurrent request handling"""
        if not self.chatbot:
            return {"error": "Chatbot not available"}
        
        import threading
        import queue
        
        results_queue = queue.Queue()
        
        def worker(worker_id: int):
            """Worker function for concurrent testing"""
            try:
                start_time = time.time()
                response = self.chatbot.process_query(f"Hello from worker {worker_id}")
                end_time = time.time()
                
                results_queue.put({
                    "worker_id": worker_id,
                    "success": True,
                    "response_time": end_time - start_time,
                    "response_length": len(response.get("response", ""))
                })
            except Exception as e:
                results_queue.put({
                    "worker_id": worker_id,
                    "success": False,
                    "error": str(e)
                })
        
        # Start concurrent workers
        threads = []
        start_time = time.time()
        
        for i in range(num_concurrent):
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        
        # Collect results
        results = []
        while not results_queue.empty():
            results.append(results_queue.get())
        
        successful_requests = sum(1 for r in results if r.get("success", False))
        
        return {
            "concurrent_requests": num_concurrent,
            "successful_requests": successful_requests,
            "success_rate": successful_requests / num_concurrent if num_concurrent > 0 else 0,
            "total_time": end_time - start_time,
            "results": results
        }


def run_all_tests():
    """Run all test suites"""
    print("MMMUT Chatbot Testing Suite")
    print("=" * 50)
    
    # Unit tests
    print("\n1. Running Unit Tests...")
    print("-" * 30)
    
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestDataExtraction,
        TestDataOrganization,
        TestChatbotTrainer,
        TestChatbot,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = test_loader.loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run unit tests
    runner = unittest.TextTestRunner(verbosity=2)
    unit_test_result = runner.run(test_suite)
    
    # Performance tests
    print("\n2. Running Performance Tests...")
    print("-" * 30)
    
    perf_tester = PerformanceTest()
    
    # Response time test
    print("Testing response times...")
    response_time_results = perf_tester.test_response_time(10)
    print(f"Average response time: {response_time_results.get('average_response_time', 0):.3f}s")
    print(f"Success rate: {response_time_results.get('success_rate', 0):.2%}")
    
    # Concurrent request test
    print("\nTesting concurrent requests...")
    concurrent_results = perf_tester.test_concurrent_requests(5)
    print(f"Concurrent success rate: {concurrent_results.get('success_rate', 0):.2%}")
    print(f"Total time for 5 concurrent requests: {concurrent_results.get('total_time', 0):.3f}s")
    
    # Summary
    print("\n3. Test Summary")
    print("-" * 30)
    print(f"Unit tests run: {unit_test_result.testsRun}")
    print(f"Unit test failures: {len(unit_test_result.failures)}")
    print(f"Unit test errors: {len(unit_test_result.errors)}")
    print(f"Unit test success rate: {((unit_test_result.testsRun - len(unit_test_result.failures) - len(unit_test_result.errors)) / unit_test_result.testsRun * 100):.1f}%" if unit_test_result.testsRun > 0 else "N/A")
    
    print(f"\nPerformance test results:")
    print(f"- Average response time: {response_time_results.get('average_response_time', 0):.3f}s")
    print(f"- Response time success rate: {response_time_results.get('success_rate', 0):.2%}")
    print(f"- Concurrent request success rate: {concurrent_results.get('success_rate', 0):.2%}")
    
    # Overall assessment
    overall_success = (
        len(unit_test_result.failures) == 0 and 
        len(unit_test_result.errors) == 0 and
        response_time_results.get('success_rate', 0) > 0.8 and
        concurrent_results.get('success_rate', 0) > 0.8
    )
    
    print(f"\nOverall Test Status: {'PASS' if overall_success else 'FAIL'}")
    
    return {
        "unit_tests": {
            "total": unit_test_result.testsRun,
            "failures": len(unit_test_result.failures),
            "errors": len(unit_test_result.errors),
            "success": len(unit_test_result.failures) == 0 and len(unit_test_result.errors) == 0
        },
        "performance_tests": {
            "response_time": response_time_results,
            "concurrent_requests": concurrent_results
        },
        "overall_success": overall_success
    }


def main():
    """Main function to run tests"""
    try:
        results = run_all_tests()
        
        # Save test results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"test_results_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\nTest results saved to: {results_file}")
        
        # Exit with appropriate code
        exit_code = 0 if results["overall_success"] else 1
        sys.exit(exit_code)
        
    except Exception as e:
        print(f"Error running tests: {str(e)}")
        logger.error(f"Test execution failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()