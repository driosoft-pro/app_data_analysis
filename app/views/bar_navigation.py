import flet as ft
from constants import ( # Asegúrate de que estas constantes estén disponibles
    VIEW_HOME,
    VIEW_UPLOAD,
    VIEW_DISPLAY,
    VIEW_QUERY,
    VIEW_EXPORT,
    VIEW_LIBRARY,
    VIEW_ABOUT,
    VIEW_SEARCH,
)

def create_navigation_rail(
    page: ft.Page,
    on_change_view,
    on_toggle_theme,
    view_routes_by_index, # Esta lista debe coincidir con el orden de los destinos de vista
    rail_state: ft.Ref[ft.NavigationRail],
    on_toggle_rail=None # Este parámetro no se usa en la función, se puede eliminar si no es necesario
):
    # Definición de los destinos de navegación.
    # El orden aquí DEBE coincidir con el orden en view_routes_by_index (después del botón de tema).
    destinations = [
        ft.NavigationRailDestination( # Índice 0: Botón de Tema
            icon=ft.Icons.DARK_MODE_OUTLINED,
            selected_icon=ft.Icons.DARK_MODE,
            label="Tema oscuro",
        ),
        ft.NavigationRailDestination( # Índice 1: Inicio
            icon=ft.Icons.HOME_OUTLINED,
            selected_icon=ft.Icons.HOME,
            label="Inicio",
        ),
        ft.NavigationRailDestination( # Índice 2: Buscar
            icon=ft.Icons.SEARCH_OUTLINED,
            selected_icon=ft.Icons.SEARCH,
            label="Buscar",
        ),
        ft.NavigationRailDestination( # Índice 3: Cargar Archivo
            icon=ft.Icons.FOLDER_OPEN_OUTLINED,
            selected_icon=ft.Icons.FOLDER_OPEN,
            label="Cargar Archivo",
        ),
        ft.NavigationRailDestination( # Índice 4: Análisis Dataset (VIEW_DISPLAY)
            icon=ft.Icons.ANALYTICS_OUTLINED, # Icono sugerido para análisis
            selected_icon=ft.Icons.ANALYTICS,
            label="Análisis Dataset",
        ),
        ft.NavigationRailDestination( # Índice 5: Consultas SQL (VIEW_QUERY)
            icon=ft.Icons.QUERY_STATS_OUTLINED, # Icono sugerido para consultas
            selected_icon=ft.Icons.QUERY_STATS,
            label="Consultas SQL",
        ),
        ft.NavigationRailDestination( # Índice 6: Exportar PDF
            icon=ft.Icons.PICTURE_AS_PDF_OUTLINED,
            selected_icon=ft.Icons.PICTURE_AS_PDF,
            label="Exportar PDF",
        ),
        ft.NavigationRailDestination( # Índice 7: Librería
            icon=ft.Icons.BOOK_OUTLINED,
            selected_icon=ft.Icons.BOOK,
            label="Librería",
        ),
        ft.NavigationRailDestination( # Índice 8: Acerca De
            icon=ft.Icons.INFO_OUTLINE,
            selected_icon=ft.Icons.INFO,
            label="Acerca De",
        ),
    ]

    def handle_rail_change(e: ft.ControlEvent):
        selected_index = e.control.selected_index

        if selected_index == 0: # Botón de Tema
            on_toggle_theme()
            # Restablecemos la selección para que no quede marcado visualmente
            e.control.selected_index = None
        elif selected_index is not None and selected_index > 0:
            # Ajustamos el índice porque el primer elemento (índice 0) es el botón de tema.
            # Los destinos de vista reales comienzan en el índice 1 del rail,
            # que corresponde al índice 0 de view_routes_by_index.
            route_to_load = view_routes_by_index[selected_index - 1]
            on_change_view(route_to_load)
        else:
            print(f"Índice de navegación fuera de rango o nulo: {selected_index}")

        # Es importante que el rail se actualice después de un cambio
        e.control.page.update()


    rail_control = ft.NavigationRail(
        selected_index=None, # Inicia sin selección visual
        label_type=ft.NavigationRailLabelType.ALL, # Mostrar todas las etiquetas por defecto
        min_width=50,
        min_extended_width=200,
        extended=True, # Inicia extendido
        group_alignment=-0.9, # Alineación superior
        destinations=destinations,
        on_change=handle_rail_change,
    )

    rail_state.current = rail_control # Asigna el control al Ref
    return rail_control
