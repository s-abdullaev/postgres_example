"""Tests for takes CRUD endpoints."""

def test_list_takes(client):
    r = client.get("/api/takes")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "id" in data[0] and "course_id" in data[0] and "grade" in data[0]


def test_get_takes(client):
    r = client.get("/api/takes/00128/CS-101/1/Fall/2017")
    assert r.status_code == 200
    assert r.json()["id"] == "00128"
    assert r.json()["course_id"] == "CS-101"
    assert r.json()["grade"] == "A"


def test_get_takes_not_found(client):
    r = client.get("/api/takes/99999/XX-999/1/Fall/2017")
    assert r.status_code == 404


def test_create_takes(client):
    # Need student and section - create new section and use existing student 70557 (Snow) who has 0 credits
    client.post(
        "/api/sections",
        json={
            "course_id": "MU-199",
            "sec_id": "2",
            "semester": "Spring",
            "year": 2025,
            "building": "Packard",
            "room_number": "101",
            "time_slot_id": "D",
        },
    )
    r = client.post(
        "/api/takes",
        json={
            "id": "70557",
            "course_id": "MU-199",
            "sec_id": "2",
            "semester": "Spring",
            "year": 2025,
            "grade": "B",
        },
    )
    assert r.status_code == 201
    assert r.json()["id"] == "70557"
    assert r.json()["course_id"] == "MU-199"
    assert r.json()["grade"] == "B"


def test_update_takes(client):
    client.post(
        "/api/sections",
        json={
            "course_id": "MU-199",
            "sec_id": "3",
            "semester": "Spring",
            "year": 2026,
            "building": "Packard",
            "room_number": "101",
            "time_slot_id": "D",
        },
    )
    client.post(
        "/api/takes",
        json={
            "id": "70557",
            "course_id": "MU-199",
            "sec_id": "3",
            "semester": "Spring",
            "year": 2026,
            "grade": "C",
        },
    )
    r = client.patch("/api/takes/70557/MU-199/3/Spring/2026", json={"grade": "A"})
    assert r.status_code == 200
    assert r.json()["grade"] == "A"


def test_update_takes_not_found(client):
    r = client.patch("/api/takes/99999/XX-999/1/Fall/2017", json={"grade": "A"})
    assert r.status_code == 404


def test_delete_takes(client):
    client.post(
        "/api/sections",
        json={
            "course_id": "MU-199",
            "sec_id": "4",
            "semester": "Spring",
            "year": 2027,
            "building": "Packard",
            "room_number": "101",
            "time_slot_id": "D",
        },
    )
    client.post(
        "/api/takes",
        json={
            "id": "70557",
            "course_id": "MU-199",
            "sec_id": "4",
            "semester": "Spring",
            "year": 2027,
            "grade": "B",
        },
    )
    r = client.delete("/api/takes/70557/MU-199/4/Spring/2027")
    assert r.status_code == 204
    r2 = client.get("/api/takes/70557/MU-199/4/Spring/2027")
    assert r2.status_code == 404


def test_delete_takes_not_found(client):
    r = client.delete("/api/takes/99999/XX-999/1/Fall/2017")
    assert r.status_code == 404
