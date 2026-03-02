"""Tests for student CRUD endpoints."""

def test_list_students(client):
    r = client.get("/api/students")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "id" in data[0] and "name" in data[0] and "tot_cred" in data[0]


def test_get_student(client):
    r = client.get("/api/students/12345")
    assert r.status_code == 200
    assert r.json()["id"] == "12345"
    assert r.json()["name"] == "Shankar"
    assert r.json()["tot_cred"] == 32


def test_get_student_not_found(client):
    r = client.get("/api/students/99999")
    assert r.status_code == 404


def test_create_student(client):
    r = client.post(
        "/api/students",
        json={
            "id": "99999",
            "name": "Test Student",
            "dept_name": "Comp. Sci.",
            "tot_cred": 0,
        },
    )
    assert r.status_code == 201
    assert r.json()["id"] == "99999"
    assert r.json()["name"] == "Test Student"


def test_update_student(client):
    client.post(
        "/api/students",
        json={
            "id": "99998",
            "name": "Original",
            "dept_name": "Comp. Sci.",
            "tot_cred": 0,
        },
    )
    r = client.patch("/api/students/99998", json={"tot_cred": 50})
    assert r.status_code == 200
    assert r.json()["tot_cred"] == 50


def test_update_student_not_found(client):
    r = client.patch("/api/students/99999", json={"name": "X"})
    assert r.status_code == 404


def test_delete_student(client):
    client.post(
        "/api/students",
        json={
            "id": "99997",
            "name": "Delete Me",
            "dept_name": "Comp. Sci.",
            "tot_cred": 0,
        },
    )
    r = client.delete("/api/students/99997")
    assert r.status_code == 204
    r2 = client.get("/api/students/99997")
    assert r2.status_code == 404


def test_delete_student_not_found(client):
    r = client.delete("/api/students/99999")
    assert r.status_code == 404
