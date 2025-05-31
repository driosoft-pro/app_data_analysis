import flet as ft


class HomePage(ft.Container):
    """
    Página de inicio
    """
    
    def __init__(self, page: ft.Page, app_state):
        super().__init__(padding=20, expand=True, alignment=ft.alignment.top_left)
        self.page = page
        self.app_state = app_state
        self.content = (
            self._build_content()
        )

    def _build_content(self):
        """
        Construye y retorna el control raíz para la vista de Inicio.
        Sigue el patrón de export_pdf_view.py para layout y responsividad.
        """
        content_column = ft.Column(
            [
                ft.Text(
                    "Bienvenido al Analizador de Datos",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Utiliza el menú de la izquierda para navegar por las funcionalidades.",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Comienza cargando un archivo CSV o XLSX desde la sección 'Cargar Archivo'.",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Luego podrás visualizar los datos, realizar búsquedas, ejecutar consultas SQL.",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=20),  # Espaciador
                ft.Image(
                    # Asumiendo que 'icon.png' está en la raíz de tu directorio 'assets'
                    # configurado en ft.app(assets_dir="assets")
                    src="icon.png",
                    width=150,
                    height=150,
                    fit=ft.ImageFit.CONTAIN,
                    error_content=ft.Text(
                        "Imagen no encontrada (icon.png)",
                        italic=True,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ),
            ],
            spacing=15,
            expand=True,  # La columna se expande para llenar el contenedor padre.
            scroll=ft.ScrollMode.ADAPTIVE,  # Scroll si el contenido excede el espacio.
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centra el contenido de la columna.
        )

        return ft.Container(
            content=content_column,
            expand=True,  # El contenedor se expande para llenar main_content_area.
            padding=0,  # El padding es manejado por main_content_area.
            alignment=ft.alignment.center,  # Centra la content_column dentro de este contenedor.
        )
