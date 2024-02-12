import flet as ft
import jwt
import os
from datetime import datetime
from flet_route import Params, Basket 
from globals.session_state import SessionState

def gestion(page: ft.Page, params: Params, basket: Basket):
    today_date = datetime.now().strftime("%d/%m/%Y")

    print(SessionState.jwt)
    jwt_token = SessionState.jwt
    decoded_token = jwt.decode(str(jwt_token), SessionState.secret, algorithms=["HS256"])
    user_name = decoded_token["sub"]
    title = ft.Text("HOY, " + today_date, size=20)
    title2 = ft.Text("Bienvenido, " + user_name, size=30)

    #-- CREACION DE IMAGE
    img = ft.Image(
                                src=f"./uploads/{user_name}.jpg",
                                width=100,
                                height=100,
                                visible=True,
                                fit=ft.ImageFit.CONTAIN,
                            )

    def change_route(param1):
        if param1 == 0:
            page.go("/categoria")
        elif param1 == 1:
            page.go("/tarea")
        elif param1 == 2:
            page.go("/")
    
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.FAVORITE_BORDER, selected_icon=ft.icons.CATEGORY, label="Categorias"
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.BOOKMARK_BORDER),
                selected_icon_content=ft.Icon(ft.icons.ADD_TASK),
                label="Tareas",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.LOGOUT, selected_icon=ft.icons.LOGOUT, label="Cerrar Sesión"
            ),
        ],
        on_change=lambda e: change_route (e.control.selected_index)
    )

    return ft.View(
        "/gestion",
        controls=[ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                ft.Column(
                    [title,title2
                     ],
                    alignment=ft.MainAxisAlignment.START,
                    expand=True,
                    spacing=10
                ),
                ft.Container(
                    content=img,
                    alignment=ft.alignment.top_right,
                    padding=10
                )
            ],
            expand=True,
        )])


 