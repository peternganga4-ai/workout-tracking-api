def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_create_and_list_exercises(client):
    res = client.post(
        "/exercises",
        json={"name": "Squat", "category": "Strength"},
    )
    assert res.status_code == 201
    assert res.get_json()["name"] == "Squat"

    res = client.get("/exercises")
    assert res.status_code == 200
    assert len(res.get_json()) == 1


def test_get_missing_exercise_returns_404(client):
    res = client.get("/exercises/9999")
    assert res.status_code == 404


def test_delete_exercise_returns_204(client):
    created = client.post(
        "/exercises", json={"name": "Plank", "category": "Core"}
    ).get_json()
    res = client.delete(f"/exercises/{created['id']}")
    assert res.status_code == 204
    assert client.get(f"/exercises/{created['id']}").status_code == 404


def test_create_workout(client):
    res = client.post(
        "/workouts",
        json={"date": "2026-01-15", "duration_minutes": 45, "notes": "leg day"},
    )
    assert res.status_code == 201
    assert res.get_json()["duration_minutes"] == 45


def test_invalid_workout_returns_400(client):
    res = client.post("/workouts", json={"duration_minutes": -5})
    assert res.status_code == 400
    assert "errors" in res.get_json()


def test_add_exercise_to_workout(client):
    workout = client.post(
        "/workouts",
        json={"date": "2026-01-15", "duration_minutes": 30},
    ).get_json()
    exercise = client.post(
        "/exercises", json={"name": "Lunge", "category": "Strength"}
    ).get_json()

    url = f"/workouts/{workout['id']}/exercises/{exercise['id']}/workout_exercises"
    res = client.post(url, json={"reps": 12, "sets": 3})
    assert res.status_code == 201
    assert res.get_json()["exercise"]["name"] == "Lunge"


def test_duplicate_association_returns_409(client):
    workout = client.post(
        "/workouts", json={"date": "2026-01-15", "duration_minutes": 30}
    ).get_json()
    exercise = client.post(
        "/exercises", json={"name": "Lunge", "category": "Strength"}
    ).get_json()

    url = f"/workouts/{workout['id']}/exercises/{exercise['id']}/workout_exercises"
    assert client.post(url, json={"reps": 12}).status_code == 201
    assert client.post(url, json={"reps": 12}).status_code == 409


def test_add_to_missing_workout_returns_404(client):
    exercise = client.post(
        "/exercises", json={"name": "Lunge", "category": "Strength"}
    ).get_json()
    url = f"/workouts/9999/exercises/{exercise['id']}/workout_exercises"
    assert client.post(url, json={}).status_code == 404
    