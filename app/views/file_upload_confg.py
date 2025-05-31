import io
import flet as ft
import pandas as pd
import numpy as np
from core.data_loader import DataLoader


class FileUploadConfig():
    """Configuración para la carga de archivos."""
    
    def __init__(self, page: ft.Page, app_state, file_picker: ft.FilePicker,
                 upload_status_text: ft.Text, file_path_text: ft.Text,
                 progress_bar: ft.ProgressBar, loading_indicator: ft.Row,
                 validation_results: ft.Column, manipulation_results: ft.Column,
                 manipulated_validation_results: ft.Column,
                 object_type_conversion_controls: ft.Column,
                 null_handling_controls: ft.Column,
                 null_handling_column_dropdown: ft.Dropdown,
                 null_handling_strategy_dropdown: ft.Dropdown,
                 rename_column_controls: ft.Column,
                 rename_column_dropdown: ft.Dropdown,
                 new_column_name_textfield: ft.TextField): # Added new UI elements
        self.page = page
        self.app_state = app_state
        self.file_picker = file_picker # Now passed from the view
        self.file_types = ['csv', 'xlsx', 'json']
        self.max_file_size = 10 * 1024 * 1024  # 10 MB
        self.data_loader = DataLoader()

        # References to UI elements from the view
        self.upload_status_text = upload_status_text
        self.file_path_text = file_path_text
        self.progress_bar = progress_bar
        self.loading_indicator = loading_indicator
        self.validation_results = validation_results
        self.manipulation_results = manipulation_results
        self.manipulated_validation_results = manipulated_validation_results
        self.object_type_conversion_controls = object_type_conversion_controls
        self.null_handling_controls = null_handling_controls
        self.null_handling_column_dropdown = null_handling_column_dropdown
        self.null_handling_strategy_dropdown = null_handling_strategy_dropdown
        self.rename_column_controls = rename_column_controls
        self.rename_column_dropdown = rename_column_dropdown
        self.new_column_name_textfield = new_column_name_textfield

    def show_notification(self, message: str, color=ft.Colors.BLUE):
        """Muestra una notificación temporal en la página."""
        snack = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=color,
            duration=3000
        )
        snack.open = True
        if self.page is not None:
            self.page.add(snack)
            self.page.update()

    def _reset_ui(self):
        """Reinicia la UI a su estado inicial."""
        self.upload_status_text.value = ""
        self.file_path_text.value = "Ningún archivo seleccionado."
        self._clear_results()
        self.object_type_conversion_controls.visible = False
        self.object_type_conversion_controls.controls.clear()
        self.null_handling_controls.visible = False
        self.rename_column_controls.visible = False
        if self.page:
            self.page.update()

    def _show_success_message(self, filename):
        """Muestra mensaje de éxito."""
        self.upload_status_text.value = f"✅ Archivo '{filename}' cargado exitosamente!"
        self.upload_status_text.color = ft.Colors.GREEN

    def _show_error_message(self, filename):
        """Muestra mensaje de error."""
        self.upload_status_text.value = f"❌ Error al cargar '{filename}'. Verifique la consola."
        self.upload_status_text.color = ft.Colors.RED

    def _hide_loading_indicators(self):
        """Oculta los indicadores de carga."""
        self.progress_bar.visible = False
        self.loading_indicator.visible = False
        if self.page:
            self.page.update()

    def _clear_results(self, e=None):
        """Limpia todos los resultados de validación y manipulación."""
        self.validation_results.controls = [
            ft.Text("Resultados de Validación del Dataset Original:", weight=ft.FontWeight.BOLD)
        ]
        self.manipulation_results.controls = [
            ft.Text("Resultados de Manipulación de Datos Básicos:", weight=ft.FontWeight.BOLD)
        ]
        self.manipulated_validation_results.controls = [ # Limpia el nuevo contenedor
            ft.Text("Resultados de Validación del Dataset Manipulado:", weight=ft.FontWeight.BOLD)
        ]
        # Limpia los resultados de manipulación
        self.object_type_conversion_controls.controls.clear()
        self.object_type_conversion_controls.visible = False
        self.null_handling_controls.visible = False
        self.rename_column_controls.visible = False
        self.rename_column_dropdown.value = None
        self.new_column_name_textfield.value = ""
        if self.page:
            self.page.update()

    def handle_file_picker_result(self, e: ft.FilePickerResultEvent):
        """Maneja el resultado de la selección de archivos."""
        self._reset_ui()

        if e.files:
            selected_file = e.files[0]
            self.file_path_text.value = f"Archivo seleccionado: {selected_file.name}"

            # Mostrar indicadores de carga
            self.progress_bar.visible = True
            self.loading_indicator.visible = True
            if self.page:
                self.page.update()

            try:
                # Cargar archivo y reemplazar '?' con NaN
                df, loaded_name = self.data_loader.load_data_from_file(
                    selected_file.path,
                    na_values=['?'] # Pass '?' to be treated as NaN during loading
                )

                if df is not None:
                    self.app_state.load_dataframe(df, loaded_name) # Load original
                    # La copia se crea automáticamente en app_state.load_dataframe
                    self._show_success_message(loaded_name)
                    self.show_notification(f"Archivo '{loaded_name}' cargado exitosamente y '?' reemplazados por NaN!", ft.Colors.GREEN)
                else:
                    self._show_error_message(selected_file.name)

            except Exception as ex:
                self._show_error_message(selected_file.name)
                print(f"Error al cargar archivo: {str(ex)}")
                self.show_notification(f"Error: {str(ex)}", ft.Colors.RED)

            finally:
                self._hide_loading_indicators()
        else:
            self.file_path_text.value = "Carga cancelada."
            if self.page:
                self.page.update()

    def show_data_info(self, info_type):
        """Muestra diferentes tipos de información sobre los datos originales (o la copia si no se ha creado una)."""
        
        # Limpia solo los resultados de validación original
        self.validation_results.controls = [
            ft.Text("Resultados de Validación del Dataset Original:", weight=ft.FontWeight.BOLD)
        ]
        df = self.app_state.get_original_dataframe() # Usa el original para esta sección
        if df is None:
            self.show_notification("No hay datos cargados para validar el dataset original.", ft.Colors.ORANGE)
            return

        try:
            result_content = []
            if info_type == "shape":
                rows, cols = df.shape
                result_content.append(ft.Text(f"📐 Forma del DataFrame:\nFilas: {rows}\nColumnas: {cols}", selectable=True))

            elif info_type == "dtypes":
                result_content.append(ft.Text("📊 Tipos de datos:", selectable=True))
                for col, dtype in df.dtypes.items():
                    result_content.append(ft.Text(f"- {col}: {dtype}", selectable=True))

            elif info_type == "nulls":
                nulls_count = df.isnull().sum()
                columns_with_nulls = {col: count for col, count in nulls_count.items() if count > 0}

                if not columns_with_nulls:
                    result_content.append(ft.Text("🎉 No hay valores nulos en el DataFrame."))
                else:
                    result_content.append(ft.Text("⚠️ Valores nulos por columna (conteo):", selectable=True))
                    for col, count in columns_with_nulls.items():
                        result_content.append(ft.Text(f"- {col}: {count}", selectable=True))

            elif info_type == "nulls_percent":
                total_rows = len(df)
                if total_rows == 0:
                    result_content.append(ft.Text("El DataFrame está vacío, no se puede calcular el porcentaje de nulos."))
                else:
                    nulls_pct = (df.isnull().sum() / total_rows * 100).round(2)
                    columns_with_nulls_pct = {col: pct for col, pct in nulls_pct.items() if pct > 0}

                    if not columns_with_nulls_pct:
                        result_content.append(ft.Text("🎉 No hay valores nulos en el DataFrame."))
                    else:
                        result_content.append(ft.Text("📉 Porcentaje de valores nulos por columna:", selectable=True))
                        for col, pct in columns_with_nulls_pct.items():
                            result_content.append(ft.Text(f"- {col}: {pct}%", selectable=True))

            elif info_type == "info":
                buffer = io.StringIO()
                df.info(buf=buffer)
                result_content.append(ft.Text("📋 Información completa del DataFrame:", selectable=True))
                result_content.append(ft.Text(buffer.getvalue(), selectable=True))

            elif info_type == "column_names": # Nuevo tipo para nombres de columnas
                result_content.append(ft.Text("📝 Nombres de las columnas:", selectable=True))
                for col_name in df.columns.tolist():
                    result_content.append(ft.Text(f"- {col_name}", selectable=True))

            else:
                result_content.append(ft.Text("Tipo de validación no reconocido"))

            self.validation_results.controls.extend(result_content)
            if self.page:
                self.page.update()

        except Exception as e:
            self.show_notification(f"Error en validación: {str(e)}", ft.Colors.RED)

    def show_manipulated_data_info(self, info_type):
        """Muestra diferentes tipos de información sobre el DataFrame MANIPULADO la copia."""
        
        # Limpia solo los resultados de validación manipulada
        self.manipulated_validation_results.controls = [
            ft.Text("Resultados de Validación del Dataset Manipulado:", weight=ft.FontWeight.BOLD)
        ]
        df = self.app_state.get_active_dataframe() # Usa el activo para esta sección

        if df is None:
            self.show_notification("No hay datos manipulados para validar.", ft.Colors.ORANGE)
            return

        try:
            result_content = []
            if info_type == "shape":
                rows, cols = df.shape
                result_content.append(ft.Text(f"📐 Forma del DataFrame:\nFilas: {rows}\nColumnas: {cols}", selectable=True))

            elif info_type == "dtypes":
                result_content.append(ft.Text("📊 Tipos de datos:", selectable=True))
                for col, dtype in df.dtypes.items():
                    result_content.append(ft.Text(f"- {col}: {dtype}", selectable=True))

            elif info_type == "nulls":
                nulls_count = df.isnull().sum()
                columns_with_nulls = {col: count for col, count in nulls_count.items() if count > 0}

                if not columns_with_nulls:
                    result_content.append(ft.Text("🎉 No hay valores nulos en el DataFrame."))
                else:
                    result_content.append(ft.Text("⚠️ Valores nulos por columna (conteo):", selectable=True))
                    for col, count in columns_with_nulls.items():
                        result_content.append(ft.Text(f"- {col}: {count}", selectable=True))

            elif info_type == "nulls_percent":
                total_rows = len(df)
                if total_rows == 0:
                    result_content.append(ft.Text("El DataFrame está vacío, no se puede calcular el porcentaje de nulos."))
                else:
                    nulls_pct = (df.isnull().sum() / total_rows * 100).round(2)
                    columns_with_nulls_pct = {col: pct for col, pct in nulls_pct.items() if pct > 0}

                    if not columns_with_nulls_pct:
                        result_content.append(ft.Text("🎉 No hay valores nulos en el DataFrame."))
                    else:
                        result_content.append(ft.Text("📉 Porcentaje de valores nulos por columna:", selectable=True))
                        for col, pct in columns_with_nulls_pct.items():
                            result_content.append(ft.Text(f"- {col}: {pct}%", selectable=True))

            elif info_type == "info":
                buffer = io.StringIO()
                df.info(buf=buffer)
                result_content.append(ft.Text("📋 Información completa del DataFrame:", selectable=True))
                result_content.append(ft.Text(buffer.getvalue(), selectable=True))

            elif info_type == "column_names": # Nuevo tipo para nombres de columnas
                result_content.append(ft.Text("📝 Nombres de las columnas:", selectable=True))
                for col_name in df.columns.tolist():
                    result_content.append(ft.Text(f"- {col_name}", selectable=True))

            else:
                result_content.append(ft.Text("Tipo de validación no reconocido"))

            self.manipulated_validation_results.controls.extend(result_content)
            if self.page:
                self.page.update()

        except Exception as e:
            self.show_notification(f"Error en validación: {str(e)}", ft.Colors.RED)

    def _create_dataframe_copy(self, e=None):
        """Crea una copia del DataFrame original para manipulación."""
        
        # Limpia solo los resultados de manipulación
        self.manipulation_results.controls = [ 
            ft.Text("Resultados de Manipulación de Datos Básicos:", weight=ft.FontWeight.BOLD)
        ]
        df_original = self.app_state.get_original_dataframe()
        if df_original is None:
            self.show_notification("Primero cargue un archivo para crear una copia.", ft.Colors.ORANGE)
            return

        self.app_state.create_dataframe_copy()
        self.show_notification("Copia del DataFrame creada exitosamente para manipulación.", ft.Colors.GREEN)
        self.manipulation_results.controls.append(ft.Text("✅ Se ha creado una copia del DataFrame para manipulación."))
        self.manipulation_results.controls.append(ft.Text(f"Filas: {self.app_state.get_active_dataframe().shape[0]}, Columnas: {self.app_state.get_active_dataframe().shape[1]}"))
        # Después de crear la copia, es buena idea mostrar su validación en la sección de manipulados
        self.show_manipulated_data_info("shape")
        if self.page:
            self.page.update()

    def _show_duplicates(self, target_df_type: str): # AHORA RECIBE target_df_type
        """
        Muestra las filas duplicadas en el DataFrame original o copiado.
        """
        
        # Limpia solo los resultados de validación original
        if target_df_type == "original":
            self.validation_results.controls = [ 
                ft.Text("Resultados de Validación del Dataset Original:", weight=ft.FontWeight.BOLD)
            ]
            df = self.app_state.get_original_dataframe()
            result_container = self.validation_results
            notification_prefix = "Original"
        else: # target_df_type == "manipulated" o cualquier otro
            # Limpia solo los resultados de manipulación
            self.manipulation_results.controls = [ 
                ft.Text("Resultados de Manipulación de Datos Básicos:", weight=ft.FontWeight.BOLD) # RENOMBRADO AQUÍ
            ]
            df = self.app_state.get_active_dataframe()
            result_container = self.manipulation_results
            notification_prefix = "Manipulado"

        if df is None:
            self.show_notification(f"No hay datos {notification_prefix.lower()} cargados o copiados para verificar duplicados.", ft.Colors.ORANGE)
            return

        duplicates = df[df.duplicated()]
        if not duplicates.empty:
            result = f"🔍 Se encontraron {len(duplicates)} filas duplicadas en el DataFrame {notification_prefix}:\n"
            # Para evitar imprimir un DataFrame masivo, solo muestra las primeras filas
            result += duplicates.head().to_string()
            if len(duplicates) > 5:
                result += "\n... (mostrando solo las primeras 5)"
            result_container.controls.append(
                ft.Text(result, selectable=True)
            )
            self.show_notification(f"Se encontraron {len(duplicates)} filas duplicadas en el dataset {notification_prefix.lower()}.", ft.Colors.BLUE)
        else:
            result_container.controls.append(
                ft.Text(f"✅ No se encontraron filas duplicadas en el DataFrame {notification_prefix}.")
            )
            self.show_notification(f"No se encontraron filas duplicadas en el dataset {notification_prefix.lower()}.", ft.Colors.GREEN)

        if self.page:
            self.page.update()

    def _delete_duplicates(self, e=None):
        """Elimina las filas duplicadas del DataFrame copiado."""
        
        # Limpia solo los resultados de manipulación
        self.manipulation_results.controls = [ 
            ft.Text("Resultados de Manipulación de Datos Básicos:", weight=ft.FontWeight.BOLD)
        ]
        df = self.app_state.get_active_dataframe()
        if df is None:
            self.show_notification("No hay datos cargados o copiados para eliminar duplicados.", ft.Colors.ORANGE)
            return

        initial_rows = len(df)
        df.drop_duplicates(inplace=True)
        rows_after_dedup = len(df)

        if initial_rows > rows_after_dedup:
            # Actualiza el DataFrame copiado en AppState
            self.app_state.load_dataframe_copy(df) 
            self.show_notification(f"Se eliminaron {initial_rows - rows_after_dedup} filas duplicadas.", ft.Colors.GREEN)
            self.manipulation_results.controls.append(
                ft.Text(f"🗑️ Se eliminaron {initial_rows - rows_after_dedup} filas duplicadas.\n"
                        f"Filas restantes: {rows_after_dedup}")
            )
            # Después de eliminar, muestra la forma actualizada en la sección de manipulados
            self.show_manipulated_data_info("shape")
        else:
            self.show_notification("No se encontraron duplicados para eliminar.", ft.Colors.BLUE_GREY_400)
            self.manipulation_results.controls.append(
                ft.Text("✅ No se encontraron filas duplicadas para eliminar.")
            )

        if self.page:
            self.page.update()

    def _show_object_column_types(self, e=None):
        """
        Identifica columnas de tipo 'object' y permite al usuario seleccionar
        un nuevo tipo de dato para conversión.
        """
        
        # Limpia solo los resultados de manipulación
        self.manipulation_results.controls = [
            ft.Text("Resultados de Manipulación de Datos Básicos:", weight=ft.FontWeight.BOLD)
        ]
        # Oculta otros controles de manipulación
        self.object_type_conversion_controls.controls.clear()
        self.object_type_conversion_controls.visible = False
        self.null_handling_controls.visible = False
        self.rename_column_controls.visible = False

        df = self.app_state.get_active_dataframe()
        if df is None:
            self.show_notification("No hay datos cargados o copiados para analizar.", ft.Colors.ORANGE)
            return

        object_columns = df.select_dtypes(include=['object']).columns.tolist()

        if not object_columns:
            self.manipulation_results.controls.append(
                ft.Text("✅ No hay columnas de tipo 'object' para analizar.")
            )
            self.show_notification("No hay columnas de tipo 'object'.", ft.Colors.BLUE_GREY_400)
            if self.page:
                self.page.update()
            return

        self.object_type_conversion_controls.controls.clear()
        self.object_type_conversion_controls.controls.append(
            ft.Text("Seleccione tipo para columnas 'object':", weight=ft.FontWeight.BOLD)
        )

        for col in object_columns:
            # Muestra valores únicos para ayudar al usuario a decidir
            unique_values_sample = df[col].dropna().unique()
            sample_text = f"Valores únicos (muestra): {unique_values_sample[:5].tolist()}"
            if len(unique_values_sample) > 5:
                sample_text += "..."

            dropdown = ft.Dropdown(
                label=f"Columna: {col}",
                options=[
                    ft.dropdown.Option("int"),
                    ft.dropdown.Option("float"),
                    ft.dropdown.Option("datetime"),
                    ft.dropdown.Option("category"),
                    ft.dropdown.Option("string")
                ],
                hint_text="Convertir a...",
                data=col
            )
            self.object_type_conversion_controls.controls.append(
                ft.Column([
                    ft.Text(f"Columna '{col}' (Tipo actual: {df[col].dtype}):"),
                    ft.Text(sample_text, size=12, color=ft.Colors.GREY_600),
                    ft.Row([
                        dropdown,
                        ft.ElevatedButton("Convertir", on_click=self._convert_column_type, data=dropdown)
                    ])
                ])
            )

        self.object_type_conversion_controls.visible = True
        self.show_notification(f"Se encontraron {len(object_columns)} columnas de tipo 'object'.", ft.Colors.BLUE)
        if self.page:
            self.page.update()

    def _convert_column_type(self, e):
        """Maneja la conversión de tipo de columna seleccionada."""
        
        # Limpia solo los resultados de manipulación
        self.manipulation_results.controls = [
            ft.Text("Resultados de Manipulación de Datos Básicos:", weight=ft.FontWeight.BOLD)
        ]
        df = self.app_state.get_active_dataframe()
        if df is None:
            self.show_notification("No hay datos para convertir.", ft.Colors.ORANGE)
            return

        dropdown = e.control.data
        column_name = dropdown.data
        selected_type = dropdown.value

        if not selected_type:
            self.show_notification(f"Seleccione un tipo para la columna '{column_name}'.", ft.Colors.ORANGE)
            return

        try:
            original_dtype = df[column_name].dtype
            if selected_type == "int":
                # Convertir a numérico primero, luego a entero nullable
                df[column_name] = pd.to_numeric(df[column_name], errors='coerce').astype('Int64')
            elif selected_type == "float":
                df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
            elif selected_type == "datetime":
                df[column_name] = pd.to_datetime(df[column_name], errors='coerce')
            elif selected_type == "category":
                df[column_name] = df[column_name].astype('category')
            elif selected_type == "string":
                df[column_name] = df[column_name].astype(str)
            
            # Actualiza el DataFrame copiado en AppState
            self.app_state.load_dataframe_copy(df)
            self.show_notification(
                f"Columna '{column_name}' convertida de '{original_dtype}' a '{selected_type}' exitosamente.",
                ft.Colors.GREEN
            )
            self.manipulation_results.controls.append(
                ft.Text(f"✅ Columna '{column_name}' convertida de '{original_dtype}' a '{selected_type}' exitosamente.")
            )
            # Después de la conversión, muestra los dtypes actualizados en la sección de manipulados
            self.show_manipulated_data_info("dtypes")
            # Ocultar los controles de conversión después de una conversión exitosa
            self.object_type_conversion_controls.visible = False
            self.object_type_conversion_controls.controls.clear()

        except Exception as ex:
            self.show_notification(f"Error al convertir columna '{column_name}': {str(ex)}", ft.Colors.RED)
            self.manipulation_results.controls.append(
                ft.Text(f"❌ Error al convertir columna '{column_name}': {str(ex)}", color=ft.Colors.RED)
            )

        if self.page:
            self.page.update()

    def _show_null_handling_options(self, e=None):
        """
        Muestra los controles para el manejo de nulos y carga las columnas del DataFrame.
        """
        
        # Limpia solo los resultados de manipulación
        self.manipulation_results.controls = [
            ft.Text("Resultados de Manipulación de Datos Básicos:", weight=ft.FontWeight.BOLD)
        ]
        # Oculta otros controles de manipulación
        self.null_handling_controls.visible = True
        self.object_type_conversion_controls.visible = False
        self.rename_column_controls.visible = False

        df = self.app_state.get_active_dataframe()
        if df is None:
            self.show_notification("No hay datos cargados o copiados para el manejo de nulos.", ft.Colors.ORANGE)
            self.null_handling_controls.visible = False
            if self.page:
                self.page.update()
            return

        # Cargar opciones de columnas en el dropdown
        column_options = [ft.dropdown.Option("Todas las columnas")]
        column_options.extend([ft.dropdown.Option(col) for col in df.columns])
        self.null_handling_column_dropdown.options = column_options
        self.null_handling_column_dropdown.value = "Todas las columnas"
        self.null_handling_strategy_dropdown.value = None

        self.show_notification("Seleccione opciones para el manejo de nulos.", ft.Colors.BLUE)
        if self.page:
            self.page.update()

    def _hide_null_handling_options(self, e=None):
        """Oculta los controles de manejo de nulos."""
        self.null_handling_controls.visible = False
        if self.page:
            self.page.update()

    def _apply_null_handling(self, e=None):
        """
        Aplica la estrategia de manejo de nulos seleccionada al DataFrame activo.
        """
        
        # Limpia solo los resultados de manipulación
        self.manipulation_results.controls = [
            ft.Text("Resultados de Manipulación de Datos Básicos:", weight=ft.FontWeight.BOLD)
        ]
        df = self.app_state.get_active_dataframe()
        if df is None:
            self.show_notification("No hay datos para aplicar manejo de nulos.", ft.Colors.ORANGE)
            return

        selected_column = self.null_handling_column_dropdown.value
        selected_strategy = self.null_handling_strategy_dropdown.value

        if not selected_strategy:
            self.show_notification("Seleccione una estrategia de manejo de nulos.", ft.Colors.ORANGE)
            return

        try:
            # Total de nulos antes de la operación
            initial_nulls = df.isnull().sum().sum()
            initial_rows = len(df)

            if selected_strategy == "Reemplazar '?' con NaN":
                # Aunque DataLoader ya lo hace, esto permite aplicarlo post-carga si es necesario
                df.replace('?', np.nan, inplace=True)
                message = "Se reemplazaron '?' con NaN en el DataFrame."

            elif selected_strategy == "Rellenar con Media (Numérico)":
                target_columns = [selected_column] if selected_column != "Todas las columnas" else df.columns
                for col in target_columns:
                    if pd.api.types.is_numeric_dtype(df[col]):
                        mean_val = df[col].mean()
                        df[col].fillna(mean_val, inplace=True)
                message = f"Nulos rellenados con la media en columna(s): {selected_column}."

            elif selected_strategy == "Rellenar con Mediana (Numérico)":
                target_columns = [selected_column] if selected_column != "Todas las columnas" else df.columns
                for col in target_columns:
                    if pd.api.types.is_numeric_dtype(df[col]):
                        median_val = df[col].median()
                        df[col].fillna(median_val, inplace=True)
                message = f"Nulos rellenados con la mediana en columna(s): {selected_column}."

            elif selected_strategy == "Rellenar con Moda (Numérico/Categórico)":
                target_columns = [selected_column] if selected_column != "Todas las columnas" else df.columns
                for col in target_columns:
                    # Moda puede devolver múltiples valores, tomamos el primero
                    mode_val = df[col].mode()[0] if not df[col].mode().empty else None
                    if mode_val is not None:
                        df[col].fillna(mode_val, inplace=True)
                message = f"Nulos rellenados con la moda en columna(s): {selected_column}."

            elif selected_strategy == "Eliminar Filas (Cualquier nulo)":
                df.dropna(how='any', inplace=True)
                message = "Filas con al menos un valor nulo eliminadas."

            elif selected_strategy == "Eliminar Filas (Todos los nulos)":
                df.dropna(how='all', inplace=True)
                message = "Filas con todos los valores nulos eliminadas."

            else:
                self.show_notification("Estrategia no reconocida.", ft.Colors.RED)
                return

            # Actualiza el DataFrame copiado
            self.app_state.load_dataframe_copy(df)
            final_nulls = df.isnull().sum().sum()
            final_rows = len(df)

            self.show_notification(message, ft.Colors.GREEN)
            self.manipulation_results.controls.append(ft.Text(f"✔️ Operación: {selected_strategy}"))
            self.manipulation_results.controls.append(ft.Text(f"Nulos antes: {initial_nulls}, Nulos después: {final_nulls}"))
            if initial_rows != final_rows:
                self.manipulation_results.controls.append(ft.Text(f"Filas antes: {initial_rows}, Filas después: {final_rows} (Se eliminaron {initial_rows - final_rows} filas)."))

            # Muestra información de nulos después de la operación en la sección de manipulados
            self.show_manipulated_data_info("nulls_percent")
            self._hide_null_handling_options()

        except Exception as ex:
            self.show_notification(f"Error al aplicar manejo de nulos: {str(ex)}", ft.Colors.RED)
            self.manipulation_results.controls.append(
                ft.Text(f"❌ Error al aplicar manejo de nulos: {str(ex)}", color=ft.Colors.RED)
            )

        if self.page:
            self.page.update()

    def _show_rename_column_options(self, e=None):
        """
        Muestra los controles para renombrar una columna y carga las columnas del DataFrame.
        """
        
        # Limpia solo los resultados de manipulación
        self.manipulation_results.controls = [
            ft.Text("Resultados de Manipulación de Datos Básicos:", weight=ft.FontWeight.BOLD)
        ]
        # Oculta otros controles de manipulación
        self.object_type_conversion_controls.visible = False
        self.null_handling_controls.visible = False
        self.rename_column_controls.visible = True

        df = self.app_state.get_active_dataframe()
        if df is None:
            self.show_notification("No hay datos cargados o copiados para renombrar columnas.", ft.Colors.ORANGE)
            self.rename_column_controls.visible = False
            if self.page:
                self.page.update()
            return

        # Cargar opciones de columnas en el dropdown de renombrado
        column_options = [ft.dropdown.Option(col) for col in df.columns]
        self.rename_column_dropdown.options = column_options
        self.rename_column_dropdown.value = None
        self.new_column_name_textfield.value = ""

        self.show_notification("Seleccione una columna para renombrar.", ft.Colors.BLUE)
        if self.page:
            self.page.update()

    def _hide_rename_column_options(self, e=None):
        """Oculta los controles de renombrado de columnas."""
        self.rename_column_controls.visible = False
        if self.page:
            self.page.update()

    def _apply_rename_column(self, e=None):
        """
        Aplica el renombramiento de la columna seleccionada.
        """
        
        # Limpia solo los resultados de manipulación
        self.manipulation_results.controls = [ 
            ft.Text("Resultados de Manipulación de Datos Básicos:", weight=ft.FontWeight.BOLD)
        ]
        df = self.app_state.get_active_dataframe()
        if df is None:
            self.show_notification("No hay datos para renombrar columnas.", ft.Colors.ORANGE)
            return

        old_column_name = self.rename_column_dropdown.value
        new_column_name = (self.new_column_name_textfield.value or "").strip()

        if not old_column_name:
            self.show_notification("Por favor, seleccione una columna existente.", ft.Colors.ORANGE)
            return
        if not new_column_name:
            self.show_notification("Por favor, ingrese un nuevo nombre para la columna.", ft.Colors.ORANGE)
            return
        if old_column_name == new_column_name:
            self.show_notification("El nuevo nombre es el mismo que el anterior. No se realizó ningún cambio.", ft.Colors.ORANGE)
            return
        if new_column_name in df.columns.tolist() and new_column_name != old_column_name:
            self.show_notification(f"El nombre '{new_column_name}' ya existe como columna. Elija uno diferente.", ft.Colors.ORANGE)
            return

        try:
            df.rename(columns={old_column_name: new_column_name}, inplace=True)
            
            # Actualiza el DataFrame copiado
            self.app_state.load_dataframe_copy(df) 

            self.show_notification(f"Columna '{old_column_name}' renombrada a '{new_column_name}' exitosamente.", ft.Colors.GREEN)
            self.manipulation_results.controls.append(
                ft.Text(f"✔️ Columna '{old_column_name}' renombrada a '{new_column_name}'.")
            )
            # Después de renombrar, muestra los nombres de columnas actualizados en la sección de manipulados
            self.show_manipulated_data_info("column_names")
            self._hide_rename_column_options()

        except Exception as ex:
            self.show_notification(f"Error al renombrar columna '{old_column_name}': {str(ex)}", ft.Colors.RED)
            self.manipulation_results.controls.append(
                ft.Text(f"❌ Error al renombrar columna '{old_column_name}': {str(ex)}", color=ft.Colors.RED)
            )

        if self.page:
            self.page.update()

    def _show_dataframe_table(self, df_type: str):
        """
        Muestra una vista previa del DataFrame (original o manipulado) en una tabla.
        """
        if df_type == "original":
            # Limpiar resultados anteriores
            self._clear_results()
            df = self.app_state.get_original_dataframe()
            target_results_container = self.validation_results
            title_text = "Vista Previa del Dataset Original:"
        elif df_type == "manipulated":
            # Limpiar resultados anteriores
            self._clear_results()
            df = self.app_state.get_active_dataframe()
            target_results_container = self.manipulated_validation_results
            title_text = "Vista Previa del Dataset Manipulado:"
        else:
            self.show_notification("Tipo de DataFrame no reconocido para mostrar tabla.", ft.Colors.RED)
            return

        if df is None:
            self.show_notification(f"No hay datos {df_type} para mostrar en tabla.", ft.Colors.ORANGE)
            return

        # Limpiar resultados anteriores en el contenedor objetivo
        current_controls = [
            control for control in target_results_container.controls
            if not (isinstance(control, ft.DataTable) or (isinstance(control, ft.Text) and control.value is not None and "Vista Previa" in control.value))
        ]
        target_results_container.controls = current_controls
        target_results_container.controls.append(ft.Text(title_text, weight=ft.FontWeight.BOLD))

        # Limitar a las primeras 10 filas para una vista previa manejable
        preview_df = df.head(10)

        columns = [
            ft.DataColumn(ft.Text(col, weight=ft.FontWeight.BOLD)) for col in preview_df.columns
        ]
        rows = []
        for index, row in preview_df.iterrows():
            cells = [ft.DataCell(ft.Text(str(row[col]), selectable=True)) for col in preview_df.columns]
            rows.append(ft.DataRow(cells))

        data_table = ft.DataTable(
            columns=columns,
            rows=rows,
            border=ft.border.all(1, ft.Colors.GREY_200),
            vertical_lines=ft.BorderSide(1, ft.Colors.GREY_200),
            horizontal_lines=ft.BorderSide(1, ft.Colors.GREY_200),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=ft.Colors.BLUE_GREY_100,
            show_checkbox_column=False,
            width=len(preview_df.columns) * 150 if len(preview_df.columns) > 5 else None
        )

        # Envuelve la tabla en un ft.Column para darle scroll si es necesario
        table_container = ft.Column(
            controls=[data_table],
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True,
            height=300
        )

        target_results_container.controls.append(table_container)
        if len(df) > 10:
            target_results_container.controls.append(ft.Text(f"... y {len(df) - 10} filas más. Mostrando solo las primeras 10.", size=12, color=ft.Colors.GREY_500))

        self.show_notification(f"Mostrando vista previa del DataFrame {df_type}.", ft.Colors.BLUE)
        if self.page:
            self.page.update()

    def _export_dataframe_csv(self, e=None):
        """
        Exporta el DataFrame manipulado a un archivo CSV con el nombre original más '_mugenC.csv'.
        """
        df = self.app_state.get_active_dataframe()
        if df is None:
            self.show_notification("No hay un DataFrame manipulado para exportar.", ft.Colors.ORANGE)
            return

        original_file_name = self.app_state.get_original_dataframe_name()
        if not original_file_name:
            # Si no hay nombre original (ej., si se creó la copia sin un archivo base)
            export_name = "exported_data_mugenC.csv"
        else:
            # Eliminar la extensión original y añadir la nueva
            base_name = original_file_name.rsplit('.', 1)[0] if '.' in original_file_name else original_file_name
            export_name = f"{base_name}_mugenC.csv"

        try:
            # Set the on_result handler temporarily for saving
            self.file_picker.on_result = lambda event: self._handle_file_save_result(event, df)
            # Use FilePicker to select the save path
            self.file_picker.save_file(
                file_name=export_name,
                allowed_extensions=["csv"],
                dialog_title="Guardar Dataset Manipulado como CSV"
            )

        except Exception as ex:
            self.show_notification(f"Error al preparar la exportación: {str(ex)}", ft.Colors.RED)
            print(f"Error al preparar la exportación: {str(ex)}")

        if self.page:
            self.page.update()

    def _handle_file_save_result(self, e: ft.FilePickerResultEvent, df: pd.DataFrame):
        """
        Maneja el resultado del diálogo de guardado de archivo para la exportación.
        """
        if e.path:
            try:
                df.to_csv(e.path, index=False)
                self.show_notification(f"Dataset exportado exitosamente a: {e.path}", ft.Colors.GREEN)
            except Exception as ex:
                self.show_notification(f"Error al guardar el archivo: {str(ex)}", ft.Colors.RED)
                print(f"Error al guardar el archivo: {str(ex)}")
        else:
            self.show_notification("Exportación cancelada.", ft.Colors.ORANGE)

        self.file_picker.on_result = self.handle_file_picker_result
        if self.page:
            self.page.update()