import flet as ft
import pandas as pd
from typing import Optional


# Ahora hereda directamente de ft.Container
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
            show_checkbox_column=False,  # Opcional: si necesitas checkboxes
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
                    expand=True,  # Permite que el Row se expanda horizontalmente
                    scroll=ft.ScrollMode.ADAPTIVE,  # Permite scroll vertical si la tabla es muy alta
                ),
            ],
            expand=True,  # Permite que el Column se expanda verticalmente
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
        self.content = self._build_content()  # Reconstruye el contenido
        self.update()  # Llama a update para que Flet redibuje el control


# Ejemplo de uso (solo para pruebas, no se ejecuta en la aplicación principal)
if __name__ == "__main__":

    def main(page: ft.Page):
        page.title = "Custom DataTable Test"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.window_width = 800  # type: ignore
        page.window_height = 600  # type: ignore

        # DataFrame de prueba
        data = {
            "Nombre": [
                "Alice",
                "Bob",
                "Charlie",
                "David",
                "Eve",
                "Frank",
                "Grace",
                "Heidi",
                "Ivan",
                "Judy",
                "Kevin",
                "Liam",
                "Mia",
                "Noah",
                "Olivia",
            ],
            "Edad": [25, 30, 35, 28, 22, 45, 29, 31, 26, 33, 38, 27, 24, 36, 41],
            "Ciudad de Residencia Muy Larga": [
                "New York City, NY",
                "London, UK",
                "Paris, France",
                "Berlin, Germany",
                "Tokyo, Japan",
                "Sydney, Australia",
                "Rio de Janeiro, Brazil",
                "Cairo, Egypt",
                "Moscow, Russia",
                "Beijing, China",
                "Rome, Italy",
                "Madrid, Spain",
                "Toronto, Canada",
                "Mexico City, Mexico",
                "Buenos Aires, Argentina",
            ],
            "Salario Anual Muy Alto ($)": [
                50000,
                60000,
                75000,
                55000,
                48000,
                90000,
                52000,
                62000,
                70000,
                58000,
                85000,
                53000,
                49000,
                78000,
                65000,
            ],
            "Experiencia (años)": [3, 7, 10, 5, 2, 20, 6, 8, 4, 9, 15, 3, 1, 12, 18],
        }
        test_df = pd.DataFrame(data)

        # Instancia del control personalizado
        custom_table = DataTableCustom(df=test_df, title="Datos de Empleados")

        # Botón para simular la actualización del DataFrame
        def update_table(e):
            new_data = {
                "Nombre": ["Zoe", "Yara"],
                "Edad": [21, 34],
                "Ciudad de Residencia Muy Larga": ["Dubai, UAE", "Seoul, South Korea"],
                "Salario Anual Muy Alto ($)": [45000, 72000],
                "Experiencia (años)": [1, 9],
            }
            new_df = pd.DataFrame(new_data)
            custom_table.update_dataframe(new_df, "Nuevos Datos de Empleados")
            page.update()

        page.add(
            ft.Column(
                [
                    ft.Text(
                        "Ejemplo de DataTableCustom", size=24, weight=ft.FontWeight.BOLD
                    ),
                    ft.Container(
                        content=custom_table,
                        expand=True,  # Permite que el control personalizado se expanda
                        height=400,  # Altura fija para la prueba, en la app real será expandido
                        width=700,
                        alignment=ft.alignment.center,
                    ),
                    ft.ElevatedButton("Actualizar Tabla", on_click=update_table),
                ],
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )

    ft.app(target=main)
