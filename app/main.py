import flet as ft
import sys
import os

# Añadir el directorio raíz del proyecto al sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(
    os.path.join(current_dir, "..")
)  
sys.path.insert(0, project_root)

from views.bar_navigation import create_navigation_rail
from views.home_view import HomePage
from views.file_upload_view import FileUploadPage
from views.data_display_view import DataDisplayPage
from views.query_view import QueryPage
from views.library_view import LibraryPage
from views.about_view import AboutPage
from views.export_pdf_view import ExportPDFPage
from views.search_view import SearchPage

# Importar las clases de la capa core
from core.data_loader import DataLoader
from core.data_analyzer import DataAnalyzer
from core.query_engine import QueryEngine
from core.plot_generator import PlotGenerator

from constants import (
    VIEW_HOME,
    VIEW_UPLOAD,
    VIEW_DISPLAY,
    VIEW_QUERY,
    VIEW_EXPORT,
    VIEW_LIBRARY,
    VIEW_ABOUT,
    VIEW_SEARCH,
)


class AppState:
    """
    Una clase simple para manejar el estado compartido de la aplicación.
    Almacena el DataFrame cargado y el nombre del archivo.
    """

    def __init__(self):
        self.df = None  # Aquí se almacenará el DataFrame de Pandas
        self.loaded_file_name = None  # Para almacenar el nombre del archivo cargado
        self.current_theme = ft.ThemeMode.LIGHT  # Tema actual

    def load_dataframe(self, dataframe, file_name=None):
        """Carga el DataFrame y el nombre del archivo en el estado."""
        self.df = dataframe
        self.loaded_file_name = file_name
        print(
            f"AppState: DataFrame cargado desde {file_name if file_name else 'memoria'}"
        )

    def get_dataframe(self):
        """Retorna el DataFrame cargado."""
        return self.df

    def get_loaded_file_name(self):
        """Retorna el nombre del archivo cargado."""
        return self.loaded_file_name

    def toggle_theme(self):
        """Alterna entre tema claro y oscuro."""
        self.current_theme = (
            ft.ThemeMode.LIGHT
            if self.current_theme == ft.ThemeMode.DARK
            else ft.ThemeMode.DARK
        )
        return self.current_theme


def main(page: ft.Page):
    # Configuración inicial de la página
    page.title = "Data Análisis App - MugenC-Data"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = ft.padding.only(left=10)

    # Estado de la aplicación
    app_state = AppState()

    # Instancias de las clases de la capa core
    data_loader = DataLoader()
    data_analyzer = DataAnalyzer()
    query_engine = QueryEngine()
    plot_generator = PlotGenerator()

    # Referencia al NavigationRail
    navigation_rail_ref = ft.Ref[ft.NavigationRail]()

    # Área de contenido principal
    main_content_area = ft.Container(
        content=ft.Text("Selecciona una opción del menú"),
        padding=ft.padding.symmetric(horizontal=20),
        alignment=ft.alignment.top_left,
        expand=True,
    )

    # Rutas de vista (ordenadas para coincidir con NavigationRail)
    # El orden aquí DEBE coincidir con el orden de los destinos en bar_navigation.py
    # (después del botón de tema, que es el índice 0 del rail)
    view_routes_by_index = [
        VIEW_HOME,  # Corresponde a rail_index 1
        VIEW_SEARCH,  # Corresponde a rail_index 2
        VIEW_UPLOAD,  # Corresponde a rail_index 3
        VIEW_DISPLAY,  # Corresponde a rail_index 4
        VIEW_QUERY,  # Corresponde a rail_index 5
        VIEW_EXPORT,  # Corresponde a rail_index 6
        VIEW_LIBRARY,  # Corresponde a rail_index 7
        VIEW_ABOUT,  # Corresponde a rail_index 8
    ]

    # Instancias de las vistas, pasando app_state y las clases de core/
    # Es crucial pasar las instancias de core a las vistas que las usarán
    home_page = HomePage(page, app_state)
    file_upload_page = FileUploadPage(page, app_state, data_loader=data_loader)
    data_display_page = DataDisplayPage(
        page, app_state, data_analyzer=data_analyzer, plot_generator=plot_generator
    )
    query_page = QueryPage(page, app_state, query_engine=query_engine)
    library_page = LibraryPage(page, app_state)
    about_page = AboutPage(page, app_state)
    export_pdf_page = ExportPDFPage(page, app_state)
    search_page = SearchPage(page, app_state)

    # Función para cambiar de vista
    def change_view(selected_route):
        nonlocal main_content_area
        print(f"Cambiando vista a: {selected_route}")

        # Asigna la instancia de la vista directamente, ya que ahora son ft.Container
        # Esto es clave: NO LLAMAR A .build() aquí.
        if selected_route == VIEW_HOME:
            main_content_area.content = home_page
        elif selected_route == VIEW_UPLOAD:
            main_content_area.content = file_upload_page
        elif selected_route == VIEW_DISPLAY:
            main_content_area.content = data_display_page
        elif selected_route == VIEW_QUERY:
            main_content_area.content = query_page
        elif selected_route == VIEW_LIBRARY:
            main_content_area.content = library_page
        elif selected_route == VIEW_ABOUT:
            main_content_area.content = about_page
        elif selected_route == VIEW_EXPORT:
            main_content_area.content = export_pdf_page
        elif selected_route == VIEW_SEARCH:
            main_content_area.content = search_page
        else:
            main_content_area.content = ft.Text(
                f"Error: Vista no encontrada para la ruta '{selected_route}'"
            )

        page.update()

    # Funciones para el tema
    def toggle_theme():
        page.theme_mode = app_state.toggle_theme()
        update_theme_icon()
        page.update()

    def update_theme_icon():
        if navigation_rail_ref.current:
            destinations = navigation_rail_ref.current.destinations
            if destinations and len(destinations) > 0:
                # El primer destino es el botón de tema
                if page.theme_mode == ft.ThemeMode.DARK:
                    destinations[0].icon = ft.Icons.LIGHT_MODE_OUTLINED
                    destinations[0].selected_icon = ft.Icons.LIGHT_MODE
                    destinations[0].label = "Tema claro"
                else:
                    destinations[0].icon = ft.Icons.DARK_MODE_OUTLINED
                    destinations[0].selected_icon = ft.Icons.DARK_MODE
                    destinations[0].label = "Tema oscuro"
                page.update()  # Asegurarse de que el icono se actualice

    # Función para alternar la barra de navegación
    def toggle_navigation_rail(e):
        current_rail = navigation_rail_ref.current
        if current_rail:
            current_rail.extended = not current_rail.extended
            current_rail.label_type = (
                ft.NavigationRailLabelType.ALL
                if current_rail.extended
                else ft.NavigationRailLabelType.NONE
            )
            app_title_text.visible = current_rail.extended
            page.update()

    # Crear barra de navegación
    create_navigation_rail(
        page=page,
        on_change_view=change_view,
        on_toggle_theme=toggle_theme,
        view_routes_by_index=view_routes_by_index,
        rail_state=navigation_rail_ref,
    )

    # Título de la aplicación
    app_title_text = ft.Text("Data Análisis", weight=ft.FontWeight.BOLD, size=18)

    # Layout principal
    main_layout = ft.Column(
        [
            # Barra superior
            ft.Row(
                [
                    ft.IconButton(
                        ft.Icons.MENU,
                        on_click=toggle_navigation_rail,
                        tooltip="Alternar barra de navegación",
                    ),
                    app_title_text,
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Divider(height=1, color=ft.Colors.BLACK26),
            # Contenido principal
            ft.Row(
                [
                    (
                        navigation_rail_ref.current
                        if navigation_rail_ref.current
                        else ft.Container()
                    ),
                    ft.VerticalDivider(width=1),
                    main_content_area,
                ],
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            ),
        ],
        expand=True,
    )

    # Añadir layout a la página
    page.add(main_layout)

    # Configuración inicial
    if navigation_rail_ref.current:
        # El índice 1 corresponde a "Inicio" si el botón de tema es el índice 0
        navigation_rail_ref.current.selected_index = 1
        change_view(VIEW_HOME)
        update_theme_icon()


if __name__ == "__main__":
    # ft.app(target=main, assets_dir="assets")    # Para ejecutar en modo desktop
    ft.app(
        target=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER
    )  # Para ejecutar en modo web
