from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from db import Session, Submenu, Dish

router = APIRouter()
session = Session()


class DishModel(BaseModel):
    title: str
    description: str
    price: str


@router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
async def get_dishes(menu_id, submenu_id):
    submenu = session.get(Submenu, submenu_id)

    if submenu is None:
        return []

    return submenu.dishes


@router.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', status_code=201)
async def create_dish(menu_id, submenu_id, body: DishModel):
    submenu = session.get(Submenu, submenu_id)

    if submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")

    new_dish = Dish(title=body.title, description=body.description, price=body.price)
    submenu.dishes.append(new_dish)
    session.commit()

    return {
        'id': new_dish.id,
        'title': new_dish.title,
        'description': new_dish.description,
        'price': str(new_dish.price)
    }


@router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
async def get_dish(menu_id, submenu_id, dish_id):
    dish = session.query(Dish).get(dish_id)

    if dish is None:
        raise HTTPException(status_code=404, detail="dish not found")

    return {
        'id': dish.id,
        'title': dish.title,
        'description': dish.description,
        'price': str(dish.price)
    }


@router.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
async def update_dish(menu_id, submenu_id, dish_id, body: DishModel):
    dish = session.get(Dish, dish_id)

    if dish is None:
        raise HTTPException(status_code=404, detail="dish not found")

    dish.title = body.title
    dish.description = body.description
    dish.price = body.price

    session.commit()

    return {
        'id': dish.id,
        'title': dish.title,
        'description': dish.description,
        'price': str(dish.price)
    }


@router.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
async def delete_dish(menu_id, submenu_id, dish_id):
    dish = session.get(Dish, dish_id)

    session.delete(dish)
    session.commit()

    return {
        "status": True,
        "message": "The dish has been deleted"
    }
