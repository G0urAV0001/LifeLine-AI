# LifeLine AI - Emergency Response System

An AI-powered emergency response system that provides real-time assistance during medical emergencies through intelligent emergency detection, hospital locating, and SOS coordination.

## Features

- **AI Emergency Detection**: Analyzes text, images, and voice inputs to identify emergency types and severity
- **Hospital Finder**: Locates nearby hospitals with real-time availability
- **SOS Alerts**: Trigger emergency alerts that notify services and emergency contacts
- **Emergency History**: Tracks all emergency requests and responses
- **Emergency Contacts**: Manage and notify emergency contacts
- **User Authentication**: Firebase-based secure authentication
- **Guest Access**: Support for emergency use without authentication

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: Firebase Firestore
- **Authentication**: Firebase Authentication
- **APIs**: REST API with JSON

## Installation

### Prerequisites
- Python 3.8+
- Firebase project
- Git

### Setup

1. Clone the repository
```bash
git clone https://github.com/G0urAV0001/LifeLine-AI.git
cd LifeLine-AI
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your Firebase credentials
```

5. Run the application
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/guest` - Guest session
- `POST /api/auth/logout` - Logout
- `POST /api/auth/verify-token` - Verify token
- `POST /api/auth/reset-password` - Reset password

### User Profile
- `GET /api/users/profile` - Get profile
- `PUT /api/users/profile` - Update profile

### AI Analysis
- `POST /api/ai/text` - Analyze text
- `POST /api/ai/image` - Analyze image
- `POST /api/ai/voice` - Analyze voice

### Emergency Services
- `POST /api/emergency/sos` - Trigger SOS
- `GET /api/emergency/hospitals?latitude=X&longitude=Y` - Find hospitals

### Emergency Contacts
- `GET /api/users/contacts` - List contacts
- `POST /api/users/contacts` - Add contact
- `PUT /api/users/contacts/<id>` - Update contact
- `DELETE /api/users/contacts/<id>` - Delete contact

### History
- `GET /api/users/history` - Get emergency history

## Project Structure

```
LifeLine-AI/
├── routes/
│   ├── auth.py
│   ├── profile.py
│   ├── ai.py
│   ├── hospitals.py
│   ├── sos.py
│   ├── contacts.py
│   └── history.py
├── services/
│   ├── ai_service.py
│   ├── hospital_service.py
│   └── sos_service.py
├── utils/
│   ├── validators.py
│   ├── decorators.py
│   ├── auth_utils.py
│   └── firebase_utils.py
├── config.py
├── app.py
├── requirements.txt
└── README.md
```

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
```bash
black .
flake8 .
```

## Deployment

### Heroku
```bash
heroku create your-app-name
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key
# Set other environment variables
git push heroku main
```

### Docker
```bash
docker build -t lifeline-ai .
docker run -p 5000:5000 lifeline-ai
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@lifelineai.com or open an issue on GitHub.

## Acknowledgments

- Firebase for backend infrastructure
- Flask community for the amazing framework
- All contributors and users
