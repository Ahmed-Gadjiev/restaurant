from fastapi import FastAPI
from routes import menu, submenu, dish

app = FastAPI()
app.include_router(menu.router)
app.include_router(submenu.router)
app.include_router(dish.router)
