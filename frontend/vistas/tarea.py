from datetime import datetime
import json
import jwt
import os
import requests
import flet as ft
from globals.session_state import SessionState
from flet_route import Params, Basket

def tarea(page: ft.Page, params: Params, basket: Basket):

    global jwt_token
    jwt_token = SessionState.jwt
    decoded_token = jwt.decode(str(jwt_token), SessionState.secret, algorithms=["HS256"])
    user_name = decoded_token["sub"]
    global categoria
    categoria = ""
    global categorias_data
    global id_categoria

    def change_route(param1):
        if param1 == 0:
            page.go("/gestion")
        elif param1 == 1:
            page.go("/categoria")

    #-- CREACION DE IMAGE
    img = ft.Image(
                                src=f"./uploads/{user_name}.jpg",
                                width=100,
                                height=100,
                                visible=True,
                                fit=ft.ImageFit.CONTAIN,
                            )


    #----- ELEMENTOS -----#
    #Titulos de inicio
    title = ft.Text("Tareas", size=30)
    title2 = ft.Text("Mis Tareas", size=30)

    #Tabla con las tareas del usuario
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Tarea")),
            ft.DataColumn(ft.Text("Fecha de finalización")),
            ft.DataColumn(ft.Text("Estado")),

        ]
    )
    #Inserta datos a la tabla
    def addDataTable(tareas_usuario):
        for tarea in tareas_usuario:
            table.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(tarea["id"])),
                ft.DataCell(ft.Text(tarea["texto_tarea"])),
                ft.DataCell(ft.Text(tarea["fecha_finalizacion"])),
                ft.DataCell(ft.Text(tarea["estado_tarea"]["llave"])),
                    ]
                )
            )
    #Para escoger la fecha
    date_picker = ft.DatePicker(
        first_date=datetime(2024, 1, 1),
        last_date=datetime(2025, 1, 1),
    )
    #Inserta el datepicker
    page.overlay.append(date_picker)

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
                icon_content=ft.Icon(ft.icons.BOOKMARK_BORDER),
                selected_icon_content=ft.Icon(ft.icons.BOOKMARK_BORDER),
                label="Categorias",
            ),
        ],
        on_change=lambda e: change_route(e.control.selected_index)
    )

    estados = ft.Dropdown(
        width=150,
        options=[
            ft.dropdown.Option("SIN_EMPEZAR"),
            ft.dropdown.Option("EMPEZADA"),
            ft.dropdown.Option("FINALIZADA"),
        ],
        visible= False
    )
    page.add(estados)

    #----- TERMINACION ELEMENTOS-----#
    
    #----- PETICIONES -----#
    #Funcion generada para retornar las tareas del usuario de la sesion
    def getTareasUsuario():
        url = "http://127.0.0.1:5000/tareas/"+user_name 
        response = requests.get(url)
        if response.status_code == 200:
            tareas_usuario = response.json()
            addDataTable(tareas_usuario)
        else:
            print("Error en la solicitud GET:", response.text)
    
    # Llamar a datos al cargar la página
    getTareasUsuario()

    #Lista de categorias creadas
    categorias = []
    #Retorno de categorias
    def getCategorias():
        url = "http://127.0.0.1:5000/categorias"  
        response = requests.get(url)
        if response.status_code == 200:
            global categorias_data
            categorias_data = response.json()
            fillCategorias(categorias_data)
        else:
            print("Error en la solicitud GET:", response.text)
    #Funcion creada para crear tarea 
    def create_tarea():
        titulo = title_input.value
        fecha = datetime.strptime(str(date_picker.value), '%Y-%m-%d %H:%M:%S')
        global id_categoria
        categoria_data = {
            "texto": titulo,
            "fecha_finalizacion": str(fecha),
            "id_categoria": id_categoria
        }
        categoria_data_json = json.dumps(categoria_data)
        print("Datos de usuario guardados en JSON:", categoria_data_json)

        url = "http://127.0.0.1:5000/tareas"  
        global jwt_token
        print("Bearer " + str(jwt_token) )
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(jwt_token)  
        }
        response = requests.post(url, data=categoria_data_json, headers=headers)
    
        if response.status_code == 200:
            print("Solicitud POST exitosa!")
            table.rows.clear()
            getTareasUsuario()
            page.update()

        else:
            print("Error en la solicitud POST:", response.text)

    #Funcion creada para actualizar tarea
    def actualizar_tarea():
        titulo = tarea_input.value
        fecha = datetime.strptime(str(date_picker.value), '%Y-%m-%d %H:%M:%S')
        tarea_data = {
            "texto": titulo,
            "fecha_finalizacion": str(fecha),
            "estado_tarea": estados.value
        }
        tarea_data_json = json.dumps(tarea_data)
        print("Datos de usuario guardados en JSON:", tarea_data_json)

        url = "http://127.0.0.1:5000/tareas/"+str(id_input.value)  
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(jwt_token)  
        }
        response = requests.put(url, data=tarea_data_json, headers=headers)
    
        if response.status_code == 200:
            print("Solicitud PUT exitosa!")
            table.rows.clear()
            getTareasUsuario()
            page.update()

        else:
            print("Error en la solicitud PUT:", response.text)

    def delete_tarea():
        id = id_eliminacion.value
        url = "http://127.0.0.1:5000/tareas/"+str(id) 
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(jwt_token)  
        }
        response = requests.delete(url,headers=headers)
        
        if response.status_code == 200:
            print("Solicitud DELETE exitosa!")
            table.rows.clear()
            getTareasUsuario()
            page.update()
        else:
            print("Error en la solicitud DELETE:", response.text)
    
    
    #----- TERMINACION PETICIONES -----#
            

    #----- CREACION DE MENUBAR DE CATEGORIAS -----#

    def saveCategoria(e):
        global categoria
        categoria = e.control.content.value
        global categorias_data
        for categoria in categorias_data:
            if categoria["nombre_categoria"]==categoria["nombre_categoria"]:
                global id_categoria
                id_categoria = categoria["id"]

    #Creacion de MenuItemButton de categorias
    def fillCategorias(categorias_data):
        for categoria in categorias_data:
            categoria_sub_menu = ft.MenuItemButton(
                        content=ft.Text(categoria["nombre_categoria"]),
                        on_click= saveCategoria
                    )
            categorias.append(categoria_sub_menu)

    getCategorias()

    #Menu de categorias
    menubar = ft.MenuBar(
        visible=False,
        style= ft.MenuStyle(
            bgcolor=ft.colors.WHITE,
        ),
        controls=[
            ft.SubmenuButton(
                content=ft.Text("Categorias"),
                controls=categorias,
                
            ),
        ]
    )

    #----- TERMINACION DE MENUBAR DE CATEGORIAS -----#

    

    #Elementos para la actualizacion de la tarea
    actualizar_tarea_button = ft.ElevatedButton("Actualizar Tarea", on_click=lambda _: visibilidad_actualizar_tarea())
    id_input = ft.TextField(label="id", visible=False,width=300)
    tarea_input = ft.TextField(label="Texto de tarea", visible=False,width=300)
    fecha_button_nueva = ft.ElevatedButton("Fecha de finalización nueva", visible=False,width=250,on_click=lambda _: date_picker.pick_date())
    actualizar_tarea_button_bottom = ft.ElevatedButton("Actualizar", on_click=lambda _: actualizar_tarea(), visible=False)

    def visibilidad_actualizar_tarea():
        if id_input.visible:
            id_input.visible = False
            tarea_input.visible = False
            fecha_button_nueva.visible = False
            estados.visible = False
            actualizar_tarea_button.text = "Actualizar Tarea"
            actualizar_tarea_button_bottom.visible = False
        else:
            id_input.visible = True
            tarea_input.visible = True
            fecha_button_nueva.visible = True
            estados.visible = True
            actualizar_tarea_button.text = "Atrás"
            actualizar_tarea_button_bottom.visible = True
        page.update()

    #Elementos para la creacion de la tarea
    crear_categoria_button = ft.ElevatedButton("Crear Tarea", on_click=lambda _: visibilidad_crear_tarea())
    title_input = ft.TextField(label="Título", visible=False,width=300)
    fecha_button = ft.ElevatedButton("Fecha de finalización", visible=False,width=200,on_click=lambda _: date_picker.pick_date())
    crear_categoria_button_bottom = ft.ElevatedButton("Crear Tarea", on_click=lambda _: create_tarea(), visible=False)

    def visibilidad_crear_tarea():
        if title_input.visible:
            title_input.visible = False
            fecha_button.visible = False
            menubar.visible = False
            crear_categoria_button.text = "Crear Tarea"
            crear_categoria_button_bottom.visible = False
        else:
            title_input.visible = True
            fecha_button.visible = True
            menubar.visible = True
            crear_categoria_button.text = "Atrás"
            crear_categoria_button_bottom.visible = True
        page.update()

    #Elementos para la eliminacion de la tarea
    eliminar_tarea_button = ft.ElevatedButton("Eliminar Tarea", on_click=lambda _: visibilidad_eliminar_tarea())
    id_eliminacion = ft.TextField(label="id", visible=False,width=300)
    eliminar_tarea_button_bottom = ft.ElevatedButton("Eliminar Categoria", on_click=lambda _: delete_tarea(), visible=False)

    def visibilidad_eliminar_tarea():
        if id_eliminacion.visible:
            id_eliminacion.visible = False
            eliminar_tarea_button.text = "Eliminar Categoria"
            eliminar_tarea_button_bottom.visible = False
        else:
            id_eliminacion.visible = True
            eliminar_tarea_button.text = "Atrás"
            eliminar_tarea_button_bottom.visible = True
        page.update()

    
    

    return ft.View(
        "/tarea",
        controls=[
            ft.Row(
                [
                    rail,
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        [
                            title,
                            ft.Row([crear_categoria_button, actualizar_tarea_button, eliminar_tarea_button]),
                            title_input,
                            fecha_button,
                            ft.Row([menubar]),
                            crear_categoria_button_bottom,
                            id_input,
                            tarea_input,
                            fecha_button_nueva,
                            estados,
                            actualizar_tarea_button_bottom,
                            id_eliminacion,
                            eliminar_tarea_button_bottom,
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
