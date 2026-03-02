"""Tests for department CRUD endpoints."""

def test_list_departments(client):
    r = client.get("/api/departments")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "dept_name" in data[0] and "budget" in data[0]


def test_get_department(client):
    r = client.get("/api/departments/Biology")
    assert r.status_code == 200
    assert r.json()["dept_name"] == "Biology"
    assert float(r.json()["budget"]) == 90000


def test_get_department_not_found(client):
    r = client.get("/api/departments/NonexistentDept")
    assert r.status_code == 404


def test_create_department(client):
    r = client.post(
        "/api/departments",
        json={"dept_name": "TestDept", "building": "Taylor", "budget": 50000},
    )
    assert r.status_code == 201
    assert r.json()["dept_name"] == "TestDept"
    assert float(r.json()["budget"]) == 50000


def test_update_department(client):
    client.post(
        "/api/departments",
        json={"dept_name": "TestDept2", "building": "Taylor", "budget": 60000},
    )
    r = client.patch("/api/departments/TestDept2", json={"budget": 75000})
    assert r.status_code == 200
    assert float(r.json()["budget"]) == 75000


def test_update_department_not_found(client):
    r = client.patch("/api/departments/X", json={"budget": 100})
    assert r.status_code == 404


def test_delete_department(client):
    client.post(
        "/api/departments",
        json={"dept_name": "DelDept", "building": "Taylor", "budget": 10000},
    )
    r = client.delete("/api/departments/DelDept")
    assert r.status_code == 204
    r2 = client.get("/api/departments/DelDept")
    assert r2.status_code == 404


def test_delete_department_not_found(client):
    r = client.delete("/api/departments/X")
    assert r.status_code == 404
