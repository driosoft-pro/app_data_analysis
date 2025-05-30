import flet as ft
from typing import Optional


class PlotContainer(ft.Container):
    """
    Control personalizado de Flet para mostrar un gráfico generado
    como una cadena base64. Ahora hereda directamente de ft.Container.
    """

    def __init__(self, plot_base64: Optional[str] = None, title: str = "Gráfico"):
        super().__init__(
            padding=ft.padding.all(10),
            border=ft.border.all(1, ft.Colors.BLACK26),
            border_radius=ft.border_radius.all(5),
            expand=True,  # Permite que este control personalizado se expanda en su padre
        )
        self.plot_base64 = plot_base64
        self.title = title
        # ft.Ref para el ft.Image si necesitas manipularlo directamente
        self.image_ref = ft.Ref[ft.Image]()
        # Inicializa el contenido del contenedor en el constructor
        self.content = self._build_content()

    def _build_content(self):
        """
        Método interno para construir el contenido del contenedor (la imagen y el título).
        """
        if not self.plot_base64:
            return ft.Column(
                [
                    ft.Text(
                        f"{self.title}: No hay gráfico para mostrar.",
                        color=ft.Colors.GREY_600,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            )

        return ft.Column(
            [
                ft.Text(self.title, size=16, weight=ft.FontWeight.BOLD),
                ft.Image(
                    ref=self.image_ref,
                    src_base64=self.plot_base64,
                    fit=ft.ImageFit.CONTAIN,  # Ajusta la imagen dentro del espacio disponible
                    expand=True,  # Permite que la imagen se expanda verticalmente
                ),
            ],
            expand=True,  # Permite que el Column se expanda verticalmente
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )

    def update_plot(
        self, new_plot_base64: Optional[str], new_title: Optional[str] = None
    ):
        """
        Actualiza la imagen del gráfico y el título mostrado por el control.
        Reconstruye el contenido del contenedor.
        """
        self.plot_base64 = new_plot_base64
        if new_title:
            self.title = new_title
        self.content = self._build_content()  # Reconstruye el contenido
        self.update()  # Llama a update para que Flet redibuje el control


# Ejemplo de uso (solo para pruebas, no se ejecuta en la aplicación principal)
if __name__ == "__main__":
    # Para probar este control, necesitarías generar una cadena base64 de un gráfico.
    # Puedes usar el PlotGenerator de core/plot_generator.py para esto.

    import pandas as pd
    from core.plot_generator import PlotGenerator  # Importar el generador de gráficos

    def main(page: ft.Page):
        page.title = "PlotContainer Test"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.window_width = 800  # type: ignore
        page.window_height = 600  # type: ignore

        # Crear un DataFrame dummy para generar un gráfico
        data = {
            "Edad": [25, 30, 35, 28, 22, 40, 25, 30, 32, 28],
            "Ingresos": [
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
            ],
            "Ciudad": [
                "New York",
                "London",
                "New York",
                "Paris",
                "London",
                "New York",
                "London",
                "Paris",
                "New York",
                "London",
            ],
        }
        test_df = pd.DataFrame(data)

        # Generar un gráfico usando PlotGenerator
        plot_gen = PlotGenerator()
        initial_plot_base64 = plot_gen.generate_histogram(
            test_df, "Edad", title="Distribución de Edades (Inicial)"
        )

        # Instancia del control personalizado
        plot_control = PlotContainer(
            plot_base64=initial_plot_base64, title="Histograma de Edades"
        )

        # Botón para simular la actualización del gráfico
        def update_plot_example(e):
            # Generar un nuevo gráfico (por ejemplo, un scatter plot)
            new_plot_base64 = plot_gen.generate_scatterplot(
                test_df, "Edad", "Ingresos", title="Edad vs Ingresos (Actualizado)"
            )
            plot_control.update_plot(new_plot_base64, "Dispersión de Edad vs Ingresos")
            page.update()

        page.add(
            ft.Column(
                [
                    ft.Text(
                        "Ejemplo de PlotContainer", size=24, weight=ft.FontWeight.BOLD
                    ),
                    ft.Container(
                        content=plot_control,
                        expand=True,  # Permite que el control personalizado se expanda
                        height=450,  # Altura fija para la prueba
                        width=700,
                        alignment=ft.alignment.center,
                    ),
                    ft.ElevatedButton(
                        "Actualizar Gráfico", on_click=update_plot_example
                    ),
                ],
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )

    ft.app(target=main)
