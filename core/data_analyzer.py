import pandas as pd


class DataAnalyzer:
    """
    Clase encargada de realizar análisis básicos sobre un DataFrame de Pandas.
    """

    def get_dataframe_info(self, df: pd.DataFrame):
        """
        Retorna información básica sobre el DataFrame.

        Args:
            df (pd.DataFrame): El DataFrame a analizar.

        Returns:
            dict: Un diccionario con información como número de filas, columnas,
                  nombres de columnas y tipos de datos.
        """
        if df is None or df.empty:
            return {
                "num_rows": 0,
                "num_cols": 0,
                "columns": [],
                "dtypes": {},
                "missing_values": {},
            }

        info = {
            "num_rows": len(df),
            "num_cols": len(df.columns),
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.apply(
                lambda x: str(x)
            ).to_dict(),  # Convertir dtypes a string
            "missing_values": df.isnull()
            .sum()
            .to_dict(),  # Conteo de valores faltantes por columna
        }
        return info

    def get_descriptive_statistics(self, df: pd.DataFrame):
        """
        Retorna estadísticas descriptivas para las columnas numéricas del DataFrame.

        Args:
            df (pd.DataFrame): El DataFrame a analizar.

        Returns:
            pd.DataFrame: Un DataFrame con estadísticas descriptivas (count, mean, std, min, max, etc.).
                          Retorna un DataFrame vacío si no hay columnas numéricas.
        """
        if df is None or df.empty:
            return pd.DataFrame()

        # Seleccionar solo columnas numéricas para las estadísticas descriptivas
        numeric_df = df.select_dtypes(include=["number"])
        if numeric_df.empty:
            print(
                "DataAnalyzer: No hay columnas numéricas para estadísticas descriptivas."
            )
            return pd.DataFrame()

        return numeric_df.describe()

    def get_unique_values(self, df: pd.DataFrame, column_name: str, top_n: int = 10):
        """
        Retorna los valores únicos y su frecuencia para una columna específica.

        Args:
            df (pd.DataFrame): El DataFrame a analizar.
            column_name (str): El nombre de la columna.
            top_n (int): El número de valores únicos más frecuentes a retornar.

        Returns:
            pd.Series: Una Serie de Pandas con los valores únicos y sus conteos.
                       Retorna una Serie vacía si la columna no existe o el DataFrame está vacío.
        """
        if df is None or df.empty or column_name not in df.columns:
            print(
                f"DataAnalyzer Error: Columna '{column_name}' no encontrada o DataFrame vacío."
            )
            return pd.Series()

        # Contar la frecuencia de cada valor único
        value_counts = df[column_name].value_counts()
        return value_counts.head(top_n)
