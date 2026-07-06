from src import app as app_module


def test_signup_prevents_duplicate_registration(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    first_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    second_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert app_module.activities[activity_name]["participants"].count(email) == 1


def test_unregister_participant_removes_them(client):
    # Arrange
    activity_name = "Chess Club"
    email = "remove-me@mergington.edu"

    # Act
    client.post(f"/activities/{activity_name}/signup", params={"email": email})
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert email not in app_module.activities[activity_name]["participants"]


def test_list_activities_returns_all_available_activities(client):
    # Arrange
    expected_activity_count = len(app_module.activities)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert len(response.json()) == expected_activity_count
