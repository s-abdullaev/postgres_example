"""Tests for advisor CRUD endpoints."""

def test_list_advisors(client):
    r = client.get("/api/advisors")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "s_id" in data[0] and "i_id" in data[0]


def test_get_advisor(client):
    r = client.get("/api/advisors/00128")
    assert r.status_code == 200
    assert r.json()["s_id"] == "00128"
    assert r.json()["i_id"] == "45565"


def test_get_advisor_not_found(client):
    r = client.get("/api/advisors/99999")
    assert r.status_code == 404


def test_create_advisor(client):
    # Need a student first - create one
    client.post(
        "/api/students",
        json={
            "id": "99990",
            "name": "Advisee",
            "dept_name": "Comp. Sci.",
            "tot_cred": 0,
        },
    )
    r = client.post(
        "/api/advisors",
        json={"s_id": "99990", "i_id": "10101"},
    )
    assert r.status_code == 201
    assert r.json()["s_id"] == "99990"
    assert r.json()["i_id"] == "10101"


def test_update_advisor(client):
    client.post(
        "/api/students",
        json={
            "id": "99991",
            "name": "Advisee2",
            "dept_name": "Comp. Sci.",
            "tot_cred": 0,
        },
    )
    client.post(
        "/api/advisors",
        json={"s_id": "99991", "i_id": "10101"},
    )
    r = client.patch("/api/advisors/99991", json={"i_id": "83821"})
    assert r.status_code == 200
    assert r.json()["i_id"] == "83821"


def test_update_advisor_not_found(client):
    r = client.patch("/api/advisors/99999", json={"i_id": "10101"})
    assert r.status_code == 404


def test_delete_advisor(client):
    client.post(
        "/api/students",
        json={
            "id": "99992",
            "name": "Advisee3",
            "dept_name": "Comp. Sci.",
            "tot_cred": 0,
        },
    )
    client.post(
        "/api/advisors",
        json={"s_id": "99992", "i_id": "10101"},
    )
    r = client.delete("/api/advisors/99992")
    assert r.status_code == 204
    r2 = client.get("/api/advisors/99992")
    assert r2.status_code == 404


def test_delete_advisor_not_found(client):
    r = client.delete("/api/advisors/99999")
    assert r.status_code == 404
