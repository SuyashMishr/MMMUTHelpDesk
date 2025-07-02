# MMMUT Help Desk Chatbot - Deployment Guide

## 🚀 Quick Start

### Option 1: Automatic Setup (Recommended)
```bash
git clone https://github.com/SuyashMishr/MMMUTHelpDesk.git
cd MMMUTHelpDesk
python3 install_dependencies.py
python3 initialize.py
python3 run_chatbot.py
```

### Option 2: Manual Setup
```bash
git clone https://github.com/SuyashMishr/MMMUTHelpDesk.git
cd MMMUTHelpDesk
pip install -r requirements.txt
python3 src/data_extraction.py
python3 src/data_organization.py
python3 src/train_chatbot.py
python3 run_chatbot.py
```

## 📋 System Requirements

- Python 3.8 or higher
- Internet connection (for Gemini AI API)
- 500MB free disk space
- 2GB RAM (recommended)

## 🔧 Configuration

### API Key Setup
The Gemini API key is pre-configured in `.env`:
```
GEMINI_API_KEY=AIzaSyAh9YFINFypPDH3i5adUIxlfkv6Fydkzgg
```

### Customization
- Modify `config/chatbot_config.py` for AI parameters
- Update `config/settings.py` for file paths
- Edit `data/structured_data.json` to add your own data

## 🌐 Web Deployment

### Local Development
```bash
python3 run_web.py
# Access at http://localhost:5000
```

### Production Deployment

#### Using Gunicorn (Linux/macOS)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 src.integration:app
```

#### Using Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN python3 initialize.py
EXPOSE 5000
CMD ["python3", "run_web.py"]
```

#### Deploy to Heroku
```bash
# Create Procfile
echo "web: python3 run_web.py" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

#### Deploy to Railway
```bash
# railway.json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python3 run_web.py"
  }
}
```

## 🔌 API Integration

### REST API Endpoints
- `POST /api/chat` - Send chat message
- `GET /api/stats` - Get chatbot statistics
- `GET /api/health` - Health check

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

### JavaScript Integration
```javascript
async function sendMessage(message) {
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            query: message,
            session_id: 'web_user'
        })
    });
    
    const data = await response.json();
    return data.response;
}
```

## 📊 Monitoring and Analytics

### Built-in Statistics
```python
from src.chatbot import AdmissionChatbot

chatbot = AdmissionChatbot()
stats = chatbot.get_statistics()
print(stats)
```

### Log Files
- Application logs: Check console output
- Error logs: Stored in system logs
- Usage analytics: Available via `/api/stats`

## 🔒 Security Considerations

### API Key Security
- Never commit API keys to version control
- Use environment variables in production
- Rotate API keys regularly

### Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)
```

### CORS Configuration
```python
CORS(app, origins=['https://yourdomain.com'])
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   python3 install_dependencies.py
   ```

2. **API Key Issues**
   - Check `.env` file exists
   - Verify API key is correct
   - Ensure internet connection

3. **Permission Errors (macOS)**
   ```bash
   pip install --user --break-system-packages package_name
   ```

4. **Port Already in Use**
   ```bash
   # Change port in run_web.py
   app.run(host='0.0.0.0', port=5001, debug=False)
   ```

### Debug Mode
```bash
export FLASK_DEBUG=1
python3 run_web.py
```

## 📈 Performance Optimization

### Caching
- Enable response caching for common queries
- Use Redis for session storage
- Implement database caching

### Load Balancing
```bash
# Multiple workers
gunicorn -w 4 -b 0.0.0.0:8000 src.integration:app

# With nginx
upstream chatbot {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
}
```

## 🔄 Updates and Maintenance

### Updating Data
```bash
# Add new PDF to data/raw_data/
python3 src/data_extraction.py
python3 src/data_organization.py
python3 src/train_chatbot.py
```

### Backup
```bash
# Backup important files
tar -czf backup.tar.gz data/ config/ .env
```

### Health Checks
```bash
# Check if service is running
curl http://localhost:5000/api/health
```

## 📞 Support

### Getting Help
- Check the troubleshooting section
- Review error logs
- Create GitHub issue
- Contact: admission@mmmut.ac.in

### Contributing
1. Fork the repository
2. Create feature branch
3. Make changes
4. Submit pull request

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

---

**Note**: This chatbot is designed specifically for MMMUT admission queries. Customize the data and responses according to your institution's requirements.