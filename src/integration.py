"""
Integration module for embedding the chatbot into websites and applications
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import threading
import time

try:
    from .chatbot import AdmissionChatbot
except ImportError:
    from chatbot import AdmissionChatbot

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatbotIntegration:
    """Integration class for embedding chatbot in various platforms"""
    
    def __init__(self):
        """Initialize the integration"""
        self.chatbot = AdmissionChatbot()
        self.active_sessions = {}
        self.request_count = 0
        self.start_time = datetime.now()
        
        logger.info("Chatbot integration initialized")
    
    def get_response(self, query: str, session_id: str = None) -> Dict[str, Any]:
        """Get response from chatbot with session management"""
        try:
            if session_id is None:
                session_id = f"session_{int(time.time())}"
            
            # Track session
            if session_id not in self.active_sessions:
                self.active_sessions[session_id] = {
                    "start_time": datetime.now(),
                    "query_count": 0,
                    "last_activity": datetime.now()
                }
            
            # Update session info
            self.active_sessions[session_id]["query_count"] += 1
            self.active_sessions[session_id]["last_activity"] = datetime.now()
            self.request_count += 1
            
            # Get response from chatbot
            response_data = self.chatbot.process_query(query, session_id)
            
            # Add session info to response
            response_data["session_id"] = session_id
            response_data["session_query_count"] = self.active_sessions[session_id]["query_count"]
            
            return response_data
            
        except Exception as e:
            logger.error(f"Error in get_response: {str(e)}")
            return {
                "response": "I apologize, but I'm experiencing technical difficulties. Please try again.",
                "response_type": "error",
                "confidence": 0.0,
                "session_id": session_id,
                "error": str(e)
            }
    
    def cleanup_sessions(self, max_inactive_minutes: int = 30):
        """Clean up inactive sessions"""
        current_time = datetime.now()
        inactive_sessions = []
        
        for session_id, session_data in self.active_sessions.items():
            inactive_duration = current_time - session_data["last_activity"]
            if inactive_duration.total_seconds() > (max_inactive_minutes * 60):
                inactive_sessions.append(session_id)
        
        for session_id in inactive_sessions:
            del self.active_sessions[session_id]
        
        if inactive_sessions:
            logger.info(f"Cleaned up {len(inactive_sessions)} inactive sessions")
    
    def get_integration_stats(self) -> Dict[str, Any]:
        """Get integration statistics"""
        current_time = datetime.now()
        uptime = current_time - self.start_time
        
        return {
            "uptime_seconds": uptime.total_seconds(),
            "total_requests": self.request_count,
            "active_sessions": len(self.active_sessions),
            "requests_per_minute": self.request_count / max(uptime.total_seconds() / 60, 1),
            "chatbot_stats": self.chatbot.get_statistics()
        }


class FlaskWebIntegration:
    """Flask web application for chatbot integration"""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 5000):
        """Initialize Flask web integration"""
        self.app = Flask(__name__)
        CORS(self.app)  # Enable CORS for cross-origin requests
        
        self.host = host
        self.port = port
        self.integration = ChatbotIntegration()
        
        # Setup routes
        self._setup_routes()
        
        # Start session cleanup thread
        self._start_cleanup_thread()
        
        logger.info(f"Flask web integration initialized on {host}:{port}")
    
    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def home():
            """Home page with chatbot interface"""
            return render_template_string(self._get_chat_html())
        
        @self.app.route('/api/chat', methods=['POST'])
        def chat_api():
            """Chat API endpoint"""
            try:
                data = request.get_json()
                
                if not data or 'query' not in data:
                    return jsonify({
                        "error": "Missing 'query' in request body",
                        "status": "error"
                    }), 400
                
                query = data['query'].strip()
                session_id = data.get('session_id')
                
                if not query:
                    return jsonify({
                        "error": "Empty query",
                        "status": "error"
                    }), 400
                
                # Get response from chatbot
                response_data = self.integration.get_response(query, session_id)
                response_data["status"] = "success"
                
                return jsonify(response_data)
                
            except Exception as e:
                logger.error(f"Error in chat API: {str(e)}")
                return jsonify({
                    "error": "Internal server error",
                    "status": "error"
                }), 500
        
        @self.app.route('/api/stats', methods=['GET'])
        def stats_api():
            """Statistics API endpoint"""
            try:
                stats = self.integration.get_integration_stats()
                return jsonify({
                    "stats": stats,
                    "status": "success"
                })
            except Exception as e:
                logger.error(f"Error in stats API: {str(e)}")
                return jsonify({
                    "error": "Failed to get statistics",
                    "status": "error"
                }), 500
        
        @self.app.route('/api/health', methods=['GET'])
        def health_check():
            """Health check endpoint"""
            return jsonify({
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "service": "MMMUT Admission Chatbot"
            })
        
        @self.app.route('/widget')
        def chat_widget():
            """Embeddable chat widget"""
            return render_template_string(self._get_widget_html())
    
    def _get_chat_html(self) -> str:
        """Get HTML template for chat interface"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MMMUT Admission Help Desk</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .chat-container {
            width: 90%;
            max-width: 800px;
            height: 80vh;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .chat-header {
            background: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
        }
        
        .chat-header h1 {
            font-size: 1.5em;
            margin-bottom: 5px;
        }
        
        .chat-header p {
            opacity: 0.8;
            font-size: 0.9em;
        }
        
        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: #f8f9fa;
        }
        
        .message {
            margin-bottom: 15px;
            display: flex;
            align-items: flex-start;
        }
        
        .message.user {
            justify-content: flex-end;
        }
        
        .message-content {
            max-width: 70%;
            padding: 12px 16px;
            border-radius: 18px;
            word-wrap: break-word;
        }
        
        .message.bot .message-content {
            background: #e3f2fd;
            color: #1565c0;
            border-bottom-left-radius: 5px;
        }
        
        .message.user .message-content {
            background: #2196f3;
            color: white;
            border-bottom-right-radius: 5px;
        }
        
        .chat-input {
            padding: 20px;
            background: white;
            border-top: 1px solid #eee;
            display: flex;
            gap: 10px;
        }
        
        .chat-input input {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            outline: none;
            font-size: 14px;
        }
        
        .chat-input input:focus {
            border-color: #2196f3;
        }
        
        .chat-input button {
            padding: 12px 24px;
            background: #2196f3;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.3s;
        }
        
        .chat-input button:hover {
            background: #1976d2;
        }
        
        .chat-input button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        
        .typing-indicator {
            display: none;
            padding: 10px;
            font-style: italic;
            color: #666;
        }
        
        .confidence-badge {
            font-size: 0.8em;
            opacity: 0.7;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h1>MMMUT Admission Help Desk</h1>
            <p>Ask me anything about admissions at MMMUT</p>
        </div>
        
        <div class="chat-messages" id="chatMessages">
            <div class="message bot">
                <div class="message-content">
                    Hello! Welcome to MMMUT Admission Help Desk. I'm here to help you with your admission queries. You can ask me about courses, eligibility criteria, fees, important dates, and more!
                </div>
            </div>
        </div>
        
        <div class="typing-indicator" id="typingIndicator">
            Bot is typing...
        </div>
        
        <div class="chat-input">
            <input type="text" id="messageInput" placeholder="Type your question here..." maxlength="500">
            <button id="sendButton" onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        let sessionId = null;
        
        function addMessage(content, isUser = false, confidence = null) {
            const messagesContainer = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
            
            let confidenceBadge = '';
            if (confidence !== null && !isUser) {
                confidenceBadge = `<div class="confidence-badge">Confidence: ${(confidence * 100).toFixed(0)}%</div>`;
            }
            
            messageDiv.innerHTML = `
                <div class="message-content">
                    ${content}
                    ${confidenceBadge}
                </div>
            `;
            
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
        
        function showTypingIndicator() {
            document.getElementById('typingIndicator').style.display = 'block';
        }
        
        function hideTypingIndicator() {
            document.getElementById('typingIndicator').style.display = 'none';
        }
        
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const sendButton = document.getElementById('sendButton');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message
            addMessage(message, true);
            
            // Clear input and disable button
            input.value = '';
            sendButton.disabled = true;
            showTypingIndicator();
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        query: message,
                        session_id: sessionId
                    })
                });
                
                const data = await response.json();
                
                if (data.status === 'success') {
                    sessionId = data.session_id;
                    addMessage(data.response, false, data.confidence);
                } else {
                    addMessage('Sorry, I encountered an error. Please try again.', false);
                }
                
            } catch (error) {
                console.error('Error:', error);
                addMessage('Sorry, I\'m having trouble connecting. Please try again.', false);
            } finally {
                hideTypingIndicator();
                sendButton.disabled = false;
                input.focus();
            }
        }
        
        // Handle Enter key
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Focus input on load
        document.getElementById('messageInput').focus();
    </script>
</body>
</html>
        """
    
    def _get_widget_html(self) -> str:
        """Get HTML template for embeddable widget"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MMMUT Chat Widget</title>
    <style>
        .chat-widget {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 350px;
            height: 500px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
            display: flex;
            flex-direction: column;
            z-index: 1000;
        }
        
        .widget-header {
            background: #2196f3;
            color: white;
            padding: 15px;
            border-radius: 10px 10px 0 0;
            text-align: center;
        }
        
        .widget-messages {
            flex: 1;
            padding: 10px;
            overflow-y: auto;
            font-size: 14px;
        }
        
        .widget-input {
            padding: 10px;
            border-top: 1px solid #eee;
            display: flex;
            gap: 5px;
        }
        
        .widget-input input {
            flex: 1;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 15px;
            outline: none;
        }
        
        .widget-input button {
            padding: 8px 12px;
            background: #2196f3;
            color: white;
            border: none;
            border-radius: 15px;
            cursor: pointer;
        }
        
        .widget-message {
            margin-bottom: 10px;
            padding: 8px 12px;
            border-radius: 15px;
            max-width: 80%;
        }
        
        .widget-message.bot {
            background: #f0f0f0;
            align-self: flex-start;
        }
        
        .widget-message.user {
            background: #2196f3;
            color: white;
            align-self: flex-end;
            margin-left: auto;
        }
    </style>
</head>
<body>
    <div class="chat-widget">
        <div class="widget-header">
            <h3>MMMUT Help Desk</h3>
        </div>
        <div class="widget-messages" id="widgetMessages">
            <div class="widget-message bot">
                Hi! How can I help you with MMMUT admissions?
            </div>
        </div>
        <div class="widget-input">
            <input type="text" id="widgetInput" placeholder="Ask a question...">
            <button onclick="sendWidgetMessage()">Send</button>
        </div>
    </div>
    
    <script>
        // Widget JavaScript code here
        // Similar to main chat but simplified for widget
    </script>
</body>
</html>
        """
    
    def _start_cleanup_thread(self):
        """Start background thread for session cleanup"""
        def cleanup_worker():
            while True:
                time.sleep(300)  # Run every 5 minutes
                self.integration.cleanup_sessions()
        
        cleanup_thread = threading.Thread(target=cleanup_worker, daemon=True)
        cleanup_thread.start()
    
    def run(self, debug: bool = False):
        """Run the Flask application"""
        logger.info(f"Starting Flask web server on {self.host}:{self.port}")
        self.app.run(host=self.host, port=self.port, debug=debug)


class APIIntegration:
    """REST API integration for the chatbot"""
    
    def __init__(self):
        """Initialize API integration"""
        self.integration = ChatbotIntegration()
    
    def create_api_response(self, query: str, session_id: str = None) -> Dict[str, Any]:
        """Create standardized API response"""
        response_data = self.integration.get_response(query, session_id)
        
        return {
            "success": True,
            "data": {
                "response": response_data["response"],
                "confidence": response_data.get("confidence", 0.0),
                "response_type": response_data.get("response_type", "unknown"),
                "session_id": response_data.get("session_id"),
                "timestamp": response_data.get("timestamp")
            },
            "metadata": {
                "query": query,
                "processing_time": "< 1s",
                "sources": response_data.get("sources", [])
            }
        }


def main():
    """Main function to run web integration"""
    try:
        print("Starting MMMUT Chatbot Web Integration")
        print("=" * 50)
        
        # Create Flask web integration
        web_app = FlaskWebIntegration(host="0.0.0.0", port=5000)
        
        print("Web server starting...")
        print("Access the chatbot at: http://localhost:5000")
        print("API endpoint: http://localhost:5000/api/chat")
        print("Widget: http://localhost:5000/widget")
        print("Health check: http://localhost:5000/api/health")
        print("\nPress Ctrl+C to stop the server")
        
        # Run the web server
        web_app.run(debug=True)
        
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error running web integration: {str(e)}")
        logger.error(f"Web integration failed: {str(e)}")


if __name__ == "__main__":
    main()