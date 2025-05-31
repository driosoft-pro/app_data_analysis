import pandas as pd
import duckdb


class QueryEngine:
    """
    Clase encargada de ejecutar consultas SQL sobre un DataFrame de Pandas
    utilizando DuckDB.
    """
    
    def execute_query_on_dataframe(self, df: pd.DataFrame, query_string: str):
        """
        Ejecuta una consulta SQL sobre el DataFrame de Pandas proporcionado.

        Args:
            df (pd.DataFrame): El DataFrame sobre el cual ejecutar la consulta.
            query_string (str): La cadena de consulta SQL.

        Returns:
            pd.DataFrame: Un nuevo DataFrame con los resultados de la consulta.
                          Retorna un DataFrame vacío si la consulta no devuelve resultados
                          o si ocurre un error.
        Raises:
            ValueError: Si el DataFrame de entrada es None o está vacío.
            duckdb.Error: Si hay un error en la ejecución de la consulta SQL.
        """
        if df is None or df.empty:
            raise ValueError(
                "QueryEngine Error: No hay un DataFrame cargado o está vacío para consultar."
            )

        try:
            # Conectar a una base de datos DuckDB en memoria
            # DuckDB permite registrar DataFrames de Pandas como tablas temporales
            # y luego consultarlas usando SQL.
            con = duckdb.connect(database=":memory:", read_only=False)

            # Registrar el DataFrame de Pandas como una tabla temporal llamada 'my_table'
            con.register("my_table", df)

            # Ejecutar la consulta SQL
            result_df = con.execute(query_string).fetchdf()

            # Cerrar la conexión
            con.close()

            print(
                f"QueryEngine: Consulta SQL ejecutada exitosamente. Filas resultantes: {len(result_df)}"
            )
            return result_df
        except duckdb.Error as e:
            print(f"QueryEngine Error: Error al ejecutar la consulta SQL: {e}")
            raise
        except Exception as e:
            print(f"QueryEngine Error: Error inesperado en el motor de consultas: {e}")
            raise
