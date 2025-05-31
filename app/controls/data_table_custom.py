import flet as ft
import pandas as pd
from typing import Optional


class DataTableCustom(ft.Container):
    """
    Control personalizado de Flet para mostrar un DataFrame de Pandas
    en un ft.DataTable, con soporte para scroll horizontal si es necesario.
    Ahora hereda directamente de ft.Container.
    """

    def __init__(self, df: Optional[pd.DataFrame] = None, title: str = "Datos"):
        super().__init__(
            padding=ft.padding.all(10),
            border=ft.border.all(1, ft.Colors.BLACK26),
            border_radius=ft.border_radius.all(5),
            expand=True,  # Permite que este control personalizado se expanda en su padre
        )
        self.df = df
        self.title = title
        # ft.Ref para el DataTable si necesitas manipularlo directamente después de la construcción
        self.data_table_ref = ft.Ref[ft.DataTable]()
        # Inicializa el contenido del contenedor en el constructor
        self.content = self._build_content()

    def _build_content(self):
        """
        Método interno para construir el contenido del contenedor (la tabla y el título).
        """
        if self.df is None or self.df.empty:
            return ft.Column(
                [
                    ft.Text(
                        f"{self.title}: No hay datos para mostrar.",
                        color=ft.Colors.GREY_600,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            )

        # Crear columnas del DataTable
        columns = [ft.DataColumn(ft.Text(col)) for col in self.df.columns]

        # Crear filas del DataTable
        rows = []
        for i in range(len(self.df)):
            cells = [
                ft.DataCell(ft.Text(str(self.df.iloc[i][col])))
                for col in self.df.columns
            ]
            rows.append(ft.DataRow(cells=cells))

        # Crear el DataTable
        data_table = ft.DataTable(
            ref=self.data_table_ref,
            columns=columns,
            rows=rows,
            # Propiedades para mejorar la apariencia y usabilidad
            sort_column_index=0,  # Opcional: columna por defecto para ordenar
            sort_ascending=True,
            heading_row_color=ft.Colors.BLUE_GREY_100,
            data_row_color={"hovered": ft.Colors.BLUE_GREY_50},
            show_checkbox_column=False,  
            # Añadir scroll horizontal si la tabla es más ancha que el espacio disponible
            horizontal_scroll_mode=ft.ScrollMode.ADAPTIVE,  # type: ignore
        )

        # Usamos un Column para el título y la tabla
        return ft.Column(
            [
                (
                    ft.Text(self.title, size=16, weight=ft.FontWeight.BOLD)
                    if self.title
                    else ft.Container()
                ),
                # Envuelve el DataTable en un Row para permitir que se expanda horizontalmente
                # y que el scroll horizontal funcione correctamente.
                ft.Row(
                    [data_table],
                    expand=True,
                    scroll=ft.ScrollMode.ADAPTIVE,
                ),
            ],
            expand=True,
            spacing=10,
        )

    def update_dataframe(self, new_df: pd.DataFrame, new_title: Optional[str] = None):
        """
        Actualiza el DataFrame y el título mostrado por el control.
        Reconstruye el contenido del contenedor.
        """
        self.df = new_df
        if new_title:
            self.title = new_title
        self.content = self._build_content()
        self.update()