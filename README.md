# Dating App API

A modern dating application API built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

- User authentication and authorization
- User profiles with customizable information
- Matching system based on gender preferences
- Like/Unlike functionality
- Real-time messaging between matched users
- Profile customization (bio, interests, location, profile picture)

## Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd dating-app
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following content:
```
DATABASE_URL=postgresql://user:password@localhost/dating_app
SECRET_KEY=your-secret-key-here
```

5. Initialize the database:
```bash
alembic upgrade head
```

## Running the Application

1. Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

2. Access the API documentation at:
```
http://localhost:8000/docs
```

## API Endpoints

### Authentication
- POST `/users/` - Create a new user
- POST `/token` - Login and get access token
- GET `/users/me` - Get current user profile

### Profile
- PUT `/users/profile` - Update user profile

### Matching
- GET `/matches` - Get potential matches
- POST `/users/like/{username}` - Like a user

### Messaging
- GET `/messages` - Get all messages
- POST `/messages/{username}` - Send a message to a user

## Testing

Run the tests using pytest:
```bash
pytest
```

## Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- HTTPS recommended for production
- Rate limiting recommended for production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 