import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(original)


@pytest.fixture()
def client():
    return TestClient(app_module.app)


def test_signup_prevents_duplicate_registration(client):
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    first_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    second_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert app_module.activities[activity_name]["participants"].count(email) == 1


def test_unregister_participant_removes_them(client):
    activity_name = "Chess Club"
    email = "remove-me@mergington.edu"

    client.post(f"/activities/{activity_name}/signup", params={"email": email})
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email not in app_module.activities[activity_name]["participants"]
