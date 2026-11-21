import os
import subprocess
from pathlib import Path

import flet as ft

ENGINE = Path(__file__).resolve().parents[1] / 'build' / 'analyzer.exe'

def main(page: ft.Page):
    page.window.bgcolor = ft.Colors.WHITE
    page.bgcolor = ft.Colors.WHITE
    page.window.always_on_bottom = False
    page.window.always_on_top = False
    page.window.frameless = False
    page.window.full_screen = False
    page.window.ignore_mouse_events = False
    page.window.resizable = True
    page.window.title_bar_hidden = True
    page.window.title_bar_buttons_hidden = True
    page.window.shadow = True
    page.padding = 0
    page.window.maximized = True

    def minimizar(e):
        page.window.minimized = True
        page.update()

    def maximizar(e):
        page.window.maximized = True
        page.update()

    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            file = e.files[0]
            with open(file.path, "r", encoding="utf-8") as f:
                contenido = f.read()


            lista_de_pestanias_codigo.tabs.append(
                ft.Tab(
                    tab_content=ft.Row([
                        ft.Text(f"   {file.name}   ", tooltip=f"{file.path}"),
                        ft.Icon(name=None,color="#12b232"),
                        ft.IconButton(ft.Icons.CLOSE, icon_size=18, tooltip="Cerrar pestaña", on_click=cerrar_pestania_codigo)
                    ], spacing=0),
                    content=Editor_de_codigo_del_Lenguaje(contenido_inicial=contenido)
                )
            )
            lista_de_pestanias_codigo.selected_index = len(lista_de_pestanias_codigo.tabs) - 1
            lista_de_pestanias_codigo.update()
        else:
            print("Nada")

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)

    def save_file_result(e: ft.FilePickerResultEvent):
        if e.path:
            file_path = e.path
            index = lista_de_pestanias_codigo.selected_index
            if not file_path.lower().endswith(".txt"):
                file_path += ".txt"

            contexto = lista_de_pestanias_codigo.tabs[index].content.controls[0].controls[1].controls[0].controls[0].value

            texto_procesado = '\n'.join([
                linea.rstrip()
                for linea in contexto.splitlines()
                if linea.strip() != ""
            ])

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(texto_procesado)  # Guardar el contenido del TextField en el archivo .txt

            file_name = os.path.basename(file_path)  # Obtener solo el nombre del archivo
            lista_de_pestanias_codigo.tabs[index].tab_content.controls[0].value = f"   {file_name}   "
            lista_de_pestanias_codigo.tabs[index].tab_content.controls[0].tooltip=f"{file_path}"
            lista_de_pestanias_codigo.tabs[index].tab_content.update()
            lista_de_pestanias_codigo.update()
        else:
            print("Operación cancelada")

    save_file_dialog = ft.FilePicker(on_result=save_file_result)
    page.overlay.append(save_file_dialog)

    cupertino_alert_dialog_archivo_guardado = ft.CupertinoAlertDialog(
        title=ft.Text("Archivo guardado",color="blue"),
        content=ft.Text("El archivo actual ha sido guardado correctamente."),
        modal=False
    )

    page.overlay.append(cupertino_alert_dialog_archivo_guardado)

    def guardar_archivo_verificar(e):
        index = lista_de_pestanias_codigo.selected_index
        ruta_archivo = lista_de_pestanias_codigo.tabs[index].tab_content.controls[0].tooltip
        if ruta_archivo == None:
            save_file_dialog.save_file(
                file_name="programa_fuente.txt",
                allowed_extensions=["txt"]
            )
        else:
            contexto = lista_de_pestanias_codigo.tabs[index].content.controls[0].controls[1].controls[0].controls[0].value

            texto_procesado = '\n'.join([
                linea.rstrip()  # Solo elimina espacios del lado derecho
                for linea in contexto.splitlines()
                if linea.strip() != ""  # Mantiene la indentación izquierda
            ])

            with open(ruta_archivo, "w", encoding="utf-8") as f:
                f.write(texto_procesado)
            cupertino_alert_dialog_archivo_guardado.open = True
            page.update()
        quitar_simbolo_no_guardado(e)

    def poner_simbolo_no_guardado(e):
        index = lista_de_pestanias_codigo.selected_index
        nombre_archivo = lista_de_pestanias_codigo.tabs[index].tab_content.controls[0].value
        if nombre_archivo != "   Sin Nombre   ":
            lista_de_pestanias_codigo.tabs[index].tab_content.controls[1].name = ft.Icons.CIRCLE_NOTIFICATIONS
            lista_de_pestanias_codigo.update()

    def quitar_simbolo_no_guardado(e):
        index = lista_de_pestanias_codigo.selected_index
        lista_de_pestanias_codigo.tabs[index].tab_content.controls[1].name = None
        lista_de_pestanias_codigo.update()

    def Editor_de_codigo_del_Lenguaje(contenido_inicial=""):
        numero_de_lineas = ft.Text(
            value="1",
            font_family="Consolas",
            size=17,
            color="#8b92b9",
            width=50,
            text_align=ft.TextAlign.RIGHT,
            weight="bold"
        )
        ingreso_de_codigo = ft.TextField(
            multiline=True,
            expand=True,
            min_lines=1,
            max_lines=None,
            content_padding=ft.Padding(top=68, left=20,right=0,bottom=0),
            text_style=ft.TextStyle(color="#00172f"),
            hint_text="Archivo actual sin contenido fuente...",
            hint_style=ft.TextStyle(color="#00172f"),
            cursor_color = "black",
            dense=True,
            value=contenido_inicial,
            autofocus=True,
            mouse_cursor=ft.MouseCursor.TEXT
        )

        scroll_contenedor = ft.Column(
            [
                ft.Row(
                    [ingreso_de_codigo],
                    scroll="auto",
                    expand=True,
                    vertical_alignment="start"
                )
            ],
            expand=True
        )

        num_caracteres = ft.Text("[0]", color="#8b92b9",weight="bold",text_align=ft.TextAlign.RIGHT,width=50)

        def update_line_numbers(e):
            lines = ingreso_de_codigo.value.split('\n')
            numero_de_lineas.value = '\n'.join(str(i + 1) for i in range(len(lines) or 1))
            num_caracteres.value = f"[{len(ingreso_de_codigo.value)}]"
            num_caracteres.update()
            numero_de_lineas.update()

        def padre_update(e):
            update_line_numbers(e)
            poner_simbolo_no_guardado(e)

        ingreso_de_codigo.on_change = padre_update
        ingreso_de_codigo.on_focus = update_line_numbers

        return ft.ListView(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column([num_caracteres,numero_de_lineas]),
                        scroll_contenedor
                    ],
                    spacing=5,
                    vertical_alignment=ft.CrossAxisAlignment.START
                )
            ],
            expand=True,
            spacing=0,
        )

    def cerrar_pestania_codigo(e):
        boton_cerrar = e.control
        for i, tab in enumerate(lista_de_pestanias_codigo.tabs):
            if boton_cerrar in tab.tab_content.controls:

                del lista_de_pestanias_codigo.tabs[i]

                if lista_de_pestanias_codigo.selected_index >= len(lista_de_pestanias_codigo.tabs):
                    lista_de_pestanias_codigo.selected_index = max(0, len(lista_de_pestanias_codigo.tabs) - 1)
                lista_de_pestanias_codigo.update()
                break

    lista_de_pestanias_codigo = ft.Tabs(
        selected_index=0,
        animation_duration=200,
        divider_color="#12b232",
        divider_height=3,
        label_color="#12b232" ,
        label_text_style=ft.TextStyle(weight="bold"),
        overlay_color="#12b232",
        unselected_label_color = "black",
        unselected_label_text_style=ft.TextStyle(weight=ft.FontWeight.NORMAL),
        indicator_color="#12b232",
        indicator_thickness = 4,
        tabs=[
            ft.Tab(
                tab_content=ft.Row([ft.Text("   Sin Nombre   "),ft.Icon(name=None,color="#12b232"),ft.IconButton(ft.Icons.CLOSE,icon_size=18,tooltip="Cerrar pestaña",on_click=cerrar_pestania_codigo)],spacing=0),
                content=Editor_de_codigo_del_Lenguaje()
            )
        ],
        expand=True,
    )

    def crear_pestania_codigo(e):
        lista_de_pestanias_codigo.tabs.append(
            ft.Tab(
                tab_content=ft.Row([ft.Text("   Sin Nombre   "),ft.Icon(name=None,color="red"),ft.IconButton(ft.Icons.CLOSE,icon_size=18,tooltip="Cerrar pestaña",on_click=cerrar_pestania_codigo)],spacing=0),
                content=Editor_de_codigo_del_Lenguaje()
            )
        )
        lista_de_pestanias_codigo.selected_index= len(lista_de_pestanias_codigo.tabs) - 1
        lista_de_pestanias_codigo.update()

    cupertino_alert_dialog_debes_guardar_primero = ft.CupertinoAlertDialog(
        title=ft.Text("Guarda el archivo",color="#008e1c"),
        content=ft.Text("Para analizar un archivo debes guardarlo en tu sistema primero."),
        modal=False
    )
    page.overlay.append(cupertino_alert_dialog_debes_guardar_primero)

    def click_iniciar_analizador_sintactico_lexico(e):

        index = lista_de_pestanias_codigo.selected_index
        ruta_archivo = lista_de_pestanias_codigo.tabs[index].tab_content.controls[0].tooltip
        if ruta_archivo == None:
            cupertino_alert_dialog_debes_guardar_primero.open = True
            page.update()
            return

        try:
            fila_de_botones.content.controls[7].visible = True
            fila_de_botones.update()

            if lista_de_pestanias_codigo.tabs[index].tab_content.controls[1].name != None:
                contexto = lista_de_pestanias_codigo.tabs[index].content.controls[0].controls[1].controls[0].controls[0].value

                texto_procesado = '\n'.join([
                    linea.rstrip()
                    for linea in contexto.splitlines()
                    if linea.strip() != ""
                ])

                with open(ruta_archivo, "w", encoding="utf-8") as f:
                    f.write(texto_procesado)
                lista_de_pestanias_codigo.tabs[index].tab_content.controls[1].name = None
                lista_de_pestanias_codigo.update()

            resultado = subprocess.run(
                [str(ENGINE), ruta_archivo],
                capture_output=True,
                encoding="utf-8",
                errors="replace",
            )
            columna_resultados.controls[1].content.controls[0].controls = None
            columna_resultados.controls[3].content.controls[0].controls = None

            entrar = True
            for linea in resultado.stdout.split("\n"):
                linea = linea.strip()

                if linea.startswith("="):
                    entrar = False
                    continue

                #Detectar errores léxicos
                if linea.startswith(">") and entrar == True:
                    signo,linea,error = linea.split("|", 2)
                    columna_resultados.controls[3].content.controls[0].controls.append(
                        ft.CupertinoListTile(
                            leading=ft.Icon(name=ft.Icons.DELETE,color="red"),
                            title=ft.Text(f"Error léxico:  {error} ",selectable=True, color="red"),
                            additional_info=ft.Text(f"📌Línea: {linea}",selectable=True, color="red"),
                            bgcolor="transparent"
                        )
                    )
                #Detectar tokens
                if linea.startswith("+") and entrar == True:
                    signo, token, datos = linea.split("|", 2)
                    lexema, nombre_token = datos.rsplit("|", 1)
                    columna_resultados.controls[1].content.controls[0].controls.append(
                        ft.CupertinoListTile(
                            leading=ft.Icon(name=ft.Icons.ALBUM,color="#12b232"),
                            title=ft.Text(f"Token: {nombre_token}",selectable=True,color="white"),
                            additional_info=ft.Text(f"Lexema: {lexema} ✅ Número de Token: {token}",selectable=True,color="white"),
                            bgcolor="transparent"
                        )
                    )
                #Sintactico
                if linea.startswith("<") and entrar == False:
                    signo,resultado_sintactico_del_archivo,relleno,lineno = linea.split("|")
                    if resultado_sintactico_del_archivo == "b":
                        sintactico.value = "EL PROGRAMA NO TIENE ERRORES SINTÁCTICOS"
                        sintactico.text_style = ft.TextStyle(weight="bold", color="#12b232")
                        sintactico.border_color = "#12b232"
                    else:
                        sintactico.value = f"ERROR SINTÁCTICO     📌LÍNEA: {lineno}"
                        sintactico.text_style = ft.TextStyle(weight="bold", color="red")
                        sintactico.border_color = "red"
        except Exception as e:
            fila_de_botones.content.controls[7].visible = False
            page.open(ft.SnackBar(ft.Text(f"No se pudo ejecutar el analizador: {e}")))
            page.update()
            return

        if len(columna_resultados.controls[1].content.controls[0].controls) == 0:
            columna_resultados.controls[1].content.controls[0].controls.append(ft.Text("\n\n\n\n\n                                            No existen Tokens",size=17))

        if len(columna_resultados.controls[3].content.controls[0].controls) == 0:
            columna_resultados.controls[3].content.controls[0].controls.append(ft.Text("\n\n\n                                        No existen errores léxicos",size=17,color="#12b232"))

        fila_de_botones.content.controls[7].visible = False
        page.update()

    def borrar_resultados_de_compilacion(e):
        columna_resultados.controls[1].content.controls[0].controls = None
        columna_resultados.controls[3].content.controls[0].controls = None
        fila_de_botones.content.controls[7].visible = False

        sintactico.value = "Sin resultados"
        sintactico.text_style = ft.TextStyle(weight="bold", color="white")
        sintactico.border_color = "transparent"

        columna_resultados.controls[1].content.controls[0].controls.append(ft.Text("\n\n\n\n\n                                                 Sin resultados",size=17))
        columna_resultados.controls[3].content.controls[0].controls.append(ft.Text("\n\n\n                                                 Sin resultados",size=17))
        page.update()

    contenedor_compilador = ft.Container(content=lista_de_pestanias_codigo,bgcolor="#ffffff", expand=True, margin=0,padding=0)

    sintactico = ft.TextField(
        value="Sin resultados",
        read_only=True,
        text_align="center",
        text_style=ft.TextStyle(weight="bold",color="white",size=17),
        border_color="transparent",
        border_radius=ft.border_radius.all(1)
    )

    contenedor_sintactico = ft.Container(
        content=sintactico,
        alignment=ft.alignment.center,
        height=120,
        padding=ft.padding.only(left=10,right=10),
        bgcolor="#00172f",
        border=ft.border.only(bottom=ft.border.BorderSide(4,"#12b232"),top=ft.border.BorderSide(4,"#12b232"))
    )

    columna_resultados = ft.Column([
        ft.Row([ft.Text("RESULTADO LÉXICO",weight="bold",size=18,text_align="center", selectable=True)],alignment="center"),
        ft.Container(
            border=ft.border.only(top=ft.border.BorderSide(4,"#12b232")),
            bgcolor="#00172f",
            expand=3,
            content=ft.ListView(
                controls=[
                    ft.Column(
                        [
                            ft.Text("\n\n\n\n\n                                                 Sin resultados",size=17)
                        ],
                        scroll="auto",
                        alignment="start",
                        expand=True
                    )
                ],
                expand=True,
                spacing=0,
            )
        ),
        ft.Container(height=10),
        ft.Container(
            bgcolor="#00172f",
            expand=2,
            content=ft.ListView(
                controls=[
                    ft.Column(
                        [
                            ft.Text("\n\n\n                                                 Sin resultados",size=17)
                        ],
                        scroll="auto",
                        alignment="start",
                        expand=True
                    )
                ],
                expand=True,
                spacing=0,
            )
        ),
        ft.Divider(color="#12b232",thickness=4),
        ft.Row([ft.Text("RESULTADO SINTÁCTICO",weight="bold",size=18,text_align="center",selectable=True)],alignment="center"),
        contenedor_sintactico
    ],spacing=0)

    panel_resultados = ft.Container(
        width=600,
        content=columna_resultados,
        bgcolor="#00172f",
        border=ft.border.only(left=ft.border.BorderSide(4,"#12b232"),)
    )

    cargando_analizar = ft.ProgressRing(width=23, height=23, stroke_width=4,color="#8baf25",visible=False)

    fila_de_botones = ft.Container(
        height=60,
        bgcolor="#00172f",
        border=ft.border.only(bottom=ft.border.BorderSide(4,"#12b232"),),
        content=ft.Row([
            ft.CupertinoButton(
                content=ft.Text("Nuevo archivo",color="white"),
                opacity_on_click=0.3,
                on_click=crear_pestania_codigo,
            ),
            ft.VerticalDivider(),
            ft.CupertinoButton(
                content=ft.Text("Abrir archivo",color="white"),
                opacity_on_click=0.3,
                on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=False,
                        allowed_extensions=["txt"]  # Solo archivos .txt
                    ),
            ),
            ft.VerticalDivider(),
            ft.CupertinoButton(
                content=ft.Text("Guardar archivo",color="white"),
                opacity_on_click=0.3,
                on_click=guardar_archivo_verificar
            ),
            ft.VerticalDivider(),

            ft.ElevatedButton("ANALIZAR",icon=ft.Icons.ADS_CLICK, bgcolor="#12b232",
            style=ft.ButtonStyle(
                icon_size=25,
                text_style=ft.TextStyle(size=16,weight="bold"),
                icon_color="white",
                color="white",
                elevation={"pressed": 0, "": 1},
                animation_duration=500,
                shape=ft.RoundedRectangleBorder(radius=5),
                alignment=ft.alignment.center_left
            ), on_click=click_iniciar_analizador_sintactico_lexico),

            cargando_analizar,

            ft.ElevatedButton("BORRAR",icon=ft.Icons.CLEAR_ALL, bgcolor="#900C3F",
            style=ft.ButtonStyle(
                icon_size=25,
                text_style=ft.TextStyle(size=16,weight="bold"),
                icon_color="white",
                color="white",
                elevation={"pressed": 0, "": 1},
                animation_duration=500,
                shape=ft.RoundedRectangleBorder(radius=5),
                alignment=ft.alignment.center_left
            ), on_click=borrar_resultados_de_compilacion),
        ])
    )

    page.add(
        ft.Column([
            ft.Row([
                ft.WindowDragArea(ft.Container(content=ft.Row([ft.Image(src="icon.png",height=35),ft.Text("ANALIZADOR LÉXICO-SINTÁCTICO",weight="bold",color="#ffffff",size=25)]), bgcolor="#12b232", padding=10), expand=True),
                ft.Container(content=ft.Row([
                    ft.IconButton(
                    ft.Icons.MINIMIZE,
                    on_click=minimizar,
                    bgcolor="white",
                    style=ft.ButtonStyle(
                        color={
                            ft.ControlState.HOVERED: ft.Colors.RED,
                            ft.ControlState.FOCUSED: "#00172f",
                            ft.ControlState.DEFAULT: "#00172f"
                        }
                    ),
                    tooltip="Minimizar"
                ),
                    ft.IconButton(
                    ft.Icons.CROP_SQUARE,
                    on_click=maximizar,
                    bgcolor="white",
                    style=ft.ButtonStyle(
                        color={
                            ft.ControlState.HOVERED: ft.Colors.RED,
                            ft.ControlState.FOCUSED: "#00172f",
                            ft.ControlState.DEFAULT: "#00172f"
                        }
                    ),
                    tooltip="Maximizar"
                ),
                    ft.IconButton(
                    ft.Icons.CLOSE,
                    on_click=lambda _: page.window.close(),
                    bgcolor="white",
                    style=ft.ButtonStyle(
                        color={
                            ft.ControlState.HOVERED: ft.Colors.RED,
                            ft.ControlState.FOCUSED: "#00172f",
                            ft.ControlState.DEFAULT: "#00172f"
                        }
                    ),
                    tooltip="Cerrar"
                ),
                ],spacing=0),bgcolor="#12b232",height=56,width=125)
            ],spacing=0),

            fila_de_botones,

            ft.Row([
                contenedor_compilador,
                panel_resultados
            ],spacing=0, expand=True, vertical_alignment=ft.CrossAxisAlignment.STRETCH),

        ],expand=True,spacing=0)
    )

ft.app(main, assets_dir=str(Path(__file__).resolve().parent / "assets"))