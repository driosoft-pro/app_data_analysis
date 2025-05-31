import flet as ft
import webbrowser


class AboutPage(ft.Container):  
    """Página de Acerca de"""
    
    def __init__(self, page: ft.Page, app_state):
        super().__init__(padding=20, expand=True, alignment=ft.alignment.top_left)
        self.page = page
        self.app_state = app_state
        self.content = (
            self._build_content()
        )  

    def _build_content(self):  # Renombrado de build a _build_content
        """
        Construye y retorna el control raíz para la vista "Acerca De".
        """
        about_content = [
            ft.Text("Acerca De", size=24, weight=ft.FontWeight.BOLD),
            ft.Text(
                "MugenC-Data",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.PRIMARY,
            ),
            ft.Text("Versión: 1.0.0 (En Desarrollo)", selectable=True),
            ft.Text("Desarrollado por: Driosoft-Pro", selectable=True),
            ft.TextButton(
                text="Visita el Repositorio en GitHub",
                on_click=lambda e: webbrowser.open(
                    "https://github.com/driosoft-pro/data_analysis.git"
                ),
            ),
            ft.Divider(height=15, thickness=1, color=ft.Colors.OUTLINE_VARIANT),
            ft.Text("Propósito", weight=ft.FontWeight.BOLD, size=16),
            ft.Text(
                "Esta aplicación tiene como objetivo proporcionar una herramienta intuitiva y eficiente "
                "para la carga, visualización preliminar y análisis básico de conjuntos de datos, "
                "facilitando la exploración inicial y la extracción de insights.",
                selectable=True,
            ),
            ft.Container(height=10),
            ft.Text("Tecnologías Clave", weight=ft.FontWeight.BOLD, size=16),
            ft.Text(
                "Construida con Python y Flet, aprovechando la simplicidad y rapidez de Flet "
                "para crear interfaces de usuario web y de escritorio interactivas.",
                selectable=True,
            ),
            ft.Container(height=10),
            ft.Text(
                "Estado Actual y Próximos Pasos", weight=ft.FontWeight.BOLD, size=16
            ),
            ft.Text(
                "Actualmente, la aplicación cuenta con la estructura básica de navegación, carga de archivos simulada "
                "y vistas preliminares. Los próximos pasos incluyen la implementación completa de la lógica de "
                "procesamiento de archivos (XLSX/CSV), la integración con DuckDB para consultas SQL, "
                "y la adición de funcionalidades de análisis y visualización de datos más avanzadas.",
                selectable=True,
            ),
            ft.Container(height=10),
            ft.Text("Contribuciones y Licencia", weight=ft.FontWeight.BOLD, size=16),
            ft.Text(
                "Las contribuciones al proyecto son bienvenidas. Por favor, consulta el repositorio en GitHub "
                "para más detalles sobre cómo contribuir. El proyecto se distribuye bajo la licencia "
                "(especificar tu licencia, ej: MIT License).",  # Especifica tu licencia
                selectable=True,
            ),
            ft.Container(height=10),
            ft.Text("Agradecimientos", weight=ft.FontWeight.BOLD, size=16),
            ft.Text(
                "Un agradecimiento especial a la comunidad de Flet y a todos los desarrolladores de las "
                "librerías de código abierto que hacen posible este proyecto.",
                selectable=True,
            ),
        ]

        content_column = ft.Column(
            controls=about_content,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )

        return content_column
