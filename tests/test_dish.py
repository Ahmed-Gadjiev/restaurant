import pytest
from fastapi.testclient import TestClient
from main import app

# from tests.test_menu import menu_id
# from tests.test_submenu import submenu_id

client = TestClient(app)

sample_menu = {"title": "Test Menu", "description": "Test Menu Description"}

sample_submenu = {"title": "Test Submenu", "description": "Test Submenu Description"}

sample_dish = {"title": "Test Dish", "description": "Test Dish Description", "price": '9.99'}
sample_updated_dish = {"title": "Updated Dish", "description": "Updated Dish Description", "price": '12.49'}

dish_id = None


def test_create_dish():
    global menu_id
    global submenu_id

    menu_id = client.post("api/v1/menus", json=sample_menu).json()['id']
    submenu_id = client.post(f"api/v1/menus/{menu_id}/submenus", json=sample_submenu).json()['id']

    resp = client.post(f"api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json=sample_dish)
    assert resp.status_code == 201
    assert "id" in resp.json()

    global dish_id
    dish_id = resp.json()["id"]


def test_read_dish():
    resp = client.get(f"api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert resp.status_code == 200
    assert resp.json()["title"] == sample_dish["title"]


def test_update_dish():
    resp = client.patch(f"api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", json=sample_updated_dish)
    assert resp.status_code == 200
    assert resp.json()["title"] == sample_updated_dish["title"]


def test_read_updated_dish():
    response = client.get(f"api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 200
    assert response.json()["title"] == sample_updated_dish["title"]


def test_delete_dish():
    response = client.delete(f"api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 200
    assert response.json()["status"] is True


def test_read_deleted_dish():
    response = client.get(f"api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "dish not found"
