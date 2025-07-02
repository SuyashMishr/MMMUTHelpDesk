# 🎓 MMMUT Admission Help Desk

A modern, AI-powered chatbot system designed to assist prospective students with admission-related queries for **Madan Mohan Malaviya University of Technology (MMMUT)**, Gorakhpur.

## ✨ Features

- **🤖 AI-Powered Intelligence**: Uses Google Gemini AI for intelligent, context-aware responses
- **📚 Comprehensive Information**: Covers courses, eligibility, fees, important dates, and facilities
- **💻 Modern Web Interface**: Beautiful, responsive design with real-time chat experience
- **🔄 Session Management**: Maintains conversation context across interactions
- **📊 Smart Analytics**: Confidence scoring and response quality metrics
- **🌐 RESTful API**: Clean API endpoints for integration with other systems
- **📱 Mobile Responsive**: Works seamlessly on all devices

## 📁 Project Structure

```
MMMUTHelpDesk/
├── 🚀 app.py                    # Main application entry point
├── 📁 src/
│   ├── 🤖 chatbot.py           # Core chatbot logic with AI integration
│   ├── 🌐 integration.py       # Web interface and API endpoints
│   └── 📄 __init__.py
├── ⚙️ config/
│   ├── 🔧 settings.py          # Application configuration
│   └── 🎛️ chatbot_config.py    # AI model and chatbot settings
├── 📊 data/
│   ├── 📋 organized_data.json   # Processed admission data
│   ├── 📄 structured_data.json # Raw structured data
│   └── 📁 raw_data/            # Original PDF documents
├── 📦 requirements.txt          # Python dependencies
└── 📖 README.md                # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd MMMUTHelpDesk
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
# Create a .env file in the root directory
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
```

### 🏃‍♂️ Running the Application

**Start the web application:**
```bash
python app.py
```

Then open your browser and go to: **http://localhost:5000**

### Direct Module Usage
```bash
# Extract data from brochures
python src/data_extraction.py

# Organize extracted data
python src/data_organization.py

# Train the chatbot
python src/train_chatbot.py

# Run tests
python src/testing.py
```

## 🌐 Web Integration

### API Endpoints
- `GET /` - Web chat interface
- `POST /api/chat` - Chat API endpoint
- `GET /api/stats` - Statistics
- `GET /api/health` - Health check
- `GET /widget` - Embeddable widget

### Example API Usage
```python
import requests

response = requests.post('http://localhost:5000/api/chat', json={
    'query': 'What courses are offered?',
    'session_id': 'user123'
})

data = response.json()
print(data['response'])
```

### Integration Code
```python
from src.integration import ChatbotIntegration

# Initialize the chatbot
chatbot = ChatbotIntegration()

# Get response for a query
response = chatbot.get_response("What are the admission requirements?")
print(response['response'])
```

## 📊 Configuration

The chatbot is pre-configured with your Gemini API key. You can modify settings in:

- `config/settings.py` - General settings
- `config/chatbot_config.py` - AI model parameters
- `.env` - Environment variables

## 🧪 Testing

```bash
# Run all tests
python src/testing.py

# Or run specific test modules
python -m pytest src/testing.py -v
```

## 📝 Sample Queries

Try these queries with the chatbot:
- "What courses are offered at MMMUT?"
- "What is the fee structure?"
- "What are the eligibility criteria?"
- "When do applications start?"
- "Tell me about placement statistics"
- "What facilities are available?"
- "How to contact admission office?"

## 🔧 Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed
   ```bash
   python install_dependencies.py
   ```

2. **API Key Issues**: Check your `.env` file contains the correct Gemini API key

3. **Permission Errors**: On macOS, you might need to use:
   ```bash
   pip install --user --break-system-packages package_name
   ```

4. **Virtual Environment Issues**: Use the manual setup option instead

### Getting Help

If you encounter issues:
1. Check the error messages carefully
2. Ensure your API key is correct
3. Try the different setup options
4. Create an issue on GitHub

## 📁 Data Management

### Adding Your Own Data
1. Place PDF files in `data/raw_data/`
2. Run `python src/data_extraction.py`
3. Run `python src/data_organization.py`

### Sample Data
If no PDF files are provided, the system uses built-in sample data about MMMUT.

## 🚀 Deployment

### Local Development
```bash
python run_web.py
```

### Production Deployment
1. Set `FLASK_ENV=production` in `.env`
2. Use a proper WSGI server like Gunicorn
3. Configure reverse proxy (nginx)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- **Suyash Mishra** - *Initial work* - [SuyashMishr](https://github.com/SuyashMishr)

## 🙏 Acknowledgments

- MMMUT for providing the admission information
- Google for the Gemini AI API
- The open-source community for various tools and libraries

## 📞 Support

For support:
- Create an issue on GitHub
- Email: [your-email@example.com]
- Check the troubleshooting section above

---

**🔐 Security Note**: Your API key is already configured in the `.env` file. Keep this file secure and never share it publicly.