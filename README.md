# MMMUT Help Desk - Admission Chatbot

A comprehensive chatbot system for MMMUT (Madan Mohan Malaviya University of Technology) admission queries, built using Google's Gemini AI.

## 🎯 Project Overview

This project creates an intelligent chatbot that can answer admission-related queries for MMMUT by processing the official UG Admission Brochure and providing accurate, contextual responses to prospective students.

## 🏗️ Project Structure

```
MMMUTHelpDesk/
│
├── data/
│   ├── raw_data/                # Raw data files (e.g., UG Admission Brochure PDF)
│   └── structured_data.json     # Structured data after extraction
│
├── src/
│   ├── __init__.py              # Initialize the project
│   ├── data_extraction.py       # Extract data from the admission brochure
│   ├── data_organization.py     # Organize the extracted data into categories
│   ├── chatbot.py               # Main chatbot code using Gemini API
│   ├── train_chatbot.py         # Train the chatbot with the extracted data
│   ├── integration.py           # Code to integrate chatbot into the website
│   └── testing.py               # Testing the chatbot functionality
│
├── config/
│   ├── settings.py              # Configuration settings (API keys, paths, etc.)
│   └── chatbot_config.py        # Chatbot-specific configurations
│
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (API keys)
├── setup.py                    # Complete setup script
├── initialize.py               # Data initialization script
├── install_dependencies.py     # Dependency installation script
├── run_chatbot.py              # Run chatbot CLI
├── run_web.py                  # Run web interface
└── README.md                   # This file
```

## 🚀 Features

- **PDF Data Extraction**: Automatically extracts information from admission brochures
- **Intelligent Query Processing**: Uses Google Gemini AI for natural language understanding
- **Structured Data Organization**: Categorizes admission information for efficient retrieval
- **Web Integration**: Ready-to-integrate chatbot for websites
- **Command Line Interface**: Interactive CLI for testing
- **Comprehensive Testing**: Full test suite for reliability

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key: `AIzaSyAh9YFINFypPDH3i5adUIxlfkv6Fydkzgg`
- Git

## 🛠️ Quick Setup (Recommended)

### Option 1: Automatic Setup
```bash
# Clone the repository
git clone https://github.com/SuyashMishr/MMMUTHelpDesk.git
cd MMMUTHelpDesk

# Run automatic setup (creates virtual environment and installs everything)
python setup.py
```

### Option 2: Manual Setup
```bash
# Clone the repository
git clone https://github.com/SuyashMishr/MMMUTHelpDesk.git
cd MMMUTHelpDesk

# Install dependencies (uses system Python)
python install_dependencies.py

# Initialize data
python initialize.py
```

### Option 3: Traditional Setup
```bash
# Clone the repository
git clone https://github.com/SuyashMishr/MMMUTHelpDesk.git
cd MMMUTHelpDesk

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize data
python initialize.py
```

## 🎮 Usage

### Command Line Interface
```bash
python run_chatbot.py
```

### Web Interface
```bash
python run_web.py
```
Then open your browser to `http://localhost:5000`

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