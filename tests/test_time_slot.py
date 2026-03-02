"""Tests for time_slot CRUD endpoints."""

def test_list_time_slots(client):
    r = client.get("/api/time-slots")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "time_slot_id" in data[0] and "day" in data[0] and "start_hr" in data[0]


def test_get_time_slot(client):
    r = client.get("/api/time-slots/A/M/8/0")
    assert r.status_code == 200
    assert r.json()["time_slot_id"] == "A"
    assert r.json()["day"] == "M"
    assert r.json()["start_hr"] == 8
    assert r.json()["start_min"] == 0


def test_get_time_slot_not_found(client):
    r = client.get("/api/time-slots/Z/X/0/0")
    assert r.status_code == 404


def test_create_time_slot(client):
    r = client.post(
        "/api/time-slots",
        json={
            "time_slot_id": "Z",
            "day": "M",
            "start_hr": 7,
            "start_min": 0,
            "end_hr": 7,
            "end_min": 50,
        },
    )
    assert r.status_code == 201
    assert r.json()["time_slot_id"] == "Z"
    assert r.json()["start_hr"] == 7


def test_update_time_slot(client):
    client.post(
        "/api/time-slots",
        json={
            "time_slot_id": "Z",
            "day": "T",
            "start_hr": 7,
            "start_min": 30,
            "end_hr": 8,
            "end_min": 20,
        },
    )
    r = client.patch("/api/time-slots/Z/T/7/30", json={"end_hr": 9, "end_min": 15})
    assert r.status_code == 200
    assert r.json()["end_hr"] == 9
    assert r.json()["end_min"] == 15


def test_update_time_slot_not_found(client):
    r = client.patch("/api/time-slots/Z/X/0/0", json={"end_hr": 10})
    assert r.status_code == 404


def test_delete_time_slot(client):
    client.post(
        "/api/time-slots",
        json={
            "time_slot_id": "Z",
            "day": "W",
            "start_hr": 6,
            "start_min": 0,
            "end_hr": 6,
            "end_min": 50,
        },
    )
    r = client.delete("/api/time-slots/Z/W/6/0")
    assert r.status_code == 204
    r2 = client.get("/api/time-slots/Z/W/6/0")
    assert r2.status_code == 404


def test_delete_time_slot_not_found(client):
    r = client.delete("/api/time-slots/Z/X/0/0")
    assert r.status_code == 404
