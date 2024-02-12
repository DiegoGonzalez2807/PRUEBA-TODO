import os
import shutil
import flet as ft
import json
import requests
from flet_route import Params, Basket
from globals.session_state import SessionState


def signin(page: ft.Page, params: Params, basket: Basket):
    page.title = "Signin"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    username_field = ft.TextField(label="Nombre de Usuario", autofocus=True, width=300)
    password_field = ft.TextField(label="Contraseña", width=300)


    #--- IMAGEN
    img_avatar = ft.Image(
        src=f"photos/{username_field.value}.jpg",
        width=100,
        height=100,
        visible=False,
        fit=ft.ImageFit.CONTAIN,
    )

    page.add(img_avatar)
    #----- CREACION DE FILEPICKER -----
    

    def visible_image():
        img_avatar.src = f"photos/{username_field.value}.jpg"
        img_avatar.visible = True
        page.update()

    def upload_files(e:ft.FilePickerResultEvent):
        for x in e.files:
            if not os.path.exists("photos"):
                os.makedirs("photos")
            shutil.copy(str(x.path), f"photos/{username_field.value}.jpg")
        visible_image()
        


    file_picker = ft.FilePicker(on_result= upload_files)
    page.overlay.append(file_picker)

    #----- TERMINACION FILE PICKER


    def open_dlg():
        page.dialog = dialog
        dialog.open = True
        page.update()

    def close_dlg(e):
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
            title=ft.Text("Felicidades"),
            content=ft.Text("Usuario creado exitosamente!"),
            actions=[ft.ElevatedButton("Entendido", on_click=close_dlg)],
            on_dismiss=lambda e: page.go("/gestion"),
        )
    
 
    def signin_clicked(e):
        username = username_field.value
        password = password_field.value
        user_data = {
            "nombre_usuario": username,
            "contrasena": password
        }
        user_data_json = json.dumps(user_data)
        print("Datos de usuario guardados en JSON:", user_data_json)

        url = "http://127.0.0.1:5000/usuarios"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, data=user_data_json, headers=headers)

        if response.status_code == 200:
            print("Solicitud POST exitosa!")
            url = "http://127.0.0.1:5000/usuarios/iniciar-sesion"
            headers = {"Content-Type": "application/json"}
            response2 = requests.post(url, data=user_data_json, headers=headers)
            if response2.status_code == 200:
                jwt = response2.json()["token_acceso"]
                SessionState.jwt = jwt
                open_dlg()
            
        else:
            print("Error en la solicitud POST:", response.text)

    

    return ft.View(
        "/signin",
        controls=[
            ft.Column(
                [
                    ft.Container(
                        content=ft.Text("Registrate", size=30),
                        alignment=ft.alignment.center,
                        width=300,
                        padding=10,
                    ),
                    username_field,
                    password_field,
                    img_avatar,
                    ft.Container(
                        content=ft.ElevatedButton("Seleccionar Archivos", on_click=lambda _: file_picker.pick_files(allow_multiple=True)),
                        margin=10,
                        alignment=ft.alignment.center,
                        width=300,
                    ),
                    ft.Container(
                        content=ft.ElevatedButton("Crear Usuario", on_click=signin_clicked),
                        margin=10,
                        alignment=ft.alignment.center,
                        width=300,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ]
    )
