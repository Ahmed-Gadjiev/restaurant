from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from db import Menu, Session
from helpers import get_dishes_count

router = APIRouter()
session = Session()


class MenuModel(BaseModel):
    title: str
    description: str


@router.get("/api/v1/menus")
async def get_menus():
    menus = session.query(Menu).all()

    if menus is None:
        raise HTTPException(status_code=404, detail="menu not found")

    def counts(menu):
        return {
            'id': menu.id,
            'description': menu.description,
            'title': menu.title,
            'submenus_count': len(menu.submenus),
            'dishes_count': get_dishes_count(menu)
        }

    menus = list(map(counts, menus))

    return menus


@router.post('/api/v1/menus', status_code=201)
async def create_menu(body: MenuModel):
    new_menu = Menu(title=body.title, description=body.description)
    session.add(new_menu)
    session.commit()

    return {
        "id": new_menu.id,
        "title": new_menu.title,
        "description": new_menu.description,
        'submenus_count': len(new_menu.submenus),
        'dishes_count': get_dishes_count(new_menu)
    }


@router.get('/api/v1/menus/{menu_id}')
async def get_menu(menu_id):
    menu = session.query(Menu).get(menu_id)
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    return {
        'id': menu.id,
        'title': menu.title,
        'description': menu.description,
        'submenus_count': len(menu.submenus),
        'dishes_count': get_dishes_count(menu)
    }


@router.patch('/api/v1/menus/{menu_id}')
async def update_menu(menu_id, body: MenuModel):
    menu = session.query(Menu).get(menu_id)

    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    menu.title = body.title
    menu.description = body.description

    session.commit()

    return {
        'id': menu.id,
        'title': menu.title,
        'description': menu.description
    }


@router.delete('/api/v1/menus/{menu_id}')
async def delete_menu(menu_id):
    menu = session.query(Menu).get(menu_id)

    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    session.delete(menu)
    session.commit()

    return {
        "status": True,
        "message": "The menu has been deleted"
    }
