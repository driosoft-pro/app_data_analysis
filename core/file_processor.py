import pandas as pd
import os


class FileProcessor:
    """
    Clase encargada de procesar archivos, incluyendo la conversión de formatos.
    """
    
    def convert_xlsx_to_csv(self, input_xlsx_path: str, output_csv_path: str):
        """
        Convierte un archivo XLSX a CSV.

        Args:
            input_xlsx_path (str): La ruta completa al archivo XLSX de entrada.
            output_csv_path (str): La ruta completa donde se guardará el archivo CSV de salida.

        Returns:
            bool: True si la conversión fue exitosa, False en caso contrario.
        """
        if not os.path.exists(input_xlsx_path):
            print(
                f"FileProcessor Error: Archivo XLSX de entrada no encontrado en {input_xlsx_path}"
            )
            return False

        try:
            # Leer el archivo XLSX en un DataFrame
            df = pd.read_excel(input_xlsx_path)

            # Asegurarse de que el directorio de salida existe
            output_dir = os.path.dirname(output_csv_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
                print(f"FileProcessor: Directorio de salida creado: {output_dir}")

            # Guardar el DataFrame como CSV
            df.to_csv(
                output_csv_path, index=False
            ) 
            print(
                f"FileProcessor: Archivo XLSX '{os.path.basename(input_xlsx_path)}' convertido a CSV exitosamente en '{output_csv_path}'."
            )
            return True
        except Exception as e:
            print(f"FileProcessor Error: Error al convertir XLSX a CSV: {e}")
            return False
