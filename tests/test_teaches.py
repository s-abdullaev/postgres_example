"""Tests for teaches CRUD endpoints."""

def test_list_teaches(client):
    r = client.get("/api/teaches")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "id" in data[0] and "course_id" in data[0] and "sec_id" in data[0]


def test_get_teaches(client):
    r = client.get("/api/teaches/10101/CS-101/1/Fall/2017")
    assert r.status_code == 200
    assert r.json()["id"] == "10101"
    assert r.json()["course_id"] == "CS-101"
    assert r.json()["sec_id"] == "1"
    assert r.json()["semester"] == "Fall"
    assert r.json()["year"] == 2017


def test_get_teaches_not_found(client):
    r = client.get("/api/teaches/99999/XX-999/1/Fall/2017")
    assert r.status_code == 404


def test_create_teaches(client):
    # Need a section first - use existing CS-101/1/Fall/2017 and an instructor not yet teaching it
    # 98345 teaches EE-181, not CS-101. Let's use 98345 for a new section we create
    client.post(
        "/api/sections",
        json={
            "course_id": "EE-181",
            "sec_id": "2",
            "semester": "Fall",
            "year": 2025,
            "building": "Taylor",
            "room_number": "3128",
            "time_slot_id": "C",
        },
    )
    r = client.post(
        "/api/teaches",
        json={
            "id": "98345",
            "course_id": "EE-181",
            "sec_id": "2",
            "semester": "Fall",
            "year": 2025,
        },
    )
    assert r.status_code == 201
    assert r.json()["id"] == "98345"
    assert r.json()["course_id"] == "EE-181"
    assert r.json()["sec_id"] == "2"


def test_delete_teaches(client):
    client.post(
        "/api/sections",
        json={
            "course_id": "EE-181",
            "sec_id": "3",
            "semester": "Fall",
            "year": 2026,
            "building": "Taylor",
            "room_number": "3128",
            "time_slot_id": "C",
        },
    )
    client.post(
        "/api/teaches",
        json={
            "id": "98345",
            "course_id": "EE-181",
            "sec_id": "3",
            "semester": "Fall",
            "year": 2026,
        },
    )
    r = client.delete("/api/teaches/98345/EE-181/3/Fall/2026")
    assert r.status_code == 204
    r2 = client.get("/api/teaches/98345/EE-181/3/Fall/2026")
    assert r2.status_code == 404


def test_delete_teaches_not_found(client):
    r = client.delete("/api/teaches/99999/XX-999/1/Fall/2017")
    assert r.status_code == 404
