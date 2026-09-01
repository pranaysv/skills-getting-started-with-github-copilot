from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_and_unregister_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "student@example.com"

    # Act: sign up
    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert: signup succeeds
    assert signup_response.status_code == 200

    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity_name]["participants"]

    # Act: unregister
    delete_response = client.delete(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert: removal succeeds
    assert delete_response.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_unregister_missing_participant_returns_404():
    # Arrange
    activity_name = "Programming Class"
    email = "missing@example.com"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert
    assert response.status_code == 404
