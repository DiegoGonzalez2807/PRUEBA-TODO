# login_view.py
import flet as ft
import json
import requests
from globals.session_state import SessionState
from flet_route import Params, Basket

def login(page: ft.Page, params: Params, basket: Basket):
    page.title = "Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    username_field = ft.TextField(label="Usuario", autofocus=True, width=300)
    password_field = ft.TextField(label="Contraseña", width=300)

    def login_clicked(e):
        username = username_field.value
        password = password_field.value
        user_data = {
            "nombre_usuario": username,
            "contrasena": password
        }
        user_data_json = json.dumps(user_data)
        print("Datos de usuario guardados en JSON:", user_data_json)

        url = "http://127.0.0.1:5000/usuarios/iniciar-sesion" 
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, data=user_data_json, headers=headers)
        
        if response.status_code == 200:
            print("Solicitud POST exitosa!")
            jwt = response.json()["token_acceso"]
            SessionState.jwt = jwt
            page.go('/gestion')
        else:
            print("Error en la solicitud POST:", response.text)

    return ft.View(
        "/",
        controls=[
        ft.Column(
            [
                ft.Container(
                    content=ft.Text("Bienvenido al aplicativo de gestión de tareas!", size=30),
                    alignment=ft.alignment.center,
                    width=300,
                    padding=10,
                ),
                username_field,
                password_field,
                ft.Container(
                    content=ft.ElevatedButton("Iniciar Sesión", on_click=login_clicked),
                    margin=10,
                    alignment=ft.alignment.center,
                    width=300,
                ),
                ft.Container(
                    content=ft.ElevatedButton("Usuario Nuevo"),
                    margin=10,
                    alignment=ft.alignment.center,
                    width=300,
                    on_click=lambda e: page.go('/signin'),
                ),
            ],
     alignment=ft.MainAxisAlignment.CENTER,) 
        ]
        
    )
