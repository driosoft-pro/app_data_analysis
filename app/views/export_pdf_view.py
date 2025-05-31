import os
import flet as ft
from fpdf import FPDF


class ExportPDFPage(ft.Container):  # Hereda de ft.Container
    """
    Vista para la sección de Exportar PDF.
    Obtiene el DataFrame del AppState para la exportación.
    """

    def __init__(self, page: ft.Page, app_state):
        super().__init__(padding=20, expand=True, alignment=ft.alignment.top_left)
        self.page = page
        self.app_state = app_state
        self.export_status_text = ft.Text("")
        self.content = (
            self._build_content()
        )

    def _build_content(self):
        """
        Construye y retorna el control raíz para la vista de Exportar PDF.
        """
        return ft.Column(
            [
                ft.Text("Exportar a PDF", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Aquí podrás configurar y generar un informe en formato PDF con los datos cargados."
                ),
                ft.ElevatedButton(
                    "Generar y Exportar PDF",
                    icon=ft.Icons.PICTURE_AS_PDF,
                    on_click=self.handle_export_pdf,
                    tooltip="Genera un informe en PDF con los datos cargados",
                ),
                self.export_status_text,
                ft.Text(
                    "\nOpciones de Exportación (Placeholder):",
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Checkbox(label="Incluir tabla de datos"),
                ft.Checkbox(label="Incluir análisis básico"),
                ft.Checkbox(label="Incluir gráficos (si están disponibles)"),
                ft.TextField(label="Título del informe"),
                ft.Dropdown(
                    options=[
                        ft.dropdown.Option("Vertical (Portrait)"),
                        ft.dropdown.Option("Horizontal (Landscape)"),
                    ],
                    label="Orientación de página",
                    value="Vertical (Portrait)",
                ),
            ],
            spacing=15,
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,
        )

    def handle_export_pdf(self, e):
        """
        Maneja el evento de clic del botón para exportar a PDF.
        Aquí es donde irá la lógica principal de generación del PDF.
        """

        # Usa get_active_dataframe para los datos manipulados
        df = self.app_state.get_active_dataframe()
        # Usa el nombre del archivo original para el título del PDF
        file_name = self.app_state.get_original_dataframe_name()

        if df is None:
            self.export_status_text.value = (
                "Error: No hay datos cargados para exportar."
            )
            self.export_status_text.color = ft.Colors.RED_ACCENT_700
            if self.page is not None:
                self.page.update()
            return

        self.export_status_text.value = "Generando PDF..."
        self.export_status_text.color = ft.Colors.BLUE_GREY_400
        if self.page is not None:
            self.page.update()

        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, "Informe de Análisis de Datos", ln=True, align="C")
            pdf.cell(200, 10, f"Datos del archivo: {file_name if file_name else 'No especificado'}", ln=True)

            # Add table headers
            pdf.ln(10) # Line break
            pdf.set_font("Arial", size=10, style='B')
            # Adjust column width based on number of columns or content
            col_width = pdf.w / (len(df.columns) + 1)
            for col in df.columns:
                pdf.cell(col_width, 10, str(col), border=1, align='C')
            pdf.ln()

            # Add table data (first 10 rows for example)
            pdf.set_font("Arial", size=8)
            for index, row in df.head(10).iterrows():
                for col in df.columns:
                    # Convert NaN to empty string
                    cell_content = str(row[col])
                    # si el contenido de la celda es demasiado largo, lo truncamos
                    if len(cell_content) > 20:
                        cell_content = cell_content[:17] + "..."
                    pdf.cell(col_width, 8, cell_content, border=1)
                pdf.ln()
            if len(df) > 10:
                pdf.cell(200, 10, f"...y {len(df) - 10} filas más. Mostrando solo las primeras 10.", ln=True, align='C')

            # Deine donde guardar el PDF
            pdf_output_dir = "exports"
            os.makedirs(pdf_output_dir, exist_ok=True)
            pdf_output_path = os.path.join(pdf_output_dir, f"informe_{file_name.replace('.', '_') if file_name else 'datos'}.pdf")
            pdf.output(pdf_output_path)

            self.export_status_text.value = f"PDF generado exitosamente en: {pdf_output_path}"
            self.export_status_text.color = ft.Colors.GREEN_ACCENT_700
            print(f"PDF exportado a: {pdf_output_path}")

        except Exception as ex:
            self.export_status_text.value = f"Error al generar el PDF: {ex}"
            self.export_status_text.color = ft.Colors.RED_ACCENT_700
            print(f"Error exportando PDF: {ex}")

        if self.page is not None:
            self.page.update()