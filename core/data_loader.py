import pandas as pd
import os


class DataLoader:
    """
    Clase encargada de cargar datos desde diferentes formatos de archivo
    (CSV y XLSX) a un DataFrame de Pandas.
    """

    def load_data_from_file(self, file_path: str, na_values=None):
        """
        Carga datos desde un archivo (CSV o XLSX) a un DataFrame de Pandas.

        Args:
            file_path (str): La ruta completa al archivo a cargar.
            na_values (list, optional): Lista de valores a interpretar como NaN.
                                        Por defecto, None.

        Returns:
            tuple: Una tupla que contiene el DataFrame de Pandas cargado
                   y el nombre original del archivo. Retorna (None, None)
                   si ocurre un error o el archivo no es soportado.
        """
        if not os.path.exists(file_path):
            print(f"Error DataLoader: Archivo no encontrado en {file_path}")
            return None, None

        file_name = None
        try:
            # Obtener la extensión del archivo para determinar el formato
            file_extension = os.path.splitext(file_path)[1].lower()
            file_name = os.path.basename(file_path)

            if file_extension == ".csv":
                # Cargar archivo CSV, aplicando na_values solo si no es None
                if na_values is not None:
                    df = pd.read_csv(file_path, na_values=na_values)
                else:
                    df = pd.read_csv(file_path)
                print(f"DataLoader: Archivo CSV '{file_name}' cargado exitosamente.")
                return df, file_name
            elif file_extension == ".xlsx":
                # Cargar archivo XLSX (pandas usa openpyxl como motor por defecto), aplicando na_values solo si no es None
                if na_values is not None:
                    df = pd.read_excel(file_path, na_values=na_values)
                else:
                    df = pd.read_excel(file_path)
                print(f"DataLoader: Archivo XLSX '{file_name}' cargado exitosamente.")
                return df, file_name
            else:
                print(
                    f"DataLoader Error: Formato de archivo no soportado: {file_extension}"
                )
                return None, None

        except pd.errors.EmptyDataError:
            print(f"DataLoader Error: El archivo '{file_name}' está vacío.")
            return None, None
        except pd.errors.ParserError as e:
            print(f"DataLoader Error: Error de parseo en el archivo '{file_name}': {e}")
            return None, None
        except Exception as e:
            print(
                f"DataLoader Error: Error inesperado al cargar el archivo '{file_name}': {e}"
            )
            return None, None