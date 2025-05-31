import flet as ft


def create_navigation_rail(
    page: ft.Page,
    on_change_view,
    on_toggle_theme,
    view_routes_by_index,  
    rail_state: ft.Ref[ft.NavigationRail],
    on_toggle_rail=None,  
):
    
    """
        Crea la barra de navegación lateral.
    """
    
    # Definición de los destinos de navegación.
    destinations = [
        ft.NavigationRailDestination(  # Índice 0: Botón de Tema
            icon=ft.Icons.DARK_MODE_OUTLINED,
            selected_icon=ft.Icons.DARK_MODE,
            label="Tema oscuro",
        ),
        ft.NavigationRailDestination(  # Índice 1: Inicio
            icon=ft.Icons.HOME_OUTLINED,
            selected_icon=ft.Icons.HOME,
            label="Inicio",
        ),
        ft.NavigationRailDestination(  # Índice 2: Buscar
            icon=ft.Icons.SEARCH_OUTLINED,
            selected_icon=ft.Icons.SEARCH,
            label="Buscar",
        ),
        ft.NavigationRailDestination(  # Índice 3: Cargar Archivo
            icon=ft.Icons.DATASET_OUTLINED,
            selected_icon=ft.Icons.DATASET,
            label="Cargar Dataset",
        ),
        ft.NavigationRailDestination(  # Índice 4: Análisis Dataset 
            icon=ft.Icons.ANALYTICS_OUTLINED,  
            selected_icon=ft.Icons.ANALYTICS,
            label="Análisis Personalizado",
        ),
        ft.NavigationRailDestination(  # Índice 5: Consultas SQL
            icon=ft.Icons.QUERY_STATS_OUTLINED,
            selected_icon=ft.Icons.QUERY_STATS,
            label="Consultas SQL",
        ),
        ft.NavigationRailDestination(  # Índice 6: Exportar PDF
            icon=ft.Icons.PICTURE_AS_PDF_OUTLINED,
            selected_icon=ft.Icons.PICTURE_AS_PDF,
            label="Exportar PDF",
        ),
        ft.NavigationRailDestination(  # Índice 7: Librería
            icon=ft.Icons.BOOK_OUTLINED,
            selected_icon=ft.Icons.BOOK,
            label="Librería",
        ),
        ft.NavigationRailDestination(  # Índice 8: Acerca De
            icon=ft.Icons.INFO_OUTLINE,
            selected_icon=ft.Icons.INFO,
            label="Acerca De",
        ),
    ]

    def handle_rail_change(e: ft.ControlEvent):
        selected_index = e.control.selected_index

        if selected_index == 0:  # Botón de Tema
            on_toggle_theme()
            # Restablecemos la selección para que no quede marcado visualmente
            e.control.selected_index = None
        elif selected_index is not None and selected_index > 0:
            # Cambia la vista según el Índice seleccionado
            route_to_load = view_routes_by_index[selected_index - 1]
            on_change_view(route_to_load)
        else:
            print(f"Índice de navegación fuera de rango o nulo: {selected_index}")

        # Es importante que el rail se actualice después de un cambio
        e.control.page.update()

    rail_control = ft.NavigationRail(
        selected_index=None,  # Inicia sin selección visual
        label_type=ft.NavigationRailLabelType.ALL,  # Mostrar todas las etiquetas por defecto
        min_width=50,
        min_extended_width=200,
        extended=True,  # Inicia extendido
        group_alignment=-0.9,  # Alineación superior
        destinations=destinations,
        on_change=handle_rail_change,
    )

    rail_state.current = rail_control  # Asigna el control al Ref
    return rail_control
