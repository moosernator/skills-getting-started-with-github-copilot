"""
Tests for POST /activities/{activity_name}/signup endpoint.
Uses the AAA (Arrange-Act-Assert) testing pattern.
"""

import pytest


def test_signup_new_participant_success(client, sample_activity_name, sample_email):
    """
    Test successfully signing up a new participant.
    
    AAA Pattern:
    - Arrange: Set up test data (activity name and email)
    - Act: Make POST request to signup endpoint
    - Assert: Verify successful response and participant added
    """
    # Arrange
    test_email = "newuser@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{sample_activity_name}/signup",
        params={"email": test_email}
    )
    
    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    assert test_email in response.json()["message"]


def test_signup_duplicate_participant_rejected(client, sample_activity_name):
    """
    Test that duplicate signup is rejected.
    
    AAA Pattern:
    - Arrange: First signup succeeds, prepare duplicate signup
    - Act: Attempt to signup same participant again
    - Assert: Verify rejection with 400 status
    """
    # Arrange
    test_email = "duplicate@mergington.edu"
    client.post(
        f"/activities/{sample_activity_name}/signup",
        params={"email": test_email}
    )
    
    # Act
    response = client.post(
        f"/activities/{sample_activity_name}/signup",
        params={"email": test_email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_nonexistent_activity_returns_404(client, sample_email, nonexistent_activity):
    """
    Test that signing up for non-existent activity returns 404.
    
    AAA Pattern:
    - Arrange: Prepare non-existent activity name and email
    - Act: Attempt to signup for non-existent activity
    - Assert: Verify 404 Not Found response
    """
    # Arrange
    # (implicit in fixtures)
    
    # Act
    response = client.post(
        f"/activities/{nonexistent_activity}/signup",
        params={"email": sample_email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_signup_multiple_participants_different_activities(client):
    """
    Test signing up the same participant to different activities.
    
    AAA Pattern:
    - Arrange: Define test email and multiple activities
    - Act: Sign up participant to multiple activities
    - Assert: Verify all signups succeed
    """
    # Arrange
    test_email = "multi@mergington.edu"
    activities = ["Chess Club", "Programming Class", "Gym Class"]
    
    # Act
    responses = []
    for activity in activities:
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": test_email}
        )
        responses.append(response)
    
    # Assert
    for response in responses:
        assert response.status_code == 200


def test_signup_at_capacity_allowed(client):
    """
    Test that signup is allowed even when activity approaches capacity.
    
    AAA Pattern:
    - Arrange: Get current participant count for an activity
    - Act: Attempt signup
    - Assert: Verify signup succeeds (no hard capacity check in current implementation)
    """
    # Arrange
    activities_response = client.get("/activities")
    activity = "Chess Club"  # Small max_participants
    current_participants = len(activities_response.json()[activity]["participants"])
    max_participants = activities_response.json()[activity]["max_participants"]
    
    test_email = "capacity@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": test_email}
    )
    
    # Assert - Signup succeeds regardless of capacity
    # (Current implementation doesn't enforce capacity limit)
    assert response.status_code == 200
