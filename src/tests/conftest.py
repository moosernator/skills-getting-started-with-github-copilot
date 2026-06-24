"""
Pytest configuration and shared fixtures for API tests.
Uses the AAA (Arrange-Act-Assert) pattern.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Fixture: Provides a TestClient for making requests to the API.
    
    Returns:
        TestClient: FastAPI test client
    """
    return TestClient(app)


@pytest.fixture
def sample_email():
    """Fixture: Provides a sample test email."""
    return "test@mergington.edu"


@pytest.fixture
def sample_activity_name():
    """Fixture: Provides a sample activity name."""
    return "Chess Club"


@pytest.fixture
def nonexistent_activity():
    """Fixture: Provides a non-existent activity name."""
    return "Nonexistent Activity"


@pytest.fixture
def nonexistent_email():
    """Fixture: Provides an email not in any activity."""
    return "nonexistent@mergington.edu"
