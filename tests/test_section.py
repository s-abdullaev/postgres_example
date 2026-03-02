"""Tests for section CRUD endpoints."""

def test_list_sections(client):
    r = client.get("/api/sections")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "course_id" in data[0] and "sec_id" in data[0] and "semester" in data[0] and "year" in data[0]


def test_get_section(client):
    r = client.get("/api/sections/CS-101/1/Fall/2017")
    assert r.status_code == 200
    assert r.json()["course_id"] == "CS-101"
    assert r.json()["sec_id"] == "1"
    assert r.json()["semester"] == "Fall"
    assert r.json()["year"] == 2017


def test_get_section_not_found(client):
    r = client.get("/api/sections/XX-999/1/Fall/2017")
    assert r.status_code == 404


def test_create_section(client):
    r = client.post(
        "/api/sections",
        json={
            "course_id": "CS-101",
            "sec_id": "99",
            "semester": "Fall",
            "year": 2025,
            "building": "Packard",
            "room_number": "101",
            "time_slot_id": "A",
        },
    )
    assert r.status_code == 201
    assert r.json()["course_id"] == "CS-101"
    assert r.json()["sec_id"] == "99"
    assert r.json()["year"] == 2025


def test_update_section(client):
    client.post(
        "/api/sections",
        json={
            "course_id": "CS-101",
            "sec_id": "98",
            "semester": "Fall",
            "year": 2026,
            "building": "Packard",
            "room_number": "101",
            "time_slot_id": "A",
        },
    )
    r = client.patch("/api/sections/CS-101/98/Fall/2026", json={"time_slot_id": "B"})
    assert r.status_code == 200
    assert r.json()["time_slot_id"] == "B"


def test_update_section_not_found(client):
    r = client.patch("/api/sections/XX-999/1/Fall/2017", json={"time_slot_id": "A"})
    assert r.status_code == 404


def test_delete_section(client):
    client.post(
        "/api/sections",
        json={
            "course_id": "CS-101",
            "sec_id": "97",
            "semester": "Fall",
            "year": 2027,
            "building": "Packard",
            "room_number": "101",
            "time_slot_id": "A",
        },
    )
    r = client.delete("/api/sections/CS-101/97/Fall/2027")
    assert r.status_code == 204
    r2 = client.get("/api/sections/CS-101/97/Fall/2027")
    assert r2.status_code == 404


def test_delete_section_not_found(client):
    r = client.delete("/api/sections/XX-999/1/Fall/2017")
    assert r.status_code == 404
