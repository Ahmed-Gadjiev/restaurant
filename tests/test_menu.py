import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

sample_menu = {"title": "Test Menu", "description": "Test Menu Description"}
sample_updated_menu = {"title": "Updated Menu", "description": "Updated Menu Description"}

menu_id = None


def test_create_menu():
    resp = client.post("api/v1/menus", json=sample_menu)
    assert resp.status_code == 201
    assert "id" in resp.json()

    global menu_id
    menu_id = resp.json()["id"]


def test_read_menu():
    resp = client.get(f'api/v1/menus/{menu_id}')
    assert resp.status_code == 200
    assert resp.json()["title"] == sample_menu["title"]


def test_update_menu():
    resp = client.patch(f'api/v1/menus/{menu_id}', json=sample_updated_menu)
    assert resp.status_code == 200
    assert resp.json()["title"] == sample_updated_menu["title"]


def test_read_updated_menu():
    response = client.get(f"api/v1/menus/{menu_id}")
    assert response.status_code == 200
    assert response.json()["title"] == sample_updated_menu["title"]


def test_delete_menu():
    response = client.delete(f"api/v1/menus/{menu_id}")
    assert response.status_code == 200
    assert response.json()["status"] is True


def test_read_deleted_menu():
    response = client.get(f"api/v1/menus/{menu_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "menu not found"
