"""
Tests for DELETE /activities/{activity_name}/unregister endpoint.
Uses the AAA (Arrange-Act-Assert) testing pattern.
"""

import pytest


def test_unregister_participant_success(client, sample_activity_name):
    """
    Test successfully unregistering a participant.
    
    AAA Pattern:
    - Arrange: Sign up a participant first
    - Act: Delete their registration
    - Assert: Verify successful removal and response
    """
    # Arrange
    test_email = "remove@mergington.edu"
    client.post(
        f"/activities/{sample_activity_name}/signup",
        params={"email": test_email}
    )
    
    # Act
    response = client.delete(
        f"/activities/{sample_activity_name}/unregister",
        params={"email": test_email}
    )
    
    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    assert test_email in response.json()["message"]


def test_unregister_nonregistered_participant_rejected(client, sample_activity_name, nonexistent_email):
    """
    Test that unregistering a non-registered participant fails.
    
    AAA Pattern:
    - Arrange: Prepare non-registered email
    - Act: Attempt to unregister non-registered participant
    - Assert: Verify 400 error
    """
    # Arrange
    # (implicit in fixtures)
    
    # Act
    response = client.delete(
        f"/activities/{sample_activity_name}/unregister",
        params={"email": nonexistent_email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"].lower()


def test_unregister_nonexistent_activity_returns_404(client, sample_email, nonexistent_activity):
    """
    Test that unregistering from non-existent activity returns 404.
    
    AAA Pattern:
    - Arrange: Prepare non-existent activity name
    - Act: Attempt to unregister from non-existent activity
    - Assert: Verify 404 Not Found response
    """
    # Arrange
    # (implicit in fixtures)
    
    # Act
    response = client.delete(
        f"/activities/{nonexistent_activity}/unregister",
        params={"email": sample_email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_unregister_frees_spot(client, sample_activity_name):
    """
    Test that unregistering frees up a spot for re-registration.
    
    AAA Pattern:
    - Arrange: Sign up, then unregister a participant
    - Act: Sign up the same participant again
    - Assert: Verify re-signup succeeds (spot is free)
    """
    # Arrange
    test_email = "respotted@mergington.edu"
    client.post(
        f"/activities/{sample_activity_name}/signup",
        params={"email": test_email}
    )
    client.delete(
        f"/activities/{sample_activity_name}/unregister",
        params={"email": test_email}
    )
    
    # Act
    response = client.post(
        f"/activities/{sample_activity_name}/signup",
        params={"email": test_email}
    )
    
    # Assert
    assert response.status_code == 200
