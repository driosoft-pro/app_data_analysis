import flet as ft
import pandas as pd
from app.controls.data_table_custom import DataTableCustom


class SearchPage(ft.Container):  # Hereda de ft.Container
    """
    Vista para la sección de Búsqueda dentro del DataFrame cargado.
    Ahora utiliza DataTableCustom para mostrar los resultados.
    """

    def __init__(self, page: ft.Page, app_state):
        super().__init__(padding=20, expand=True, alignment=ft.alignment.top_left)
        self.page = page
        self.app_state = app_state

        self.search_input = ft.TextField(
            label="Introduce el texto a buscar...", expand=True
        )
        self.results_table_display = DataTableCustom(title="Resultados de la Búsqueda")
        self.search_status = ft.Text("", ref=ft.Ref())

        self.content = self._build_content()

    def _build_content(self):
        """Construye la interfaz de la vista."""
        return ft.Column(
            [
                ft.Text(
                    "Buscar en Datos en el DataFrame cargado.",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Introduce texto para encontrar coincidencias en las columnas del dataset."
                ),
                self.search_input,
                ft.ElevatedButton(
                    "Buscar", icon=ft.Icons.SEARCH, on_click=self.handle_search
                ),
                self.search_status,
                ft.Divider(),
                self.results_table_display,
            ],
            spacing=15,
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,
        )

    def handle_search(self, e):
        """
        Maneja el evento de clic del botón de búsqueda.
        Realiza la búsqueda en el DataFrame cargado y actualiza DataTableCustom.
        """
        df = self.app_state.get_dataframe()
        search_text = (self.search_input.value or "").strip()

        if df is None:
            self.search_status.value = "Error: No hay un DataFrame cargado para buscar."
            self.search_status.color = ft.Colors.ORANGE_700
            self.results_table_display.update_dataframe(
                pd.DataFrame(), "Carga un archivo primero."
            )
            if self.page is not None:
                self.page.update()
            return

        if not search_text:
            self.search_status.value = (
                "Error: El texto de búsqueda no puede estar vacío."
            )
            self.search_status.color = ft.Colors.RED_ACCENT_700
            self.results_table_display.update_dataframe(
                pd.DataFrame(), "Introduce un texto para buscar."
            )
            if self.page is not None:
                self.page.update()
            return

        self.search_status.value = "Realizando búsqueda..."
        self.search_status.color = ft.Colors.BLUE_GREY_400
        if self.page is not None:
            self.page.update()

        try:
            string_columns = df.select_dtypes(include="object").columns

            if string_columns.empty:
                self.search_status.value = (
                    "No hay columnas de texto para buscar en este DataFrame."
                )
                self.search_status.color = ft.Colors.AMBER_700
                self.results_table_display.update_dataframe(
                    pd.DataFrame(), "No hay columnas de texto."
                )
                if self.page is not None:
                    self.page.update()
                return

            mask = (
                df[string_columns]
                .astype(str)
                .apply(lambda col: col.str.contains(search_text, case=False, na=False))
                .any(axis=1)
            )

            df_results = df[mask]

            if not df_results.empty:
                self.results_table_display.update_dataframe(
                    df_results, f"Resultados para '{search_text}'"
                )
                self.search_status.value = (
                    f"Se encontraron {len(df_results)} resultados."
                )
                self.search_status.color = ft.Colors.GREEN_ACCENT_700
            else:
                self.results_table_display.update_dataframe(
                    pd.DataFrame(),
                    f"No se encontraron resultados para '{search_text}'.",
                )
                self.search_status.value = (
                    "Búsqueda completada, no se encontraron resultados."
                )
                self.search_status.color = ft.Colors.AMBER_700

        except Exception as ex:
            self.results_table_display.update_dataframe(
                pd.DataFrame(), "Error al realizar la búsqueda."
            )
            self.search_status.value = f"Error: {ex}"
            self.search_status.color = ft.Colors.RED_ACCENT_700
            print(f"Error en búsqueda: {ex}")

        if self.page is not None:
            self.page.update()
