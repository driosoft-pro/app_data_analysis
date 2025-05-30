import flet as ft
import pandas as pd
from core.data_analyzer import DataAnalyzer
from core.plot_generator import PlotGenerator
from app.controls.data_table_custom import DataTableCustom
from app.controls.plot_container import PlotContainer


class DataDisplayPage(ft.Container):  # Hereda de ft.Container
    def __init__(
        self,
        page: ft.Page,
        app_state,
        data_analyzer: DataAnalyzer,
        plot_generator: PlotGenerator,
    ):
        super().__init__(padding=20, expand=True, alignment=ft.alignment.top_left)
        self.page = page
        self.app_state = app_state
        self.data_analyzer = data_analyzer
        self.plot_generator = plot_generator

        # Instancias de tus controles personalizados
        self.data_table_preview = DataTableCustom(title="Vista Previa de Datos")
        self.histogram_plot_container = PlotContainer(title="Histograma (Ejemplo)")
        self.scatterplot_plot_container = PlotContainer(
            title="Diagrama de Dispersión (Ejemplo)"
        )

        self.tabs_content_area = ft.Container(expand=True, ref=ft.Ref())
        self.analysis_tabs = ft.Tabs(  # Hacerlo una propiedad de la instancia
            selected_index=0,
            tabs=[
                ft.Tab(text="Vista Previa Datos"),
                ft.Tab(text="Análisis Básico"),
                ft.Tab(text="Análisis Avanzado"),
            ],
        )
        self.analysis_tabs.on_change = self._handle_tab_change  # Asignar el handler

        self.content = (
            self._build_content()
        )  # Establece el contenido inicial del contenedor

    def _build_content(self):  # Renombrado de build a _build_content
        """Construye la interfaz de la vista."""
        df = self.app_state.get_dataframe()

        if df is None:
            return ft.Column(
                [
                    ft.Text(
                        "Visualización de Datos", size=24, weight=ft.FontWeight.BOLD
                    ),
                    ft.Text(
                        "No hay datos cargados. Por favor, carga un archivo CSV o XLSX primero desde la sección 'Cargar Archivo'."
                    ),
                ],
                spacing=15,
                expand=True,
                scroll=ft.ScrollMode.ADAPTIVE,
            )

        # --- Contenido para la pestaña "Vista Previa Datos" ---
        self.data_table_preview.update_dataframe(
            df.head(10), "Primeras 10 Filas del Dataset"
        )
        tab_content_preview = ft.Column(
            [self.data_table_preview],
            spacing=10,
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,
        )

        # --- Contenido para la pestaña "Análisis Básico" ---
        df_info = self.data_analyzer.get_dataframe_info(df)
        desc_stats_df = self.data_analyzer.get_descriptive_statistics(df)

        desc_stats_text_lines = []
        if not desc_stats_df.empty:
            desc_stats_text_lines.append(
                "Estadísticas Descriptivas de Columnas Numéricas:"
            )
            for index, row in desc_stats_df.iterrows():
                desc_stats_text_lines.append(f"  - Columna '{index}':")
                for stat, value in row.items():
                    desc_stats_text_lines.append(f"    {stat}: {value:.2f}")
        else:
            desc_stats_text_lines.append(
                "No hay columnas numéricas para estadísticas descriptivas."
            )

        tab_content_basic_analysis = ft.Column(
            [
                ft.Text(f"Número total de filas (registros): {df_info['num_rows']}"),
                ft.Text(f"Número total de columnas: {df_info['num_cols']}"),
                ft.Text(f"Nombres de columnas: {', '.join(df_info['columns'])}"),
                ft.Text("Tipos de datos por columna:"),
                *[
                    ft.Text(f"  - {col}: {dtype}")
                    for col, dtype in df_info["dtypes"].items()
                ],
                ft.Text("Valores faltantes por columna:"),
                *[
                    ft.Text(f"  - {col}: {count}")
                    for col, count in df_info["missing_values"].items()
                ],
                ft.Divider(),
                ft.Text("\n".join(desc_stats_text_lines)),
            ],
            spacing=10,
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,
        )

        # --- Contenido para la pestaña "Análisis Avanzado" (con ejemplos de gráficos) ---
        plot_elements = []
        # Asegúrate de que las columnas existan y sean del tipo correcto antes de generar
        if "Edad" in df.columns and pd.api.types.is_numeric_dtype(df["Edad"]):
            hist_base64 = self.plot_generator.generate_histogram(
                df, "Edad", title="Distribución de Edades"
            )
            if hist_base64:
                self.histogram_plot_container.update_plot(
                    hist_base64, "Histograma de Edades"
                )
                plot_elements.append(self.histogram_plot_container)
        else:
            plot_elements.append(
                ft.Text(
                    "No se pudo generar histograma de 'Edad' (columna no encontrada o no numérica)."
                )
            )

        if (
            "Edad" in df.columns
            and "Ingresos" in df.columns
            and pd.api.types.is_numeric_dtype(df["Edad"])
            and pd.api.types.is_numeric_dtype(df["Ingresos"])
        ):
            scatter_base64 = self.plot_generator.generate_scatterplot(
                df, "Edad", "Ingresos", title="Edad vs Ingresos"
            )
            if scatter_base64:
                self.scatterplot_plot_container.update_plot(
                    scatter_base64, "Dispersión de Edad vs Ingresos"
                )
                plot_elements.append(self.scatterplot_plot_container)
        else:
            plot_elements.append(
                ft.Text(
                    "No se pudo generar diagrama de dispersión de 'Edad' vs 'Ingresos' (columnas no encontradas o no numéricas)."
                )
            )

        tab_content_advanced_analysis = ft.Column(
            [
                ft.Text(
                    "Análisis Avanzado y Visualizaciones:", weight=ft.FontWeight.BOLD
                ),
                ft.Text("Aquí se mostrarán gráficos y análisis más complejos."),
                ft.Divider(),
                *plot_elements,
            ],
            spacing=10,
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,
        )

        # Establece el contenido inicial del área de pestañas
        # Esto se hará en _handle_tab_change o al cargar la vista por primera vez
        # self.tabs_content_area.content = tab_content_preview

        # Retorna el Column principal, ya que el contenedor padre (self) lo contiene.
        return ft.Column(
            [
                ft.Text("Análisis Dataset", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(f"Dataset: {self.app_state.loaded_file_name or 'No cargado'}"),
                self.analysis_tabs,
                self.tabs_content_area,
            ],
            spacing=15,
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,
        )

    def _handle_tab_change(
        self, e
    ):  # Renombrado de handle_tab_change a _handle_tab_change
        """Maneja el cambio de pestaña."""
        df = self.app_state.get_dataframe()
        if df is None:  # Si no hay DataFrame, no intentes construir contenido dinámico
            self.tabs_content_area.content = ft.Text(
                "No hay datos cargados para mostrar en esta pestaña."
            )
            if self.page is not None:
                self.page.update()
            return

        selected_tab_index = e.control.selected_index
        # Reconstruye el contenido de las pestañas cada vez que se cambia
        # Esto asegura que los datos más recientes del DataFrame se reflejen
        # y que los gráficos se generen con los datos actuales.
        if selected_tab_index == 0:
            self.data_table_preview.update_dataframe(
                df.head(10), "Primeras 10 Filas del Dataset"
            )
            self.tabs_content_area.content = ft.Column(
                [self.data_table_preview],
                spacing=10,
                expand=True,
                scroll=ft.ScrollMode.ADAPTIVE,
            )
        elif selected_tab_index == 1:
            df_info = self.data_analyzer.get_dataframe_info(df)
            desc_stats_df = self.data_analyzer.get_descriptive_statistics(df)
            desc_stats_text_lines = []
            if not desc_stats_df.empty:
                desc_stats_text_lines.append(
                    "Estadísticas Descriptivas de Columnas Numéricas:"
                )
                for index, row in desc_stats_df.iterrows():
                    desc_stats_text_lines.append(f"  - Columna '{index}':")
                    for stat, value in row.items():
                        desc_stats_text_lines.append(f"    {stat}: {value:.2f}")
            else:
                desc_stats_text_lines.append(
                    "No hay columnas numéricas para estadísticas descriptivas."
                )

            self.tabs_content_area.content = ft.Column(
                [
                    ft.Text(
                        f"Número total de filas (registros): {df_info['num_rows']}"
                    ),
                    ft.Text(f"Número total de columnas: {df_info['num_cols']}"),
                    ft.Text(f"Nombres de columnas: {', '.join(df_info['columns'])}"),
                    ft.Text("Tipos de datos por columna:"),
                    *[
                        ft.Text(f"  - {col}: {dtype}")
                        for col, dtype in df_info["dtypes"].items()
                    ],
                    ft.Text("Valores faltantes por columna:"),
                    *[
                        ft.Text(f"  - {col}: {count}")
                        for col, count in df_info["missing_values"].items()
                    ],
                    ft.Divider(),
                    ft.Text("\n".join(desc_stats_text_lines)),
                ],
                spacing=10,
                expand=True,
                scroll=ft.ScrollMode.ADAPTIVE,
            )
        elif selected_tab_index == 2:
            plot_elements = []
            if "Edad" in df.columns and pd.api.types.is_numeric_dtype(df["Edad"]):
                hist_base64 = self.plot_generator.generate_histogram(
                    df, "Edad", title="Distribución de Edades"
                )
                if hist_base64:
                    self.histogram_plot_container.update_plot(
                        hist_base64, "Histograma de Edades"
                    )
                    plot_elements.append(self.histogram_plot_container)
            else:
                plot_elements.append(
                    ft.Text(
                        "No se pudo generar histograma de 'Edad' (columna no encontrada o no numérica)."
                    )
                )

            if (
                "Edad" in df.columns
                and "Ingresos" in df.columns
                and pd.api.types.is_numeric_dtype(df["Edad"])
                and pd.api.types.is_numeric_dtype(df["Ingresos"])
            ):
                scatter_base64 = self.plot_generator.generate_scatterplot(
                    df, "Edad", "Ingresos", title="Edad vs Ingresos"
                )
                if scatter_base64:
                    self.scatterplot_plot_container.update_plot(
                        scatter_base64, "Dispersión de Edad vs Ingresos"
                    )
                    plot_elements.append(self.scatterplot_plot_container)
            else:
                plot_elements.append(
                    ft.Text(
                        "No se pudo generar diagrama de dispersión de 'Edad' vs 'Ingresos' (columnas no encontradas o no numéricas)."
                    )
                )

            self.tabs_content_area.content = ft.Column(
                [
                    ft.Text(
                        "Análisis Avanzado y Visualizaciones:",
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text("Aquí se mostrarán gráficos y análisis más complejos."),
                    ft.Divider(),
                    *plot_elements,
                ],
                spacing=10,
                expand=True,
                scroll=ft.ScrollMode.ADAPTIVE,
            )
        if self.page is not None:
            self.page.update()
