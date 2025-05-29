import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from typing import Optional

class PlotGenerator:
    """
    Clase encargada de generar diferentes tipos de gráficos
    a partir de un DataFrame de Pandas.
    """

    def __init__(self):
        # Configuración básica de Matplotlib para mejorar la apariencia
        plt.style.use('seaborn-v0_8-darkgrid') # Un estilo visual agradable
        plt.rcParams['figure.figsize'] = (10, 6) # Tamaño por defecto de las figuras
        plt.rcParams['font.size'] = 12
        plt.rcParams['axes.labelsize'] = 14
        plt.rcParams['axes.titlesize'] = 16
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 10
        plt.rcParams['legend.fontsize'] = 12
        plt.rcParams['figure.titleweight'] = 'bold'

    def _plot_to_base64(self, fig):
        """
        Convierte una figura de Matplotlib a una cadena base64 (PNG).
        Útil para incrustar gráficos en la interfaz de usuario de Flet.

        Args:
            fig (matplotlib.figure.Figure): La figura de Matplotlib a convertir.

        Returns:
            str: Una cadena base64 que representa la imagen PNG de la figura.
        """
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', dpi=100) # dpi para calidad
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig) # Cierra la figura para liberar memoria
        return img_base64
    def generate_histogram(self, df: pd.DataFrame, column: str, title: Optional[str] = None):
        """
        Genera un histograma para una columna numérica.

        Args:
            df (pd.DataFrame): El DataFrame.
            column (str): El nombre de la columna numérica.
            title (str, optional): Título del gráfico. Por defecto, "Histograma de [columna]".

        Returns:
            str: Cadena base64 de la imagen del histograma, o None si hay un error.
        """
        if df is None or df.empty or column not in df.columns:
            print(f"PlotGenerator Error: Columna '{column}' no encontrada o DataFrame vacío para histograma.")
            return None
        if not pd.api.types.is_numeric_dtype(df[column]):
            print(f"PlotGenerator Error: La columna '{column}' no es numérica para histograma.")
            return None

        fig, ax = plt.subplots()
        sns.histplot(data=df, x=column, kde=True, ax=ax) # Seaborn recomienda usar 'data' y 'x'
        ax.set_title(title or f'Histograma de {column}')
        ax.set_xlabel(column)
        ax.set_ylabel('Frecuencia')
        return self._plot_to_base64(fig)

    def generate_scatterplot(self, df: pd.DataFrame, x_column: str, y_column: str, title: Optional[str] = None):
        """
        Genera un diagrama de dispersión entre dos columnas numéricas.

        Args:
            df (pd.DataFrame): El DataFrame.
            x_column (str): El nombre de la columna para el eje X.
            y_column (str): El nombre de la columna para el eje Y.
            title (str, optional): Título del gráfico. Por defecto, "Dispersión de [X] vs [Y]".

        Returns:
            str: Cadena base64 de la imagen del diagrama de dispersión, o None si hay un error.
        """
        if df is None or df.empty or x_column not in df.columns or y_column not in df.columns:
            print(f"PlotGenerator Error: Columnas '{x_column}' o '{y_column}' no encontradas o DataFrame vacío para dispersión.")
            return None
        if not pd.api.types.is_numeric_dtype(df[x_column]) or not pd.api.types.is_numeric_dtype(df[y_column]):
            print(f"PlotGenerator Error: Las columnas '{x_column}' o '{y_column}' no son numéricas para dispersión.")
            return None

        fig, ax = plt.subplots()
        sns.scatterplot(x=df[x_column], y=df[y_column], ax=ax)
        ax.set_title(title or f'Dispersión de {x_column} vs {y_column}')
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        return self._plot_to_base64(fig)

    def generate_boxplot(self, df: pd.DataFrame, column: str, by_column: Optional[str] = None, title: Optional[str] = None):
        """
        Genera un diagrama de caja (boxplot) para una columna numérica.
        Opcionalmente, puede agrupar por una columna categórica.

        Args:
            df (pd.DataFrame): El DataFrame.
            column (str): El nombre de la columna numérica.
            by_column (str, optional): El nombre de una columna categórica para agrupar.
            title (str, optional): Título del gráfico. Por defecto, "Diagrama de Caja de [columna]".

        Returns:
            str: Cadena base64 de la imagen del diagrama de caja, o None si hay un error.
        """
        if df is None or df.empty or column not in df.columns:
            print(f"PlotGenerator Error: Columna '{column}' no encontrada o DataFrame vacío para boxplot.")
            return None
        if not pd.api.types.is_numeric_dtype(df[column]):
            print(f"PlotGenerator Error: La columna '{column}' no es numérica para boxplot.")
            return None
        if by_column and by_column not in df.columns:
            print(f"PlotGenerator Error: Columna de agrupación '{by_column}' no encontrada para boxplot.")
            return None

        fig, ax = plt.subplots()
        if by_column:
            sns.boxplot(x=df[by_column], y=df[column], ax=ax)
            ax.set_title(title or f'Diagrama de Caja de {column} por {by_column}')
            ax.set_xlabel(by_column)
        else:
            sns.boxplot(y=df[column], ax=ax)
            ax.set_title(title or f'Diagrama de Caja de {column}')
        ax.set_ylabel(column)
        return self._plot_to_base64(fig)

    def generate_countplot(self, df: pd.DataFrame, column: str, title: Optional[str] = None):
        """
        Genera un gráfico de conteo para una columna categórica.

        Args:
            df (pd.DataFrame): El DataFrame.
            column (str): El nombre de la columna categórica.
            title (str, optional): Título del gráfico. Por defecto, "Conteo de [columna]".

        Returns:
            str: Cadena base64 de la imagen del gráfico de conteo, o None si hay un error.
        """
        if df is None or df.empty or column not in df.columns:
            print(f"PlotGenerator Error: Columna '{column}' no encontrada o DataFrame vacío para countplot.")
            return None

        fig, ax = plt.subplots()
        sns.countplot(y=df[column], order=df[column].value_counts().index, ax=ax)
        ax.set_title(title or f'Conteo de {column}')
        ax.set_xlabel('Conteo')
        ax.set_ylabel(column)
        return self._plot_to_base64(fig)