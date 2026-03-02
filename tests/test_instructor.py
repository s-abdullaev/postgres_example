"""Tests for instructor CRUD endpoints."""

def test_list_instructors(client):
    r = client.get("/api/instructors")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "id" in data[0] and "name" in data[0] and "salary" in data[0]


def test_get_instructor(client):
    r = client.get("/api/instructors/10101")
    assert r.status_code == 200
    assert r.json()["id"] == "10101"
    assert r.json()["name"] == "Srinivasan"
    assert float(r.json()["salary"]) == 65000


def test_get_instructor_not_found(client):
    r = client.get("/api/instructors/99999")
    assert r.status_code == 404


def test_create_instructor(client):
    r = client.post(
        "/api/instructors",
        json={
            "id": "99999",
            "name": "Test Prof",
            "dept_name": "Comp. Sci.",
            "salary": 50000,
        },
    )
    assert r.status_code == 201
    assert r.json()["id"] == "99999"
    assert r.json()["name"] == "Test Prof"


def test_update_instructor(client):
    client.post(
        "/api/instructors",
        json={
            "id": "99998",
            "name": "Original",
            "dept_name": "Comp. Sci.",
            "salary": 50000,
        },
    )
    r = client.patch("/api/instructors/99998", json={"name": "Updated Name"})
    assert r.status_code == 200
    assert r.json()["name"] == "Updated Name"


def test_update_instructor_not_found(client):
    r = client.patch("/api/instructors/99999", json={"name": "X"})
    assert r.status_code == 404


def test_delete_instructor(client):
    client.post(
        "/api/instructors",
        json={
            "id": "99997",
            "name": "Delete Me",
            "dept_name": "Comp. Sci.",
            "salary": 50000,
        },
    )
    r = client.delete("/api/instructors/99997")
    assert r.status_code == 204
    r2 = client.get("/api/instructors/99997")
    assert r2.status_code == 404


def test_delete_instructor_not_found(client):
    r = client.delete("/api/instructors/99999")
    assert r.status_code == 404
