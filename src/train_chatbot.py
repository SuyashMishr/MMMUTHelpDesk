"""
Training module for the MMMUT Admission Chatbot
This module handles data preparation and chatbot training/fine-tuning
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatbotTrainer:
    """Train and prepare the chatbot with admission data"""
    
    def __init__(self):
        """Initialize the trainer"""
        self.training_data = []
        self.validation_data = []
        self.knowledge_base = {}
        self.intent_patterns = {}
        
        logger.info("Chatbot trainer initialized")
    
    def prepare_training_data(self) -> Dict[str, Any]:
        """Prepare training data from organized admission data"""
        try:
            try:
                import sys
                sys.path.append(str(Path(__file__).parent.parent))
                from config.settings import DATA_DIR
                organized_data_path = DATA_DIR / "organized_data.json"
            except ImportError:
                # Fallback to default path
                organized_data_path = Path(__file__).parent.parent / "data" / "organized_data.json"
            if organized_data_path.exists():
                with open(organized_data_path, 'r', encoding='utf-8') as f:
                    organized_data = json.load(f)
            else:
                logger.warning("Organized data not found, creating sample training data")
                organized_data = self._create_sample_organized_data()
            
            # Generate training examples
            self._generate_training_examples(organized_data)
            
            # Create intent patterns
            self._create_intent_patterns()
            
            # Build knowledge base
            self._build_knowledge_base(organized_data)
            
            # Split data for training and validation
            self._split_training_data()
            
            logger.info(f"Training data prepared: {len(self.training_data)} examples")
            return {
                "training_examples": len(self.training_data),
                "validation_examples": len(self.validation_data),
                "intent_patterns": len(self.intent_patterns),
                "knowledge_base_entries": len(self.knowledge_base)
            }
            
        except Exception as e:
            logger.error(f"Error preparing training data: {str(e)}")
            raise
    
    def _create_sample_organized_data(self) -> Dict[str, Any]:
        """Create sample organized data for training"""
        return {
            "categories": {
                "university": {
                    "data": {
                        "name": "Madan Mohan Malaviya University of Technology",
                        "location": "Gorakhpur, Uttar Pradesh",
                        "established": "1962",
                        "type": "Government University"
                    }
                },
                "courses": {
                    "data": {
                        "undergraduate": {
                            "engineering": [
                                "Computer Science and Engineering",
                                "Information Technology",
                                "Electronics and Communication Engineering",
                                "Electrical Engineering",
                                "Mechanical Engineering",
                                "Civil Engineering"
                            ]
                        }
                    }
                },
                "eligibility": {
                    "data": {
                        "minimum_marks": "75% in 10+2",
                        "qualifying_exam": "10+2 with PCM",
                        "entrance_exam": "JEE Main"
                    }
                },
                "fees": {
                    "data": {
                        "tuition_fee": "50000",
                        "hostel_fee": "25000",
                        "total_fee": "100000"
                    }
                }
            },
            "faq": [
                {
                    "question": "What is the eligibility criteria?",
                    "answer": "10+2 with PCM and 75% marks, qualify JEE Main",
                    "category": "eligibility"
                }
            ]
        }
    
    def _generate_training_examples(self, organized_data: Dict[str, Any]):
        """Generate training examples from organized data"""
        categories = organized_data.get("categories", {})
        faqs = organized_data.get("faq", [])
        
        # Generate examples from categories
        for category_name, category_data in categories.items():
            self._generate_category_examples(category_name, category_data)
        
        # Generate examples from FAQs
        for faq in faqs:
            self.training_data.append({
                "input": faq["question"],
                "output": faq["answer"],
                "intent": faq.get("category", "general"),
                "confidence": 1.0
            })
        
        # Generate variations and paraphrases
        self._generate_variations()
    
    def _generate_category_examples(self, category_name: str, category_data: Dict[str, Any]):
        """Generate training examples for a specific category"""
        data = category_data.get("data", {})
        
        if category_name == "university":
            examples = [
                ("What is MMMUT?", f"MMMUT is {data.get('name', 'Madan Mohan Malaviya University of Technology')}"),
                ("Where is MMMUT located?", f"MMMUT is located in {data.get('location', 'Gorakhpur, Uttar Pradesh')}"),
                ("When was MMMUT established?", f"MMMUT was established in {data.get('established', '1962')}"),
                ("Tell me about MMMUT", f"MMMUT is a {data.get('type', 'Government')} university located in {data.get('location', 'Gorakhpur')}")
            ]
        
        elif category_name == "courses":
            courses = data.get("undergraduate", {}).get("engineering", [])
            course_list = ", ".join(courses) if courses else "Computer Science, IT, ECE, EE, ME, CE"
            examples = [
                ("What courses are offered?", f"MMMUT offers B.Tech in {course_list}"),
                ("Which branches are available?", f"Available branches: {course_list}"),
                ("Tell me about engineering courses", f"Engineering courses available: {course_list}")
            ]
        
        elif category_name == "eligibility":
            examples = [
                ("What is the eligibility criteria?", f"Eligibility: {data.get('minimum_marks', '75% in 10+2')}, {data.get('qualifying_exam', '10+2 with PCM')}"),
                ("What are the admission requirements?", f"Requirements: {data.get('entrance_exam', 'JEE Main qualification')} and {data.get('minimum_marks', '75% marks')}"),
                ("Am I eligible for admission?", f"You need {data.get('minimum_marks', '75% in 10+2')} and qualify {data.get('entrance_exam', 'JEE Main')}")
            ]
        
        elif category_name == "fees":
            total_fee = data.get('total_fee', '100000')
            examples = [
                ("What is the fee structure?", f"Annual fee is approximately ₹{total_fee}"),
                ("How much does it cost?", f"Total annual fee: ₹{total_fee}"),
                ("Tell me about fees", f"Fee structure includes tuition and other charges, total ₹{total_fee}")
            ]
        
        else:
            # Generic examples for other categories
            examples = [
                (f"Tell me about {category_name}", f"Here's information about {category_name}: {str(data)[:200]}...")
            ]
        
        # Add examples to training data
        for question, answer in examples:
            self.training_data.append({
                "input": question,
                "output": answer,
                "intent": category_name,
                "confidence": 0.9
            })
    
    def _generate_variations(self):
        """Generate variations and paraphrases of training examples"""
        original_data = self.training_data.copy()
        
        # Question variations
        question_variations = {
            "what is": ["tell me about", "can you explain", "what do you know about"],
            "where is": ["what is the location of", "where can I find"],
            "when": ["what time", "at what time"],
            "how much": ["what is the cost", "what are the fees", "how expensive"],
            "which": ["what", "what are the"]
        }
        
        for example in original_data:
            input_text = example["input"].lower()
            
            # Generate variations
            for original, variations in question_variations.items():
                if original in input_text:
                    for variation in variations:
                        new_input = input_text.replace(original, variation)
                        self.training_data.append({
                            "input": new_input.capitalize(),
                            "output": example["output"],
                            "intent": example["intent"],
                            "confidence": example["confidence"] * 0.8
                        })
    
    def _create_intent_patterns(self):
        """Create intent recognition patterns"""
        self.intent_patterns = {
            "greeting": [
                r"(?i)\b(hello|hi|hey|good morning|good afternoon|good evening)\b",
                r"(?i)\b(greetings|salutations)\b"
            ],
            "university_info": [
                r"(?i)\b(about|what is|tell me about)\s+(mmmut|university)\b",
                r"(?i)\b(location|where|address)\b.*\b(mmmut|university)\b"
            ],
            "courses": [
                r"(?i)\b(courses?|programs?|branches?|streams?)\b",
                r"(?i)\b(engineering|btech|b\.tech)\b.*\b(courses?|programs?)\b",
                r"(?i)\b(computer science|mechanical|civil|electrical)\b"
            ],
            "eligibility": [
                r"(?i)\b(eligibility|criteria|requirements?|qualifications?)\b",
                r"(?i)\b(eligible|qualify|minimum marks)\b",
                r"(?i)\b(10\+2|intermediate|jee)\b"
            ],
            "fees": [
                r"(?i)\b(fees?|cost|payment|money|expensive|cheap)\b",
                r"(?i)\b(how much|price|charges?)\b",
                r"(?i)\b(scholarship|financial aid)\b"
            ],
            "dates": [
                r"(?i)\b(dates?|deadline|when|schedule|timeline)\b",
                r"(?i)\b(application|admission|exam)\s+(date|deadline)\b",
                r"(?i)\b(last date|important dates)\b"
            ],
            "contact": [
                r"(?i)\b(contact|phone|email|address|office)\b",
                r"(?i)\b(reach|call|write|visit)\b",
                r"(?i)\b(help|support|assistance)\b"
            ],
            "facilities": [
                r"(?i)\b(facilities|infrastructure|hostel|library)\b",
                r"(?i)\b(campus|labs?|laboratories)\b",
                r"(?i)\b(sports|gym|cafeteria)\b"
            ],
            "placement": [
                r"(?i)\b(placement|jobs?|career|recruitment)\b",
                r"(?i)\b(salary|package|companies)\b",
                r"(?i)\b(internship|training)\b"
            ]
        }
    
    def _build_knowledge_base(self, organized_data: Dict[str, Any]):
        """Build knowledge base from organized data"""
        categories = organized_data.get("categories", {})
        
        for category_name, category_data in categories.items():
            self.knowledge_base[category_name] = {
                "data": category_data.get("data", {}),
                "keywords": category_data.get("keywords", []),
                "description": category_data.get("description", "")
            }
        
        # Add FAQs to knowledge base
        faqs = organized_data.get("faq", [])
        self.knowledge_base["faqs"] = faqs
        
        # Add quick responses
        quick_responses = organized_data.get("quick_responses", {})
        self.knowledge_base["quick_responses"] = quick_responses
    
    def _split_training_data(self):
        """Split data into training and validation sets"""
        total_examples = len(self.training_data)
        split_index = int(total_examples * 0.8)  # 80% for training, 20% for validation
        
        # Shuffle data
        import random
        random.shuffle(self.training_data)
        
        self.validation_data = self.training_data[split_index:]
        self.training_data = self.training_data[:split_index]
    
    def classify_intent(self, text: str) -> Tuple[str, float]:
        """Classify intent of input text"""
        text_lower = text.lower()
        best_intent = "general"
        best_score = 0.0
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    # Simple scoring based on pattern match
                    score = len(re.findall(pattern, text_lower)) * 0.3
                    if score > best_score:
                        best_score = score
                        best_intent = intent
        
        return best_intent, min(best_score, 1.0)
    
    def get_relevant_knowledge(self, intent: str, query: str) -> Dict[str, Any]:
        """Get relevant knowledge for a given intent and query"""
        if intent in self.knowledge_base:
            return self.knowledge_base[intent]
        
        # Fallback: search for relevant knowledge
        relevant_data = {}
        query_words = set(query.lower().split())
        
        for category, data in self.knowledge_base.items():
            if category == "faqs":
                continue
            
            keywords = data.get("keywords", [])
            if any(keyword in query_words for keyword in keywords):
                relevant_data[category] = data
        
        return relevant_data
    
    def save_training_data(self, output_dir: str = None):
        """Save training data and models"""
        if output_dir is None:
            try:
                import sys
                sys.path.append(str(Path(__file__).parent.parent))
                from config.settings import DATA_DIR
                output_dir = DATA_DIR / "training"
            except ImportError:
                # Fallback to default path
                output_dir = Path(__file__).parent.parent / "data" / "training"
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(exist_ok=True)
        
        # Save training data
        training_file = output_dir / "training_data.json"
        with open(training_file, 'w', encoding='utf-8') as f:
            json.dump({
                "training_data": self.training_data,
                "validation_data": self.validation_data,
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "total_examples": len(self.training_data) + len(self.validation_data),
                    "training_examples": len(self.training_data),
                    "validation_examples": len(self.validation_data)
                }
            }, f, indent=2, ensure_ascii=False)
        
        # Save intent patterns
        patterns_file = output_dir / "intent_patterns.json"
        with open(patterns_file, 'w', encoding='utf-8') as f:
            json.dump(self.intent_patterns, f, indent=2, ensure_ascii=False)
        
        # Save knowledge base
        kb_file = output_dir / "knowledge_base.json"
        with open(kb_file, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge_base, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Training data saved to: {output_dir}")
    
    def evaluate_model(self) -> Dict[str, float]:
        """Evaluate the trained model (simplified evaluation)"""
        if not self.validation_data:
            logger.warning("No validation data available")
            return {"accuracy": 0.0}
        
        correct_predictions = 0
        total_predictions = len(self.validation_data)
        
        for example in self.validation_data:
            predicted_intent, confidence = self.classify_intent(example["input"])
            if predicted_intent == example["intent"]:
                correct_predictions += 1
        
        accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0.0
        
        return {
            "accuracy": accuracy,
            "total_examples": total_predictions,
            "correct_predictions": correct_predictions
        }
    
    def generate_training_report(self) -> Dict[str, Any]:
        """Generate comprehensive training report"""
        evaluation_results = self.evaluate_model()
        
        # Intent distribution
        intent_distribution = {}
        for example in self.training_data + self.validation_data:
            intent = example["intent"]
            intent_distribution[intent] = intent_distribution.get(intent, 0) + 1
        
        return {
            "training_summary": {
                "total_examples": len(self.training_data) + len(self.validation_data),
                "training_examples": len(self.training_data),
                "validation_examples": len(self.validation_data),
                "intent_patterns": len(self.intent_patterns),
                "knowledge_base_entries": len(self.knowledge_base)
            },
            "evaluation_results": evaluation_results,
            "intent_distribution": intent_distribution,
            "training_date": datetime.now().isoformat()
        }


def main():
    """Main function to run chatbot training"""
    try:
        print("MMMUT Chatbot Training")
        print("=" * 50)
        
        # Initialize trainer
        trainer = ChatbotTrainer()
        
        # Prepare training data
        print("Preparing training data...")
        preparation_results = trainer.prepare_training_data()
        print(f"Training data prepared: {preparation_results}")
        
        # Save training data
        print("Saving training data...")
        trainer.save_training_data()
        
        # Generate report
        print("Generating training report...")
        report = trainer.generate_training_report()
        
        print("\nTraining Report:")
        print("=" * 30)
        print(json.dumps(report, indent=2))
        
        # Test intent classification
        print("\nTesting Intent Classification:")
        print("-" * 30)
        test_queries = [
            "What courses are offered?",
            "What is the fee structure?",
            "What are the eligibility criteria?",
            "Hello, how are you?",
            "Where is MMMUT located?"
        ]
        
        for query in test_queries:
            intent, confidence = trainer.classify_intent(query)
            print(f"Query: '{query}' -> Intent: {intent} (Confidence: {confidence:.2f})")
        
        print("\nTraining completed successfully!")
        
    except Exception as e:
        print(f"Error during training: {str(e)}")
        logger.error(f"Training failed: {str(e)}")


if __name__ == "__main__":
    main()