import flet as ft
import pandas as pd
from core.query_engine import QueryEngine
from app.controls.data_table_custom import DataTableCustom


class QueryPage(ft.Container):
    """Vista para realizar consultas SQL sobre el DataFrame cargado."""
    
    def __init__(self, page: ft.Page, app_state, query_engine: QueryEngine):
        super().__init__(padding=20, expand=True, alignment=ft.alignment.top_left)
        self.page = page
        self.app_state = app_state
        self.query_engine = query_engine

        self.query_input = ft.TextField(
            label="Escribe tu consulta SQL aquí...",
            multiline=True,
            min_lines=3,
            max_lines=5,
            expand=True,
        )
        self.results_table_display = DataTableCustom(title="Resultados de la Consulta")
        self.query_status = ft.Text("", ref=ft.Ref())

        self.content = self._build_content()

    def _build_content(self):
        """Construye la interfaz de la vista."""
        return ft.Column(
            [
                ft.Text("Realizar Consultas SQL", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Escribe y ejecuta consultas SQL sobre el DataFrame cargado."),
                self.query_input,
                ft.ElevatedButton(
                    "Ejecutar Consulta",
                    icon=ft.Icons.PLAY_ARROW,
                    on_click=self.handle_execute_query,
                ),
                self.query_status,
                ft.Divider(),
                self.results_table_display,
            ],
            spacing=15,
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,
        )

    def handle_execute_query(self, e):
        """Maneja la ejecución de la consulta SQL."""
        df_original = self.app_state.get_dataframe()
        query_str = self.query_input.value

        if df_original is None:
            self.query_status.value = (
                "Error: No hay un DataFrame cargado para consultar."
            )
            self.query_status.color = ft.Colors.ORANGE_700
            self.results_table_display.update_dataframe(
                pd.DataFrame(), "Carga un archivo primero."
            )  # Limpiar tabla
            if self.page is not None:
                self.page.update()
            return

        if not query_str:
            self.query_status.value = "Error: La consulta no puede estar vacía."
            self.query_status.color = ft.Colors.RED_ACCENT_700
            self.results_table_display.update_dataframe(
                pd.DataFrame(), "Introduce una consulta SQL."
            )  # Limpiar tabla
            if self.page is not None:
                self.page.update()
            return

        self.query_status.value = "Ejecutando consulta..."
        self.query_status.color = ft.Colors.BLUE_GREY_400
        if self.page is not None:
            self.page.update()

        try:
            # Ejecución de consulta con QueryEngine
            result_df = self.query_engine.execute_query_on_dataframe(
                df_original, query_str
            )

            if not result_df.empty:
                self.results_table_display.update_dataframe(
                    result_df, "Resultados de la Consulta"
                )
                self.query_status.value = f"Consulta ejecutada exitosamente. Se encontraron {len(result_df)} resultados."
                self.query_status.color = ft.Colors.GREEN_ACCENT_700
            else:
                self.results_table_display.update_dataframe(
                    pd.DataFrame(), "La consulta no devolvió resultados."
                )
                self.query_status.value = "Consulta ejecutada, pero no hay resultados."
                self.query_status.color = ft.Colors.AMBER_700

        except Exception as ex:
            self.results_table_display.update_dataframe(
                pd.DataFrame(), "Error al ejecutar la consulta."
            )
            self.query_status.value = f"Error: {ex}"
            self.query_status.color = ft.Colors.RED_ACCENT_700
            print(f"Error en consulta: {ex}")

        if self.page is not None:
            self.page.update()
