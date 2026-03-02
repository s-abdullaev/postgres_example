"""Tests for prereq CRUD endpoints."""

def test_list_prereqs(client):
    r = client.get("/api/prereqs")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "course_id" in data[0] and "prereq_id" in data[0]


def test_get_prereq(client):
    r = client.get("/api/prereqs/CS-315/CS-101")
    assert r.status_code == 200
    assert r.json()["course_id"] == "CS-315"
    assert r.json()["prereq_id"] == "CS-101"


def test_get_prereq_not_found(client):
    r = client.get("/api/prereqs/XX-999/YY-001")
    assert r.status_code == 404


def test_create_prereq(client):
    # Both courses must exist - CS-101 and BIO-101 exist
    r = client.post(
        "/api/prereqs",
        json={"course_id": "CS-319", "prereq_id": "CS-190"},
    )
    assert r.status_code == 201
    assert r.json()["course_id"] == "CS-319"
    assert r.json()["prereq_id"] == "CS-190"


def test_delete_prereq(client):
    # Create then delete
    client.post(
        "/api/prereqs",
        json={"course_id": "CS-190", "prereq_id": "CS-315"},
    )
    r = client.delete("/api/prereqs/CS-190/CS-315")
    assert r.status_code == 204
    r2 = client.get("/api/prereqs/CS-190/CS-315")
    assert r2.status_code == 404


def test_delete_prereq_not_found(client):
    r = client.delete("/api/prereqs/XX-999/YY-001")
    assert r.status_code == 404
