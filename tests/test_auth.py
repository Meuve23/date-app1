import pytest
from fastapi.testclient import TestClient
from datetime import datetime

from app.main import app
from app.models.user import User
from app.schemas.user import UserCreate

def test_create_user(client):
    response = client.post(
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
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "password" not in data

def test_login_user(client):
    # First create a user
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
    
    # Then try to login
    response = client.post(
        "/token",
        data={
            "username": "test@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_get_current_user(client):
    # First create a user and get token
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
    
    # Try to get current user
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser" 