import pandas as pd
import os

def cargar_datos(ruta_archivo="data/data.xlsx"):
    """
    Carga y limpia el archivo de ventas, quedándose solo con las columnas:
    Fecha, Producto, Cantidad y Total, y las ordena por fecha ascendente.

    Parámetros:
        ruta_archivo (str): Ruta del archivo Excel a cargar.

    Retorna:
        pd.DataFrame: DataFrame limpio y ordenado por fecha, o vacío si hay error.
    """
    try:
        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError(f"El archivo no existe en la ruta: {ruta_archivo}")

        # Leer el archivo Excel con openpyxl
        df = pd.read_excel(ruta_archivo, engine='openpyxl')

        columnas_requeridas = ['Fecha', 'Producto', 'Cantidad', 'Total']
        for col in columnas_requeridas:
            if col not in df.columns:
                raise ValueError(f"Falta la columna requerida: {col}")

        df = df[columnas_requeridas].copy()

        # Convertir a datetime y eliminar vacíos
        df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
        df = df.dropna(subset=columnas_requeridas)

        # Limpiar espacios en productos
        df['Producto'] = df['Producto'].str.strip()

        # Ordenar por fecha ascendente
        df = df.sort_values(by='Fecha', ascending=True).reset_index(drop=True)

        return df

    except Exception as e:
        print(f"❌ Error al cargar el archivo: {e}")
        return pd.DataFrame()
