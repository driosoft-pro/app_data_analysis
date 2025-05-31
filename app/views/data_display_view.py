import flet as ft
from core.data_analyzer import DataAnalyzer
from core.plot_generator import PlotGenerator


class DataDisplayPage(ft.Container):
    """
    Vista para visualizar y analizar los datos cargados.
    """

    def __init__(self, page: ft.Page, app_state, data_analyzer: DataAnalyzer, plot_generator: PlotGenerator):
        super().__init__(
            padding=20,
            expand=True,
            alignment=ft.alignment.top_left
        )
        self.page = page
        self.app_state = app_state
        self.data_analyzer = data_analyzer
        self.plot_generator = plot_generator

        # Elementos UI
        self.data_table_container = ft.Container(
            content=ft.Text("Cargue un archivo para ver los datos aquí."),
            expand=True,
            alignment=ft.alignment.center,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=5,
            padding=10,
        )
        self.plot_container = ft.Container(
            content=ft.Text("Seleccione opciones de visualización."),
            expand=True,
            alignment=ft.alignment.center,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=5,
            padding=10,
        )

        # Botones de visualización/análisis
        self.analysis_buttons = ft.ResponsiveRow([
            ft.ElevatedButton(
                "Ver Datos",
                on_click=self._display_dataframe,
                icon=ft.Icons.GRID_ON,
                tooltip="Muestra el DataFrame cargado en una tabla.",
                col={"sm": 12, "md": 6, "lg": 3}
            ),
            ft.ElevatedButton(
                "Generar Gráfico (Ejemplo)",
                on_click=self._generate_sample_plot,
                icon=ft.Icons.BAR_CHART,
                tooltip="Genera un gráfico de ejemplo (requiere datos numéricos).",
                col={"sm": 12, "md": 6, "lg": 3}
            ),
        ], spacing=10)

        # Construir interfaz
        self.content = self._build_content()

    def _build_content(self):
        """Construye la interfaz de la vista."""
        return ft.Column(
            [
                ft.Text("Visualización y Análisis de Datos", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20),
                self.analysis_buttons,
                ft.Divider(height=20),
                ft.Text("Tabla de Datos:", size=18, weight=ft.FontWeight.BOLD),
                self.data_table_container,
                ft.Divider(height=20),
                ft.Text("Visualizaciones:", size=18, weight=ft.FontWeight.BOLD),
                self.plot_container,
                ft.Divider(height=20),
            ],
            spacing=10,
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,
        )

    def show_notification(self, message: str, color=ft.Colors.BLUE):
        """Muestra una notificación temporal en la página."""
        snack = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=color,
            duration=3000
        )
        snack.open = True
        if self.page is not None:
            self.page.add(snack)
            self.page.update()

    def _display_dataframe(self, e=None):
        """Muestra el DataFrame activo en una tabla."""
        df = self.app_state.get_active_dataframe() 

        if df is None:
            self.data_table_container.content = ft.Text("No hay datos cargados para mostrar.")
            self.show_notification("No hay datos cargados para mostrar.", ft.Colors.ORANGE)
            if self.page:
                self.page.update()
            return

        try:
            # Crear las columnas para la tabla de Flet
            columns = [
                ft.DataColumn(ft.Text(col), on_sort=self._on_sort_column) for col in df.columns
            ]

            # Crear las filas para la tabla de Flet
            rows = []
            for index, row_data in df.iterrows():
                cells = [ft.DataCell(ft.Text(str(cell))) for cell in row_data]
                rows.append(ft.DataRow(cells=cells))

            data_table = ft.DataTable(
                columns=columns,
                rows=rows,
                sort_column_index=0,
                sort_ascending=True,
                heading_row_color=ft.Colors.GREY_200,
                data_row_color=ft.Colors.BLUE_GREY_100,
                horizontal_lines=ft.BorderSide(1, ft.Colors.GREY_300),
                vertical_lines=ft.BorderSide(0.5, ft.Colors.GREY_300),
                show_checkbox_column=False,
            )

            self.data_table_container.content = ft.Column(
                [
                    ft.Text(f"Mostrando datos de: {self.app_state.get_loaded_file_name()}", size=16, weight=ft.FontWeight.BOLD),
                    ft.Container(data_table, expand=True)
                ],
                expand=True
            )
            self.show_notification("DataFrame mostrado exitosamente.", ft.Colors.GREEN)

        except Exception as ex:
            self.data_table_container.content = ft.Text(f"Error al mostrar el DataFrame: {str(ex)}", color=ft.Colors.RED)
            self.show_notification(f"Error al mostrar datos: {str(ex)}", ft.Colors.RED)
            print(f"Error al mostrar DataFrame: {ex}")

        if self.page:
            self.page.update()

    def _on_sort_column(self, e: ft.ControlEvent):
        """Maneja la ordenación de columnas de la tabla."""
        self.show_notification(f"Ordenando columna: {e.control.label}", ft.Colors.BLUE_GREY_400)
        if self.page:
            self.page.update()

    def _generate_sample_plot(self, e=None):
        """Genera un gráfico de ejemplo utilizando plot_generator."""
        df = self.app_state.get_active_dataframe()

        if df is None:
            self.plot_container.content = ft.Text("Cargue un archivo para generar gráficos.")
            self.show_notification("No hay datos para generar gráficos.", ft.Colors.ORANGE)
            if self.page:
                self.page.update()
            return

        # Intenta generar un histograma de la primera columna numérica
        numeric_cols = df.select_dtypes(include=['number']).columns
        if not numeric_cols.empty:
            column_to_plot = numeric_cols[0]
            try:
                # plot_generator.generate_histogram debería devolver un control de Flet (ej. ft.Image)
                plot_control = self.plot_generator.generate_histogram(df, column_to_plot)
                if plot_control:
                    # Ensure plot_control is a Control, not a string
                    controls = [
                        ft.Text(f"Histograma de '{column_to_plot}':", size=16, weight=ft.FontWeight.BOLD)
                    ]
                    if isinstance(plot_control, str):
                        controls.append(ft.Text(plot_control))
                    else:
                        controls.append(plot_control)
                    self.plot_container.content = ft.Column(
                        controls,
                        expand=True,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                    self.show_notification(f"Gráfico generado para '{column_to_plot}'.", ft.Colors.GREEN)
                else:
                    self.plot_container.content = ft.Text("No se pudo generar el gráfico. Verifique la consola.")
                    self.show_notification("Error al generar el gráfico.", ft.Colors.RED)

            except Exception as ex:
                self.plot_container.content = ft.Text(f"Error al generar el gráfico: {str(ex)}", color=ft.Colors.RED)
                self.show_notification(f"Error al generar gráfico: {str(ex)}", ft.Colors.RED)
                print(f"Error al generar gráfico: {ex}")
        else:
            self.plot_container.content = ft.Text("No hay columnas numéricas para generar un gráfico de ejemplo.")
            self.show_notification("No hay columnas numéricas para gráficos.", ft.Colors.ORANGE)

        if self.page:
            self.page.update()