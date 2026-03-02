"""Tests for classroom CRUD endpoints."""

import pytest


def test_list_classrooms(client):
    r = client.get("/api/classrooms")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "building" in data[0] and "room_number" in data[0] and "capacity" in data[0]


def test_get_classroom(client):
    r = client.get("/api/classrooms/Packard/101")
    assert r.status_code == 200
    assert r.json() == {"building": "Packard", "room_number": "101", "capacity": 500}


def test_get_classroom_not_found(client):
    r = client.get("/api/classrooms/Nonexistent/999")
    assert r.status_code == 404


def test_create_classroom(client):
    r = client.post(
        "/api/classrooms",
        json={"building": "TestBldg", "room_number": "999", "capacity": 25},
    )
    assert r.status_code == 201
    assert r.json()["building"] == "TestBldg"
    assert r.json()["room_number"] == "999"
    assert r.json()["capacity"] == 25


def test_update_classroom(client):
    client.post(
        "/api/classrooms",
        json={"building": "TestBldg2", "room_number": "888", "capacity": 10},
    )
    r = client.patch("/api/classrooms/TestBldg2/888", json={"capacity": 30})
    assert r.status_code == 200
    assert r.json()["capacity"] == 30


def test_update_classroom_not_found(client):
    r = client.patch("/api/classrooms/X/Y", json={"capacity": 5})
    assert r.status_code == 404


def test_delete_classroom(client):
    client.post(
        "/api/classrooms",
        json={"building": "DelBldg", "room_number": "777", "capacity": 5},
    )
    r = client.delete("/api/classrooms/DelBldg/777")
    assert r.status_code == 204
    r2 = client.get("/api/classrooms/DelBldg/777")
    assert r2.status_code == 404


def test_delete_classroom_not_found(client):
    r = client.delete("/api/classrooms/X/Y")
    assert r.status_code == 404
