# main.py
import flet as ft
from flet_route import Routing,path
from vistas.login import login
from vistas.signin import signin
from vistas.gestion import gestion
from vistas.categoria import categoria
from vistas.tarea import tarea

def main(page: ft.Page):
     app_routes = [
        path(
            url="/", 
            clear=True,
            view=login 
            ),
        path(
            url="/signin", 
            clear=True, 
            view=signin
            ), 
        path(
            url="/gestion", 
            clear=True, 
            view=gestion 
            ),
        path(
            url="/categoria", 
            clear=True, 
            view=categoria 
            ),
        path(
            url="/tarea", 
            clear=True, 
            view=tarea 
            ),
    ]
     Routing(
        page=page,
        app_routes=app_routes, 
        )
     page.go(page.route)

ft.app(port=8080,target=main, assets_dir="assets", upload_dir="assets/uploads", view=ft.AppView.WEB_BROWSER)
