import flet as ft
from core.data_loader import DataLoader
from .file_upload_confg import FileUploadConfig


class FileUploadPage(ft.Container):
    """
    Vista mejorada para cargar y validar archivos de datos.
    """
    def __init__(self, page: ft.Page, app_state, data_loader: DataLoader):
        super().__init__(
            padding=20,
            expand=True,
            alignment=ft.alignment.top_left
        )
        self.page = page
        self.app_state = app_state
        self.data_loader = data_loader

        # Elementos UI (instantiated here)
        self.file_path_text = ft.Text("Ningún archivo seleccionado.", size=14)
        self.upload_status_text = ft.Text("", size=14, color=ft.Colors.GREY_600)
        self.progress_bar = ft.ProgressBar(width=400, visible=False)
        self.loading_indicator = ft.Row(
            [ft.ProgressRing(width=20, height=20, visible=False),
             ft.Text("Procesando...")],
            visible=False
        )

        # FilePicker (instantiated here)
        # Note: on_result will be set by the config class, but we need to pass a reference
        self.file_picker = ft.FilePicker() # Initialize without on_result here
        self.page.overlay.append(self.file_picker)

        # Area de resultados para VALIDACIÓN del Dataset ORIGINAL
        self.validation_results = ft.Column(
            [ft.Text("Resultados de Validación del Dataset Original:", weight=ft.FontWeight.BOLD)],
            scroll=ft.ScrollMode.ALWAYS,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

        # Area de resultados para MANIPULACIÓN (Copia, Duplicados, Tipos Objeto, Manejo Nulos, Renombrar Columnas)
        self.manipulation_results = ft.Column(
            [ft.Text("Resultados de Manipulación de Datos Básicos:", weight=ft.FontWeight.BOLD)], # RENOMBRADO AQUÍ
            scroll=ft.ScrollMode.ALWAYS,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

        # Area de resultados para VALIDACIÓN del Dataset MANIPULADO (la copia)
        self.manipulated_validation_results = ft.Column(
            [ft.Text("Resultados de Validación del Dataset Manipulado:", weight=ft.FontWeight.BOLD)],
            scroll=ft.ScrollMode.ALWAYS,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

        # Dropdowns para conversión de tipo (inicialmente ocultos)
        self.object_type_conversion_controls = ft.Column(visible=False)

        # Controles para el manejo de nulos (inicialmente ocultos)
        self.null_handling_controls = ft.Column(visible=False)
        self.null_handling_column_dropdown = ft.Dropdown(
            label="Seleccionar Columna",
            hint_text="Todas las columnas",
            options=[ft.dropdown.Option("Todas las columnas")],
            expand=True
        )
        self.null_handling_strategy_dropdown = ft.Dropdown(
            label="Estrategia de Manejo de Nulos",
            options=[
                ft.dropdown.Option("Reemplazar '?' con NaN"),
                ft.dropdown.Option("Rellenar con Media (Numérico)"),
                ft.dropdown.Option("Rellenar con Mediana (Numérico)"),
                ft.dropdown.Option("Rellenar con Moda (Numérico/Categórico)"),
                ft.dropdown.Option("Eliminar Filas (Cualquier nulo)"),
                ft.dropdown.Option("Eliminar Filas (Todos los nulos)"),
            ],
            expand=True
        )

        # Controles para renombrar columnas (inicialmente ocultos)
        self.rename_column_controls = ft.Column(visible=False)
        self.rename_column_dropdown = ft.Dropdown(
            label="Seleccionar Columna a Renombrar",
            hint_text="Seleccione una columna",
            options=[],
            expand=True
        )
        self.new_column_name_textfield = ft.TextField(
            label="Nuevo Nombre de Columna",
            hint_text="Ingrese el nuevo nombre",
            expand=True
        )

        # Instantiate the FileUploadConfig and pass UI elements
        self.config = FileUploadConfig(
            page=self.page,
            app_state=self.app_state,
            file_picker=self.file_picker,
            upload_status_text=self.upload_status_text,
            file_path_text=self.file_path_text,
            progress_bar=self.progress_bar,
            loading_indicator=self.loading_indicator,
            validation_results=self.validation_results,
            manipulation_results=self.manipulation_results,
            manipulated_validation_results=self.manipulated_validation_results,
            object_type_conversion_controls=self.object_type_conversion_controls,
            null_handling_controls=self.null_handling_controls,
            null_handling_column_dropdown=self.null_handling_column_dropdown,
            null_handling_strategy_dropdown=self.null_handling_strategy_dropdown,
            rename_column_controls=self.rename_column_controls,
            rename_column_dropdown=self.rename_column_dropdown,
            new_column_name_textfield=self.new_column_name_textfield
        )
        # Set the file_picker's on_result handler to the one in config
        self.file_picker.on_result = self.config.handle_file_picker_result

        # Botón principal
        self.select_button = ft.ElevatedButton(
            "Seleccionar Archivo",
            icon=ft.Icons.UPLOAD_FILE,
            on_click=lambda _: self.file_picker.pick_files(
                allowed_extensions=["xlsx", "csv"],
                dialog_title="Seleccione un archivo de datos"
            ),
        )

        # Botones de validación inicial (para el dataset original)
        self.validation_buttons = ft.ResponsiveRow([
            ft.ElevatedButton(
                "Cantidad Datos",
                on_click=lambda _: self.config.show_data_info("shape"),
                icon=ft.Icons.TABLE_CHART,
                tooltip="Muestra filas y columnas",
                col={"sm": 12, "md": 6, "lg": 2}
            ),
            ft.ElevatedButton(
                "Tipos de datos",
                on_click=lambda _: self.config.show_data_info("dtypes"),
                icon=ft.Icons.DATA_ARRAY,
                tooltip="Muestra tipos de datos",
                col={"sm": 12, "md": 6, "lg": 2}
            ),
            ft.ElevatedButton(
                "Nombres Columnas",
                on_click=lambda _: self.config.show_data_info("column_names"),
                icon=ft.Icons.VIEW_COLUMN,
                tooltip="Muestra los nombres de todas las columnas",
                col={"sm": 12, "md": 6, "lg": 2}
            ),
            ft.ElevatedButton(
                "Valores Duplicados",
                on_click=lambda _: self.config._show_duplicates("original"),
                icon=ft.Icons.FILTER_1,
                tooltip="Muestra filas duplicadas",
                col={"sm": 12, "md": 6, "lg": 2}
            ),
            ft.ElevatedButton(
                "Valores nulos",
                on_click=lambda _: self.config.show_data_info("nulls"),
                icon=ft.Icons.WARNING_AMBER,
                tooltip="Muestra valores faltantes",
                col={"sm": 12, "md": 6, "lg": 2}
            ),
            ft.ElevatedButton(
                "Nulos %",
                on_click=lambda _: self.config.show_data_info("nulls_percent"),
                icon=ft.Icons.PERCENT,
                tooltip="Porcentaje de valores nulos",
                col={"sm": 12, "md": 6, "lg": 2}
            ),
            ft.ElevatedButton(
                "Ver Tabla Original",
                on_click=lambda _: self.config._show_dataframe_table("original"),
                icon=ft.Icons.GRID_ON,
                tooltip="Muestra una vista previa del DataFrame original",
                col={"sm": 12, "md": 6, "lg": 2}
            ),
            ft.ElevatedButton(
                "Resumen",
                on_click=lambda _: self.config.show_data_info("info"),
                icon=ft.Icons.INFO_OUTLINE,
                tooltip="Información completa del DataFrame",
                col={"sm": 12, "md": 6, "lg": 2}
            ),            
            ft.ElevatedButton(
                "limpiar",
                on_click=lambda _: self.config._clear_results(),
                icon=ft.Icons.CLEANING_SERVICES,
                tooltip="Limpiar todos los resultados",
                col={"sm": 12, "md": 6, "lg": 2}
            )
        ], spacing=10)

        # Botones de Manipulación y Limpieza de Datos
        self.data_manipulation_buttons = ft.ResponsiveRow([
            ft.ElevatedButton(
                "Crear Copia Dataset",
                on_click=self.config._create_dataframe_copy,
                icon=ft.Icons.COPY,
                tooltip="Crea una copia del DataFrame actual para manipulación",
                col={"sm": 12, "md": 6, "lg": 2}
            ),
            ft.ElevatedButton(
                "Eliminar Duplicados",
                on_click=lambda _: self.config._delete_duplicates(),
                icon=ft.Icons.DELETE_SWEEP,
                tooltip="Elimina filas duplicadas del DataFrame copiado",
                col={"sm": 12, "md": 6, "lg": 2}
            ),
            ft.ElevatedButton(
                "Modificar Tipos Object",
                on_click=lambda _: self.config._show_object_column_types(),
                icon=ft.Icons.FORMAT_COLOR_TEXT,
                tooltip="Analiza columnas de tipo 'object' y sugiere conversiones",
                col={"sm": 12, "md": 6, "lg": 2}
            ),
            ft.ElevatedButton(
                "Corregir Nulos",
                on_click=self.config._show_null_handling_options,
                icon=ft.Icons.DELETE_OUTLINE,
                tooltip="Opciones para rellenar o eliminar valores nulos",
                col={"sm": 12, "md": 6, "lg": 2}
            ),
            # Nuevo botón para modificar nombres de columnas
            ft.ElevatedButton(
                "Modificar Nombres Columnas",
                on_click=self.config._show_rename_column_options,
                icon=ft.Icons.EDIT,
                tooltip="Permite renombrar una columna del DataFrame copiado",
                col={"sm": 12, "md": 6, "lg": 2}
            ),
        ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER)

        # Botones de validación para la copia del dataset
        self.copied_data_validation_buttons = ft.ResponsiveRow([
            ft.ElevatedButton(
                "Cantidad Datos",
                on_click=lambda _: self.config.show_manipulated_data_info("shape"),
                icon=ft.Icons.TABLE_CHART,
                tooltip="Muestra filas y columnas de la copia",
                col={"sm": 12, "md": 6, "lg": 2}
            ),
            ft.ElevatedButton(
                "Tipos de datos",
                on_click=lambda _: self.config.show_manipulated_data_info("dtypes"),
                icon=ft.Icons.DATA_ARRAY,
                tooltip="Muestra tipos de datos de la copia",
                col={"sm": 12, "md": 6, "lg": 2}
            ),
            ft.ElevatedButton(
                "Nombres Columnas",
                on_click=lambda _: self.config.show_manipulated_data_info("column_names"),
                icon=ft.Icons.VIEW_COLUMN,
                tooltip="Muestra los nombres de todas las columnas de la copia",
                col={"sm": 12, "md": 6, "lg": 2}
            ),
            ft.ElevatedButton(
                "Valores nulos",
                on_click=lambda _: self.config.show_manipulated_data_info("nulls"),
                icon=ft.Icons.WARNING_AMBER,
                tooltip="Muestra valores faltantes de la copia",
                col={"sm": 12, "md": 6, "lg": 2}
            ),
            ft.ElevatedButton(
                "Nulos %",
                on_click=lambda _: self.config.show_manipulated_data_info("nulls_percent"),
                icon=ft.Icons.PERCENT,
                tooltip="Porcentaje de valores nulos de la copia",
                col={"sm": 12, "md": 6, "lg": 2}
            ),
            ft.ElevatedButton(
                "Ver Tabla Manipulada",
                on_click=lambda _: self.config._show_dataframe_table("manipulated"),
                icon=ft.Icons.GRID_ON,
                tooltip="Muestra una vista previa del DataFrame manipulado",
                col={"sm": 12, "md": 6, "lg": 2}
            ),
            ft.ElevatedButton(
                "Resumen",
                on_click=lambda _: self.config.show_manipulated_data_info("info"),
                icon=ft.Icons.INFO_OUTLINE,
                tooltip="Información completa de la copia del DataFrame",
                col={"sm": 12, "md": 6, "lg": 2}
            ),            
        ], spacing=10)

        # Build `null_handling_controls` using self.config methods
        self.null_handling_controls.controls.extend([
            ft.Text("Opciones de Manejo de Nulos:", weight=ft.FontWeight.BOLD),
            ft.Row([self.null_handling_column_dropdown, self.null_handling_strategy_dropdown]),
            ft.ElevatedButton("Aplicar Manejo de Nulos", on_click=self.config._apply_null_handling),
            ft.ElevatedButton("Cerrar Opciones de Nulos", on_click=self.config._hide_null_handling_options)
        ])

        # Build `rename_column_controls` using self.config methods
        self.rename_column_controls.controls.extend([
            ft.Text("Renombrar Columna:", weight=ft.FontWeight.BOLD),
            ft.Row([self.rename_column_dropdown]),
            ft.Row([self.new_column_name_textfield]),
            ft.ElevatedButton("Aplicar Renombre", on_click=self.config._apply_rename_column),
            ft.ElevatedButton("Cerrar Opciones de Renombre", on_click=self.config._hide_rename_column_options)
        ])

        # Construir interfaz
        self.content = self._build_content()

    def _build_content(self):
        """Construye la interfaz de la vista."""
        return ft.Column(
            [
                ft.Text("Cargar Archivo de Datos", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Formatos soportados: XLSX (Excel) y CSV", size=14, color=ft.Colors.GREY_600),
                ft.Divider(height=20),

                # Sección de carga
                ft.Row([self.select_button, self.loading_indicator], spacing=10),
                self.progress_bar,
                self.file_path_text,

                ft.Divider(height=20),

                # Sección de validación de datos originales
                ft.Text("Validación de Datos Originales", size=18, weight=ft.FontWeight.BOLD),
                self.upload_status_text,
                self.validation_buttons,

                ft.Container( # Contenedor para resultados de validación ORIGINAL
                    self.validation_results,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=5,
                    padding=10,
                    expand=True,
                    height=300 
                ),

                ft.Divider(height=20),

                # Sección de Manipulación de Datos Básicos
                ft.Text("Manipulación y Limpieza de Datos Básicos", size=18, weight=ft.FontWeight.BOLD), # RENOMBRADO AQUÍ
                self.data_manipulation_buttons,
                self.object_type_conversion_controls, # Controles de conversión de tipo
                self.null_handling_controls, # Controles de manejo de nulos
                self.rename_column_controls, # Controles de renombrado de columna

                ft.Container( # Contenedor para resultados de manipulación
                    self.manipulation_results,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=5,
                    padding=10,
                    expand=True,
                    height=300
                ),

                ft.Divider(height=20),

                # Sección de Validación de Datos Manipulados (Copia del Dataset)
                ft.Text("Validación de Datos Manipulados (Copia del Dataset)", size=18, weight=ft.FontWeight.BOLD),
                self.copied_data_validation_buttons,

                ft.Container( # Contenedor para resultados de validación MANIPULADA
                    self.manipulated_validation_results,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=5,
                    padding=10,
                    expand=True,
                    height=300
                ),

                ft.Divider(height=20),
                # bloque para exportación
                #ft.Text("Exportar Dataset Manipulado", size=18, weight=ft.FontWeight.BOLD),
                #ft.ResponsiveRow([
                #    ft.ElevatedButton(
                #        "Exportar CSV",
                #        on_click=self.config._export_dataframe_csv,
                #        icon=ft.Icons.SAVE,
                #        tooltip="Exporta el DataFrame manipulado como CSV",
                #        col={"sm": 12, "md": 6, "lg": 2}
                #    ),
                #], spacing=10),

                #ft.Divider(height=20),
            ],
            spacing=10,
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,
        )