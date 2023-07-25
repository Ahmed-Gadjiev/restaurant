from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from db import Menu, Session, Submenu

router = APIRouter()
session = Session()


class SubmenuModel(BaseModel):
    title: str
    description: str


@router.get('/api/v1/menus/{menu_id}/submenus')
async def get_submenus(menu_id):
    menu = session.query(Menu).get(menu_id)

    if menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")

    return menu.submenus


@router.post('/api/v1/menus/{menu_id}/submenus', status_code=201)
async def create_submenu(menu_id, body: SubmenuModel):
    menu = session.query(Menu).get(menu_id)

    if menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")

    new_submenu = Submenu(title=body.title, description=body.description, menu_id=menu_id)
    menu.submenus.append(new_submenu)

    session.commit()

    return {
        'id': new_submenu.id,
        'title': new_submenu.title,
        'description': new_submenu.description,
        'dishes_count': 0
    }


@router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
async def get_submenu(menu_id, submenu_id):
    submenu = session.query(Submenu).get(submenu_id)

    if submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")

    return {
        'id': submenu.id,
        'title': submenu.title,
        'description': submenu.description,
        'dishes_count': len(submenu.dishes)
    }


@router.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
async def update_submenu(menu_id, submenu_id, body: SubmenuModel):
    submenu = session.query(Submenu).get(submenu_id)

    if submenu is None:
        raise HTTPException(status_code=404, detail="Menu not found")

    submenu.title = body.title
    submenu.description = body.description

    session.commit()

    return {
        'id': submenu.id,
        'title': submenu.title,
        'description': submenu.description
    }


@router.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
async def delete_submenu(menu_id, submenu_id):
    submenu = session.query(Submenu).get(submenu_id)

    if submenu is None:
        raise HTTPException(status_code=404, detail="Menu not found")

    session.delete(submenu)
    session.commit()

    return {
        "status": True,
        "message": "The submenu has been deleted"
    }
