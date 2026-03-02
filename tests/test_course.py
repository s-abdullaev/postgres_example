"""Tests for course CRUD endpoints."""

def test_list_courses(client):
    r = client.get("/api/courses")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "course_id" in data[0] and "title" in data[0] and "credits" in data[0]


def test_get_course(client):
    r = client.get("/api/courses/CS-101")
    assert r.status_code == 200
    assert r.json()["course_id"] == "CS-101"
    assert r.json()["title"] == "Intro. to Computer Science"
    assert r.json()["credits"] == 4


def test_get_course_not_found(client):
    r = client.get("/api/courses/XX-999")
    assert r.status_code == 404


def test_create_course(client):
    r = client.post(
        "/api/courses",
        json={
            "course_id": "TEST-01",
            "title": "Test Course",
            "dept_name": "Comp. Sci.",
            "credits": 3,
        },
    )
    assert r.status_code == 201
    assert r.json()["course_id"] == "TEST-01"
    assert r.json()["credits"] == 3


def test_update_course(client):
    client.post(
        "/api/courses",
        json={
            "course_id": "TEST-02",
            "title": "Test",
            "dept_name": "Comp. Sci.",
            "credits": 2,
        },
    )
    r = client.patch("/api/courses/TEST-02", json={"credits": 4})
    assert r.status_code == 200
    assert r.json()["credits"] == 4


def test_update_course_not_found(client):
    r = client.patch("/api/courses/XX-999", json={"credits": 1})
    assert r.status_code == 404


def test_delete_course(client):
    client.post(
        "/api/courses",
        json={
            "course_id": "DEL-01",
            "title": "Delete Me",
            "dept_name": "Comp. Sci.",
            "credits": 1,
        },
    )
    r = client.delete("/api/courses/DEL-01")
    assert r.status_code == 204
    r2 = client.get("/api/courses/DEL-01")
    assert r2.status_code == 404


def test_delete_course_not_found(client):
    r = client.delete("/api/courses/XX-999")
    assert r.status_code == 404
