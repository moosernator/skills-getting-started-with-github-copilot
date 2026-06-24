"""
Tests for GET /activities endpoint.
Uses the AAA (Arrange-Act-Assert) testing pattern.
"""

import pytest


def test_get_activities_returns_all_activities(client):
    """
    Test that GET /activities returns all activities.
    
    AAA Pattern:
    - Arrange: Client is ready (fixture)
    - Act: Make GET request to /activities
    - Assert: Verify response contains expected activities
    """
    # Arrange
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Soccer Team",
        "Basketball Club",
        "Art Club",
        "Drama Club",
        "Debate Team",
        "Science Club"
    ]
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    for activity in expected_activities:
        assert activity in data


def test_activity_has_required_fields(client):
    """
    Test that each activity has all required fields.
    
    AAA Pattern:
    - Arrange: Define required fields
    - Act: Fetch activities
    - Assert: Verify each activity has all fields
    """
    # Arrange
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        for field in required_fields:
            assert field in activity_data, f"Activity '{activity_name}' missing field '{field}'"


def test_participants_is_list(client):
    """
    Test that participants field is a list.
    
    AAA Pattern:
    - Arrange: Client ready (fixture)
    - Act: Fetch activities
    - Assert: Verify participants is a list for each activity
    """
    # Arrange
    # (implicit in fixture)
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data["participants"], list), \
            f"Activity '{activity_name}' participants should be a list"


def test_max_participants_is_integer(client):
    """
    Test that max_participants is an integer.
    
    AAA Pattern:
    - Arrange: Client ready (fixture)
    - Act: Fetch activities
    - Assert: Verify max_participants is int for each activity
    """
    # Arrange
    # (implicit in fixture)
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data["max_participants"], int), \
            f"Activity '{activity_name}' max_participants should be an integer"
