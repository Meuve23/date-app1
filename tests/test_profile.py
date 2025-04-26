import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models.user import User

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture
def auth_headers(client):
    # Create a user and get token
    client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "password": "testpassword123",
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "date_of_birth": "1990-01-01",
            "gender": "male",
            "looking_for": "female"
        }
    )
    
    login_response = client.post(
        "/token",
        data={
            "username": "test@example.com",
            "password": "testpassword123"
        }
    )
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_update_profile(client, auth_headers):
    response = client.put(
        "/users/profile",
        headers=auth_headers,
        json={
            "bio": "Test bio",
            "interests": ["reading", "travel"],
            "location": "New York",
            "profile_picture": "https://example.com/picture.jpg"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["bio"] == "Test bio"
    assert data["interests"] == ["reading", "travel"]
    assert data["location"] == "New York"
    assert data["profile_picture"] == "https://example.com/picture.jpg"

def test_get_matches(client, auth_headers):
    # Create another user for matching
    client.post(
        "/users/",
        json={
            "email": "match@example.com",
            "password": "testpassword123",
            "username": "matchuser",
            "first_name": "Match",
            "last_name": "User",
            "date_of_birth": "1992-01-01",
            "gender": "female",
            "looking_for": "male"
        }
    )
    
    response = client.get("/matches", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(user["username"] == "matchuser" for user in data)

def test_like_user(client, auth_headers):
    # Create another user to like
    client.post(
        "/users/",
        json={
            "email": "like@example.com",
            "password": "testpassword123",
            "username": "likeuser",
            "first_name": "Like",
            "last_name": "User",
            "date_of_birth": "1992-01-01",
            "gender": "female",
            "looking_for": "male"
        }
    )
    
    response = client.post(
        "/users/like/likeuser",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "match" in data
    assert isinstance(data["match"], bool)

def test_get_messages(client, auth_headers):
    response = client.get("/messages", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_send_message(client, auth_headers):
    # Create another user to message
    client.post(
        "/users/",
        json={
            "email": "message@example.com",
            "password": "testpassword123",
            "username": "messageuser",
            "first_name": "Message",
            "last_name": "User",
            "date_of_birth": "1992-01-01",
            "gender": "female",
            "looking_for": "male"
        }
    )
    
    # First create a like to enable messaging
    client.post(
        "/users/like/messageuser",
        headers=auth_headers
    )
    
    # Create a like back to establish a match
    message_login = client.post(
        "/token",
        data={
            "username": "message@example.com",
            "password": "testpassword123"
        }
    )
    message_token = message_login.json()["access_token"]
    client.post(
        "/users/like/testuser",
        headers={"Authorization": f"Bearer {message_token}"}
    )
    
    # Now try to send a message
    response = client.post(
        "/messages/messageuser",
        headers=auth_headers,
        json={"content": "Hello!"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["content"] == "Hello!" 