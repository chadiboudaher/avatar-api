import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db

TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, 
                       connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False,
                                   autoflush=False,
                                   bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)
client = TestClient(app)

def test_get_characters_empty():
    response = client.get("/characters")
    assert response.status_code == 401


def test_register_login_and_access_protected_route():
    # Register
    register_response = client.post("/register", json={
        "username": "testuser",
        "password": "testpass123"
    })

    assert register_response.status_code == 201

    # Login
    login_response = client.post("/login", data={
        "username": "testuser",
        "password": "testpass123"
    })

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Access protected route
    response = client.get("/characters", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200