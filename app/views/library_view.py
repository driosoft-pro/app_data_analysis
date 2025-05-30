import flet as ft


class LibraryPage(ft.Container):  # Hereda de ft.Container
    """
    Vista para mostrar información sobre la "Biblioteca" o librerías usadas.
    """

    def __init__(self, page: ft.Page, app_state):
        super().__init__(padding=20, expand=True, alignment=ft.alignment.top_left)
        self.page = page
        self.app_state = app_state
        self.content = (
            self._build_content()
        )  # Establece el contenido inicial del contenedor

    def _build_content(self):  # Renombrado de build a _build_content
        """
        Construye y retorna el control raíz para la vista de Biblioteca.
        """
        libraries_info = [
            ("Python", "El lenguaje de programación que impulsa toda la aplicación."),
            ("Flet", "Framework para construir interfaces de usuario interactivas."),
            ("Flet-desktop", "Soporte para empaquetar como aplicación de escritorio."),
            ("Flet-webview", "Integración con WebView (si se usa)."),
            ("Flet-core", "Core de flet."),
            ("Pandas", "Para manipulación y análisis de datos."),
            ("DuckDB", "Para consultas SQL sobre DataFrames."),
            ("ReportLab", "Para generación de PDFs."),
            ("NumPy", "Para cálculos numéricos avanzados."),
            ("Matplotlib", "Para visualización de datos."),
            ("Seaborn", "Para visualización estadística."),
            ("scipy", "Para cálculos numéricos avanzados."),
            ("tabulate", "Para tablas en formato texto (para consola, si se desea)."),
            ("black", "Formateador automático."),
            ("flake8", "Verificación de estilo de código."),
            ("isort", "Ordenamiento automático de imports."),
            ("pytest", "Testing unitario y de integración."),
            ("PyInstaller", "Para crear ejecutables de escritorio."),
            ("ReportLab", "Para generación de PDFs."),
            ("openpyxl", "Para leer y escribir archivos Excel."),
            ("xlrd", "Para leer archivos Excel (antiguos)."),
            ("time", "Para medir tiempos."),
        ]

        library_controls = []
        for lib_name, lib_desc in libraries_info:
            library_controls.append(
                ft.Text(lib_name, weight=ft.FontWeight.BOLD, size=16)
            )
            library_controls.append(ft.Text(lib_desc, selectable=True))
            library_controls.append(
                ft.Divider(height=5, thickness=0.5, color=ft.Colors.OUTLINE_VARIANT)
            )

        content_column = ft.Column(
            [
                ft.Text("Librerías y Tecnologías", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Esta aplicación se construye sobre el poder de Python y el ecosistema de código abierto. "
                    "Algunas de las tecnologías clave incluyen:",
                    selectable=True,
                    color=ft.Colors.ON_SURFACE_VARIANT,
                ),
                ft.Divider(height=15, thickness=1, color=ft.Colors.OUTLINE_VARIANT),
                *library_controls,
                ft.Container(height=10),
                ft.Text("Nota:", weight=ft.FontWeight.BOLD, size=18),
                ft.Text(
                    "Este listado de librerías puede variar segun la version de la aplicación. ",
                    selectable=True,
                    color=ft.Colors.ON_SURFACE_VARIANT,
                ),
            ],
            spacing=10,
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )

        return content_column  # Retorna la columna directamente
