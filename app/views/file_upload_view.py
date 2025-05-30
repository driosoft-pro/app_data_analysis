import io
import flet as ft
from core.data_loader import DataLoader


class FileUploadPage(ft.Container):
    """
    Vista mejorada para cargar y validar archivos de datos.
    """

    def __init__(self, page: ft.Page, app_state, data_loader: DataLoader):
        super().__init__(padding=20, expand=True, alignment=ft.alignment.top_left)
        self.page = page
        self.app_state = app_state
        self.data_loader = data_loader

        # Elementos UI
        self.file_path_text = ft.Text("Ningún archivo seleccionado.", size=14)
        self.upload_status_text = ft.Text("", size=14, color=ft.Colors.GREY_600)
        self.progress_bar = ft.ProgressBar(width=400, visible=False)
        self.loading_indicator = ft.Row(
            [
                ft.ProgressRing(width=20, height=20, visible=False),
                ft.Text("Procesando..."),
            ],
            visible=False,
        )

        # FilePicker
        self.file_picker = ft.FilePicker(on_result=self.handle_file_picker_result)
        self.page.overlay.append(self.file_picker)

        # Botón principal
        self.select_button = ft.ElevatedButton(
            "Seleccionar Archivo",
            icon=ft.Icons.UPLOAD_FILE,
            on_click=lambda _: self.file_picker.pick_files(
                allowed_extensions=["xlsx", "csv"],
                dialog_title="Seleccione un archivo de datos",
            ),
        )

        # Botones de validación avanzada
        self.validation_buttons = ft.ResponsiveRow(
            [
                ft.ElevatedButton(
                    "Cantidad Datos",
                    on_click=lambda _: self.show_data_info("shape"),
                    icon=ft.Icons.TABLE_CHART,
                    tooltip="Muestra filas y columnas",
                    col={"sm": 12, "md": 6, "lg": 2},
                ),
                ft.ElevatedButton(
                    "Tipos de datos",
                    on_click=lambda _: self.show_data_info("dtypes"),
                    icon=ft.Icons.DATA_ARRAY,
                    tooltip="Muestra tipos de datos",
                    col={"sm": 12, "md": 6, "lg": 2},
                ),
                ft.ElevatedButton(
                    "Valores nulos",
                    on_click=lambda _: self.show_data_info("nulls"),
                    icon=ft.Icons.WARNING_AMBER,
                    tooltip="Muestra valores faltantes",
                    col={"sm": 12, "md": 6, "lg": 2},
                ),
                ft.ElevatedButton(
                    "Nulos",
                    on_click=lambda _: self.show_data_info("nulls_percent"),
                    icon=ft.Icons.PERCENT,
                    tooltip="Porcentaje de valores nulos",
                    col={"sm": 12, "md": 6, "lg": 2},
                ),
                ft.ElevatedButton(
                    "Resumen",
                    on_click=lambda _: self.show_data_info("info"),
                    icon=ft.Icons.INFO_OUTLINE,
                    tooltip="Información completa del DataFrame",
                    col={"sm": 12, "md": 6, "lg": 2},
                ),
                ft.ElevatedButton(
                    "Limpiar",
                    on_click=lambda _: self._clear_results(),
                    icon=ft.Icons.CLEANING_SERVICES,
                    tooltip="Limpiar todos los resultados",
                    col={"sm": 12, "md": 6, "lg": 2},
                ),
            ],
            spacing=10,
        )

        # Área de resultados
        self.validation_results = ft.Column(
            [ft.Text("Resultados de validación:", weight=ft.FontWeight.BOLD)],
            scroll=ft.ScrollMode.ALWAYS,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

        # Construir interfaz
        self.content = self._build_content()

    def _build_content(self):
        """Construye la interfaz de la vista."""
        return ft.Column(
            [
                ft.Text("Cargar Archivo de Datos", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Formatos soportados: XLSX (Excel) y CSV",
                    size=14,
                    color=ft.Colors.GREY_600,
                ),
                ft.Divider(height=20),
                # Sección de carga
                ft.Row([self.select_button, self.loading_indicator], spacing=10),
                self.progress_bar,
                self.file_path_text,
                ft.Divider(height=20),
                # Sección de validación
                ft.Text("Validación de Datos", size=18, weight=ft.FontWeight.BOLD),
                self.upload_status_text,
                self.validation_buttons,
                ft.Container(
                    self.validation_results,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=5,
                    padding=10,
                    expand=True,
                ),
                ft.Divider(height=20),
            ],
            spacing=10,
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,
        )

    def show_notification(self, message: str, color=ft.Colors.BLUE):
        """Muestra una notificación temporal en la página."""
        snack = ft.SnackBar(content=ft.Text(message), bgcolor=color, duration=3000)
        snack.open = True
        if self.page is not None:
            self.page.add(snack)
            self.page.update()

    def _clear_results(self):
        """Limpia todos los resultados de validación."""
        self.validation_results.controls = [
            ft.Text("Resultados de validación:", weight=ft.FontWeight.BOLD)
        ]
        if self.page:
            self.page.update()

    def handle_file_picker_result(self, e: ft.FilePickerResultEvent):
        """Maneja el resultado de la selección de archivos."""
        self._reset_ui()

        if e.files:
            selected_file = e.files[0]
            self.file_path_text.value = f"Archivo seleccionado: {selected_file.name}"

            # Mostrar indicadores de carga
            self.progress_bar.visible = True
            self.loading_indicator.visible = True
            if self.page:
                self.page.update()

            try:
                # Cargar archivo
                df, loaded_name = self.data_loader.load_data_from_file(
                    selected_file.path
                )

                if df is not None:
                    self.app_state.load_dataframe(df, loaded_name)
                    self._show_success_message(loaded_name)
                    self.show_notification(
                        f"Archivo '{loaded_name}' cargado exitosamente!",
                        ft.Colors.GREEN,
                    )
                else:
                    self._show_error_message(selected_file.name)

            except Exception as ex:
                self._show_error_message(selected_file.name)
                print(f"Error al cargar archivo: {str(ex)}")
                self.show_notification(f"Error: {str(ex)}", ft.Colors.RED)

            finally:
                self._hide_loading_indicators()
        else:
            self.file_path_text.value = "Carga cancelada."
            if self.page:
                self.page.update()

    def _reset_ui(self):
        """Reinicia la UI a su estado inicial."""
        self.upload_status_text.value = ""
        self.file_path_text.value = "Ningún archivo seleccionado."
        self._clear_results()

    def _show_success_message(self, filename):
        """Muestra mensaje de éxito."""
        self.upload_status_text.value = f"✅ Archivo '{filename}' cargado exitosamente!"
        self.upload_status_text.color = ft.Colors.GREEN

    def _show_error_message(self, filename):
        """Muestra mensaje de error."""
        self.upload_status_text.value = (
            f"❌ Error al cargar '{filename}'. Verifique la consola."
        )
        self.upload_status_text.color = ft.Colors.RED

    def _hide_loading_indicators(self):
        """Oculta los indicadores de carga."""
        self.progress_bar.visible = False
        self.loading_indicator.visible = False
        if self.page:
            self.page.update()

    def show_data_info(self, info_type):
        """Muestra diferentes tipos de información sobre los datos."""
        self._clear_results()
        df = self.app_state.get_dataframe()

        if df is None:
            self.show_notification(
                "No hay datos cargados para validar.", ft.Colors.ORANGE
            )
            return

        try:
            if info_type == "shape":
                rows, cols = df.shape
                result = f"📐 Forma del DataFrame:\nFilas: {rows}\nColumnas: {cols}"

            elif info_type == "dtypes":
                result = "📊 Tipos de datos:\n" + "\n".join(
                    f"- {col}: {dtype}" for col, dtype in df.dtypes.items()
                )

            elif info_type == "nulls":
                nulls = df.isnull().sum()
                result = "⚠️ Valores nulos por columna:\n" + "\n".join(
                    f"- {col}: {count}" for col, count in nulls.items()
                )

            elif info_type == "nulls_percent":
                obs, _ = df.shape
                nulls_pct = (df.isnull().sum() * 100 / obs).round(2)
                result = "📉 Porcentaje de valores nulos:\n" + "\n".join(
                    f"- {col}: {pct}%" for col, pct in nulls_pct.items()
                )

            elif info_type == "info":
                # Usamos StringIO para capturar la salida de info()
                buffer = io.StringIO()
                df.info(buf=buffer)
                result = "📋 Información completa:\n" + buffer.getvalue()

            else:
                result = "Tipo de validación no reconocido"

            # Mostrar resultados
            self.validation_results.controls.append(ft.Text(result, selectable=True))
            if self.page:
                self.page.update()

        except Exception as e:
            self.show_notification(f"Error en validación: {str(e)}", ft.Colors.RED)
