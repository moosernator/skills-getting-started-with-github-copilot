"""
Tests for GET / root endpoint.
Uses the AAA (Arrange-Act-Assert) testing pattern.
"""

import pytest


def test_root_redirects_to_static_index(client):
    """
    Test that GET / redirects to /static/index.html.
    
    AAA Pattern:
    - Arrange: Client ready (fixture)
    - Act: Make GET request to root
    - Assert: Verify redirect response
    """
    # Arrange
    # (implicit in fixture)
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert "/static/index.html" in response.headers["location"]


def test_root_redirect_with_follow(client):
    """
    Test that following the redirect from / reaches index.html.
    
    AAA Pattern:
    - Arrange: Client ready (fixture)
    - Act: Make GET request to root with redirect following
    - Assert: Verify successful redirect to static content
    """
    # Arrange
    # (implicit in fixture)
    
    # Act
    response = client.get("/", follow_redirects=True)
    
    # Assert
    assert response.status_code == 200
