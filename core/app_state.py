import pandas as pd
import flet as ft # Importar flet para ThemeMode
from typing import Optional


class AppState:
    """
    Una clase para manejar el estado compartido de la aplicación,
    especialmente los DataFrames cargados y manipulados.
    """
    
    def __init__(self):
        self._original_dataframe: Optional[pd.DataFrame] = None
        self._active_dataframe: Optional[pd.DataFrame] = None  # DataFrame que será manipulado
        self.loaded_file_name: Optional[str] = None
        self.current_theme = ft.ThemeMode.DARK

    def load_dataframe(self, dataframe: pd.DataFrame, file_name: Optional[str] = None):
        """
        Carga el DataFrame original y su nombre en el estado.
        Automáticamente crea una copia activa para manipulación.
        """
        self._original_dataframe = dataframe
        self.loaded_file_name = file_name
        # Crea una copia al cargar el original
        self.create_dataframe_copy() 
        print(
            f"AppState: DataFrame original cargado desde {file_name if file_name else 'memoria'} y copia activa creada."
        )

    def create_dataframe_copy(self):
        """
        Crea una copia del DataFrame original y la establece como el DataFrame activo.
        Si no hay un DataFrame original, el activo se establece en None.
        """
        if self._original_dataframe is not None:
            self._active_dataframe = self._original_dataframe.copy()
            print("AppState: Copia del DataFrame original creada y establecida como activa.")
        else:
            self._active_dataframe = None
            print("AppState: No hay DataFrame original para copiar.")

    def load_dataframe_copy(self, df_copy: pd.DataFrame):
        """
        Actualiza el DataFrame activo (la copia) con un nuevo DataFrame.
        Esto se usa después de operaciones de limpieza o manipulación.
        """
        self._active_dataframe = df_copy
        print("AppState: DataFrame activo actualizado con los cambios.")

    from typing import Optional

    def get_original_dataframe(self) -> Optional[pd.DataFrame]:
        """Retorna el DataFrame original cargado (solo lectura)."""
        return self._original_dataframe

    def get_active_dataframe(self) -> Optional[pd.DataFrame]:
        """Retorna el DataFrame activo (la copia que se manipula)."""
        return self._active_dataframe

    def get_loaded_file_name(self) -> Optional[str]:
        """Retorna el nombre del archivo cargado."""
        return self.loaded_file_name

    def toggle_theme(self):
        """Alterna entre tema claro y oscuro."""
        self.current_theme = (
            ft.ThemeMode.LIGHT
            if self.current_theme == ft.ThemeMode.DARK
            else ft.ThemeMode.DARK
        )
        return self.current_theme