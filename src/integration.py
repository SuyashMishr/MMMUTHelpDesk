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
            response_data["status"] = "success"
            
            return response_data
            
        except Exception as e:
            logger.error(f"Error in get_response: {str(e)}")
            return {
                "response": "I apologize, but I'm experiencing technical difficulties. Please try again.",
                "response_type": "error",
                "confidence": 0.0,
                "session_id": session_id,
                "status": "error",
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

        @self.app.route('/favicon.ico')
        def favicon():
            """Serve favicon"""
            return '', 204  # No content, prevents 404 error
    
    def _get_chat_html(self) -> str:
        """Get modern HTML template for chat interface"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MMMUT Admission Help Desk - AI Assistant</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-color: #059669;
            --primary-dark: #047857;
            --secondary-color: #f0fdf4;
            --accent-color: #10b981;
            --text-primary: #1e293b;
            --text-secondary: #64748b;
            --border-color: #dcfce7;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --error-color: #ef4444;
            --gradient-bg: linear-gradient(135deg, #34d399 0%, #059669 100%);
            --chat-bg: #ffffff;
            --message-user-bg: var(--primary-color);
            --message-bot-bg: #f0fdf4;
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--gradient-bg);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1rem;
            line-height: 1.6;
        }

        .chat-container {
            width: 100%;
            max-width: 900px;
            height: 85vh;
            min-height: 600px;
            background: var(--chat-bg);
            border-radius: 20px;
            box-shadow: var(--shadow-xl);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .chat-header {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
            color: white;
            padding: 1.5rem 2rem;
            position: relative;
            overflow: hidden;
        }

        .chat-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml;charset=utf-8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"></path></pattern></defs><rect width="100" height="100" fill="url(%23grid)"></rect></svg>');
            opacity: 0.3;
        }

        .header-content {
            position: relative;
            z-index: 1;
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .university-logo {
            width: 50px;
            height: 50px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }

        .header-text h1 {
            font-size: 1.75rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
            letter-spacing: -0.025em;
        }

        .header-text p {
            opacity: 0.9;
            font-size: 0.95rem;
            font-weight: 400;
        }

        .status-indicator {
            position: absolute;
            top: 1.5rem;
            right: 2rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.875rem;
            opacity: 0.9;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background: var(--success-color);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .chat-messages {
            flex: 1;
            padding: 1.5rem;
            overflow-y: auto;
            background: linear-gradient(to bottom, #f8fafc 0%, #f1f5f9 100%);
            scroll-behavior: smooth;
        }

        .chat-messages::-webkit-scrollbar {
            width: 6px;
        }

        .chat-messages::-webkit-scrollbar-track {
            background: transparent;
        }

        .chat-messages::-webkit-scrollbar-thumb {
            background: var(--border-color);
            border-radius: 3px;
        }

        .chat-messages::-webkit-scrollbar-thumb:hover {
            background: var(--text-secondary);
        }

        .message {
            margin-bottom: 1.5rem;
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
            animation: fadeInUp 0.3s ease-out;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .message.user {
            justify-content: flex-end;
            flex-direction: row-reverse;
        }

        .message-avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.875rem;
            font-weight: 600;
            flex-shrink: 0;
        }

        .message.bot .message-avatar {
            background: linear-gradient(135deg, var(--accent-color), #22c55e);
            color: white;
        }

        .message.user .message-avatar {
            background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
            color: white;
        }

        .message-content {
            max-width: 75%;
            padding: 1rem 1.25rem;
            border-radius: 18px;
            word-wrap: break-word;
            position: relative;
            box-shadow: var(--shadow-sm);
        }

        .message.bot .message-content {
            background: var(--message-bot-bg);
            color: var(--text-primary);
            border-bottom-left-radius: 6px;
            border: 1px solid var(--border-color);
        }

        .message.user .message-content {
            background: var(--message-user-bg);
            color: white;
            border-bottom-right-radius: 6px;
        }

        .message-time {
            font-size: 0.75rem;
            opacity: 0.6;
            margin-top: 0.5rem;
            display: block;
        }

        .confidence-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            font-size: 0.75rem;
            padding: 0.25rem 0.5rem;
            background: rgba(16, 185, 129, 0.1);
            color: var(--success-color);
            border-radius: 12px;
            margin-top: 0.5rem;
            font-weight: 500;
        }

        .typing-indicator {
            display: none;
            padding: 1rem 1.5rem;
            color: var(--text-secondary);
            font-style: italic;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .typing-dots {
            display: flex;
            gap: 0.25rem;
        }

        .typing-dot {
            width: 6px;
            height: 6px;
            background: var(--text-secondary);
            border-radius: 50%;
            animation: typingDot 1.4s infinite ease-in-out;
        }

        .typing-dot:nth-child(1) { animation-delay: -0.32s; }
        .typing-dot:nth-child(2) { animation-delay: -0.16s; }

        @keyframes typingDot {
            0%, 80%, 100% {
                transform: scale(0);
                opacity: 0.5;
            }
            40% {
                transform: scale(1);
                opacity: 1;
            }
        }

        .chat-input {
            padding: 1.5rem 2rem;
            background: white;
            border-top: 1px solid var(--border-color);
            display: flex;
            gap: 1rem;
            align-items: flex-end;
        }

        .input-container {
            flex: 1;
            position: relative;
        }

        .chat-input textarea {
            width: 100%;
            padding: 1rem 1.25rem;
            border: 2px solid var(--border-color);
            border-radius: 24px;
            outline: none;
            font-size: 0.95rem;
            font-family: inherit;
            transition: all 0.2s ease;
            resize: none;
            min-height: 48px;
            max-height: 120px;
            overflow-y: auto;
            line-height: 1.4;
        }

        .chat-input textarea:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }

        .chat-input textarea::placeholder {
            color: var(--text-secondary);
            opacity: 0.7;
        }

        .send-button {
            padding: 0.75rem;
            background: var(--primary-color);
            color: white;
            border: none;
            border-radius: 50%;
            cursor: pointer;
            font-size: 1.125rem;
            transition: all 0.2s ease;
            width: 48px;
            height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: var(--shadow-md);
        }

        .send-button:hover:not(:disabled) {
            background: var(--primary-dark);
            transform: translateY(-1px);
            box-shadow: var(--shadow-lg);
        }

        .send-button:disabled {
            background: var(--text-secondary);
            cursor: not-allowed;
            transform: none;
            box-shadow: var(--shadow-sm);
        }

        .quick-suggestions {
            display: flex;
            gap: 0.5rem;
            padding: 0 1.5rem 1rem;
            flex-wrap: wrap;
        }

        .suggestion-chip {
            padding: 0.5rem 1rem;
            background: white;
            border: 1px solid var(--border-color);
            border-radius: 20px;
            font-size: 0.875rem;
            cursor: pointer;
            transition: all 0.2s ease;
            color: var(--text-secondary);
        }

        .suggestion-chip:hover {
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
        }

        @media (max-width: 768px) {
            body {
                padding: 0.5rem;
            }

            .chat-container {
                height: 100vh;
                border-radius: 0;
            }

            .chat-header {
                padding: 1rem 1.5rem;
            }

            .header-text h1 {
                font-size: 1.5rem;
            }

            .chat-messages {
                padding: 1rem;
            }

            .chat-input {
                padding: 1rem 1.5rem;
            }

            .message-content {
                max-width: 85%;
            }
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <div class="header-content">
                <div class="university-logo">
                    <i class="fas fa-graduation-cap"></i>
                </div>
                <div class="header-text">
                    <h1>MMMUT Admission Help Desk</h1>
                    <p>AI-powered assistance for your admission queries</p>
                </div>
            </div>
            <div class="status-indicator">
                <div class="status-dot"></div>
                <span>Online</span>
            </div>
        </div>

        <div class="chat-messages" id="chatMessages">
            <div class="message bot">
                <div class="message-avatar">AI</div>
                <div class="message-content">
                    <strong>Welcome to MMMUT Admission Help Desk! 🎓</strong><br><br>
                    I'm your AI assistant, here to help you with all admission-related queries for Madan Mohan Malaviya University of Technology, Gorakhpur.<br><br>
                    <strong>I can help you with:</strong><br>
                    • Course details and eligibility criteria<br>
                    • Admission procedures and important dates<br>
                    • Fee structure and payment options<br>
                    • Campus facilities and placement information<br><br>
                    How can I assist you today?
                    <span class="message-time" id="welcomeTime"></span>
                </div>
            </div>
        </div>

        <div class="quick-suggestions">
            <div class="suggestion-chip" onclick="sendSuggestion('What engineering courses are available at MMMUT?')">📚 Available Courses</div>
            <div class="suggestion-chip" onclick="sendSuggestion('What are the eligibility criteria for B.Tech admission?')">✅ Eligibility Criteria</div>
            <div class="suggestion-chip" onclick="sendSuggestion('What is the complete fee structure for engineering courses?')">💰 Fee Structure</div>
            <div class="suggestion-chip" onclick="sendSuggestion('What are the important admission dates and deadlines?')">📅 Important Dates</div>
            <div class="suggestion-chip" onclick="sendSuggestion('Tell me about campus facilities and hostel accommodation')">🏫 Campus Facilities</div>
            <div class="suggestion-chip" onclick="sendSuggestion('What are the placement statistics and career opportunities?')">🎯 Placement Info</div>
        </div>

        <div class="typing-indicator" id="typingIndicator">
            <i class="fas fa-robot"></i>
            <span>AI is thinking</span>
            <div class="typing-dots">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>

        <div class="chat-input">
            <div class="input-container">
                <textarea id="messageInput" placeholder="Ask me anything about MMMUT admissions... (e.g., 'What courses are available?', 'Tell me about fees', 'Eligibility criteria for CSE')" maxlength="1000" rows="1"></textarea>
            </div>
            <button class="send-button" id="sendButton" onclick="sendMessage()">
                <i class="fas fa-paper-plane"></i>
            </button>
        </div>
    </div>

    <script>
        let sessionId = null;
        let messageCount = 0;

        // Define functions first to ensure they're available
        function sendMessage() {
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

            fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: message,
                    session_id: sessionId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    sessionId = data.session_id;
                    setTimeout(() => {
                        addMessage(data.response, false, data.confidence, data.response_type);
                    }, 500);
                } else {
                    setTimeout(() => {
                        addMessage('I apologize, but I encountered an error processing your request. Please try rephrasing your question or contact the admission office directly.', false);
                    }, 800);
                }
            })
            .catch(error => {
                console.error('Connection error:', error);
                setTimeout(() => {
                    addMessage('I am having trouble connecting to the server. Please check your internet connection and try again.', false);
                }, 800);
            })
            .finally(() => {
                setTimeout(() => {
                    hideTypingIndicator();
                    sendButton.disabled = false;
                    input.focus();
                }, 1000);
            });
        }

        function sendSuggestion(suggestion) {
            const input = document.getElementById('messageInput');
            input.value = suggestion;
            input.focus();
            sendMessage();
        }

        // Make functions globally accessible
        window.sendMessage = sendMessage;
        window.sendSuggestion = sendSuggestion;

        // Initialize welcome message time
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('welcomeTime').textContent = new Date().toLocaleTimeString();
            document.getElementById('messageInput').focus();
        });

        function formatMessage(content) {
            // Convert markdown-like formatting to HTML
            return content
                .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
                .replace(/\\*(.*?)\\*/g, '<em>$1</em>')
                .replace(/\\n/g, '<br>')
                .replace(/• /g, '• ');
        }

        function addMessage(content, isUser = false, confidence = null, responseType = null) {
            const messagesContainer = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;

            const currentTime = new Date().toLocaleTimeString();
            const avatar = isUser ? 'YOU' : 'AI';
            const formattedContent = isUser ? content : formatMessage(content);

            let confidenceBadge = '';
            if (confidence !== null && !isUser && confidence > 0.7) {
                const confidenceIcon = confidence > 0.9 ? '🎯' : confidence > 0.8 ? '✅' : '👍';
                confidenceBadge = `<div class="confidence-badge">
                    <i class="fas fa-check-circle"></i>
                    ${confidenceIcon} ${(confidence * 100).toFixed(0)}% confident
                </div>`;
            }

            messageDiv.innerHTML = `
                <div class="message-avatar">${avatar}</div>
                <div class="message-content">
                    ${formattedContent}
                    ${confidenceBadge}
                    <span class="message-time">${currentTime}</span>
                </div>
            `;

            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            messageCount++;
        }





        function showTypingIndicator() {
            const indicator = document.getElementById('typingIndicator');
            indicator.style.display = 'flex';
            const messagesContainer = document.getElementById('chatMessages');
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        function hideTypingIndicator() {
            document.getElementById('typingIndicator').style.display = 'none';
        }



        // Enhanced keyboard handling
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        // Auto-resize textarea
        const messageInput = document.getElementById('messageInput');
        messageInput.addEventListener('input', function() {
            // Reset height to auto to get the correct scrollHeight
            this.style.height = 'auto';
            // Set height based on scrollHeight, with min and max limits
            const newHeight = Math.min(Math.max(this.scrollHeight, 48), 120);
            this.style.height = newHeight + 'px';
        });

        // Add some helpful keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            // Focus input with Ctrl+/ (fixed regex issue)
            if (e.ctrlKey && e.key === '/') {
                e.preventDefault();
                document.getElementById('messageInput').focus();
            }
        });

        // Add connection status monitoring
        let isOnline = navigator.onLine;

        window.addEventListener('online', function() {
            isOnline = true;
            document.querySelector('.status-indicator span').textContent = 'Online';
            document.querySelector('.status-dot').style.background = 'var(--success-color)';
        });

        window.addEventListener('offline', function() {
            isOnline = false;
            document.querySelector('.status-indicator span').textContent = 'Offline';
            document.querySelector('.status-dot').style.background = 'var(--error-color)';
        });
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
        web_app = FlaskWebIntegration(host="0.0.0.0", port=8080)
        
        print("Web server starting...")
        print("Access the chatbot at: http://localhost:8080")
        print("API endpoint: http://localhost:8080/api/chat")
        print("Widget: http://localhost:8080/widget")
        print("Health check: http://localhost:8080/api/health")
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