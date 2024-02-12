import json
import requests
import flet as ft
import jwt
import os
from globals.session_state import SessionState
from flet_route import Params, Basket

def categoria(page: ft.Page, params: Params, basket: Basket):

    global jwt_token
    jwt_token = SessionState.jwt
    decoded_token = jwt.decode(str(jwt_token), SessionState.secret, algorithms=["HS256"])
    user_name = decoded_token["sub"]

    def change_route(param1):
        if param1 == 0:
            page.go("/gestion")
        elif param1 == 1:
            page.go("/tarea")

    img = ft.Image(
                                src=f"./uploads/{user_name}.jpg",
                                width=100,
                                height=100,
                                visible=True,
                                fit=ft.ImageFit.CONTAIN,
                            )


    title = ft.Text("Categorias", size=30)
    title2 = ft.Text("Mis categorias", size=30)


    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Categoria")),
            ft.DataColumn(ft.Text("Descripcion")),
        ]
    )

    def addDataTable(categorias_data):
        for categoria in categorias_data:
            table.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(categoria["id"])),
                ft.DataCell(ft.Text(categoria["nombre_categoria"])),
                ft.DataCell(ft.Text(categoria["descripcion"])),
                    ]
                )
            )
    
    def getCategorias():
        url = "http://127.0.0.1:5000/categorias"  
        response = requests.get(url)
        if response.status_code == 200:
            categorias_data = response.json()
          
            addDataTable(categorias_data)
        else:
            print("Error en la solicitud GET:", response.text)
    
    # Llamar a getCategorias() al cargar la página
    getCategorias()

    def create_categoria():
        titulo = title_input.value
        descripcion = description_input.value
        categoria_data = {
            "nombre": titulo,
            "descripcion": descripcion
        }
        categoria_data_json = json.dumps(categoria_data)
        print("Datos de usuario guardados en JSON:", categoria_data_json)

        url = "http://127.0.0.1:5000/categorias"
        global jwt_token  
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(jwt_token)  
        }
        response = requests.post(url, data=categoria_data_json, headers=headers)
        
        if response.status_code == 200:
            print("Solicitud POST exitosa!")
            table.rows.clear()
            getCategorias()
            page.update()
        else:
            print("Error en la solicitud POST:", response.text)
    
    def delete_categoria():
        id = id_input.value
        url = "http://127.0.0.1:5000/categorias/"+str(id) 
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(jwt_token)  
        }
        response = requests.delete(url, headers=headers)
        
        if response.status_code == 200:
            print("Solicitud DELETE exitosa!")
            table.rows.clear()
            getCategorias()
            page.update()
        else:
            print("Error en la solicitud DELETE:", response.text)
    
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.ARROW_BACK, selected_icon=ft.icons.ARROW_BACK, label="Volver"
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.ADD_TASK),
                selected_icon_content=ft.Icon(ft.icons.ADD_TASK),
                label="Tareas",
            ),
        ],
        on_change=lambda e: change_route(e.control.selected_index)
    )

    #Elementos para la eliminacion de la categoria
    eliminar_categoria_button = ft.ElevatedButton("Eliminar Categoria", on_click=lambda _: visibilidad_eliminar_categoria())
    id_input = ft.TextField(label="id", visible=False,width=300)
    eliminar_categoria_button_bottom = ft.ElevatedButton("Eliminar Categoria", on_click=lambda _: delete_categoria(), visible=False)


    #Elementos para la creacion de la categoria
    crear_categoria_button = ft.ElevatedButton("Crear Categoria", on_click=lambda _: visibilidad_crear_categoria())
    title_input = ft.TextField(label="Título", visible=False,width=300)
    description_input = ft.TextField(label="Descripción", visible=False,width=300)
    crear_categoria_button_bottom = ft.ElevatedButton("Crear Categoria", on_click=lambda _: create_categoria(), visible=False)

    def visibilidad_crear_categoria():
        if title_input.visible:
            title_input.visible = False
            description_input.visible = False
            crear_categoria_button.text = "Crear Categoria"
            crear_categoria_button_bottom.visible = False
        else:
            title_input.visible = True
            description_input.visible = True
            crear_categoria_button.text = "Atrás"
            crear_categoria_button_bottom.visible = True
        page.update()
    
    def visibilidad_eliminar_categoria():
        if id_input.visible:
            id_input.visible = False
            eliminar_categoria_button.text = "Eliminar Categoria"
            eliminar_categoria_button_bottom.visible = False
        else:
            id_input.visible = True
            eliminar_categoria_button.text = "Atrás"
            eliminar_categoria_button_bottom.visible = True
        page.update()

    return ft.View(
        "/categoria",
        controls=[
            ft.Row(
                [
                    rail,
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        [
                            title,
                            ft.Row([crear_categoria_button, eliminar_categoria_button]), 
                            title_input,
                            description_input,
                            crear_categoria_button_bottom,
                            id_input,
                            eliminar_categoria_button_bottom,
                            title2,
                            table

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
            )
        ]
    )
