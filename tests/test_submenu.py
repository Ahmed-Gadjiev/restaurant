import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

sample_menu = {"title": "Test Menu", "description": "Test Menu Description"}
sample_submenu = {"title": "Test Submenu", "description": "Test Submenu Description"}
sample_updated_submenu = {"title": "Updated Submenu", "description": "Updated Submenu Description"}

menu_id = None
submenu_id = None


def test_create_submenu():
    global menu_id
    menu_id = client.post("api/v1/menus", json=sample_menu).json()['id']

    resp = client.post(f"api/v1/menus/{menu_id}/submenus", json=sample_submenu)
    assert resp.status_code == 201
    assert "id" in resp.json()

    global submenu_id
    submenu_id = resp.json()["id"]


def test_read_submenu():
    resp = client.get(f"api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert resp.status_code == 200
    assert resp.json()["title"] == sample_submenu["title"]


def test_update_submenu():
    resp = client.patch(f"api/v1/menus/{menu_id}/submenus/{submenu_id}", json=sample_updated_submenu)
    assert resp.status_code == 200
    assert resp.json()["title"] == sample_updated_submenu["title"]


def test_read_updated_submenu():
    response = client.get(f"api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200
    assert response.json()["title"] == sample_updated_submenu["title"]


def test_delete_submenu():
    response = client.delete(f"api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200
    assert response.json()["status"] is True


def test_read_deleted_submenu():
    response = client.get(f"api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "submenu not found"
