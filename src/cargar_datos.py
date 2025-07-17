import pandas as pd
import os

def cargar_datos(ruta_archivo):
    """
    Carga y limpia el archivo Excel de ventas.
    Conserva solo: Fecha, Producto, Cantidad, Total.
    Si falla, retorna un DataFrame vacío y lanza el error por consola o Streamlit.
    """
    try:
        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError(f"❌ El archivo no existe: {ruta_archivo}")

        df = pd.read_excel(ruta_archivo, engine='openpyxl')

        columnas_requeridas = ['Fecha', 'Producto', 'Cantidad', 'Total']
        for col in columnas_requeridas:
            if col not in df.columns:
                raise ValueError(f"❌ Falta la columna requerida: '{col}'")

        df = df[columnas_requeridas].copy()
        df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
        df = df.dropna(subset=columnas_requeridas)
        df['Producto'] = df['Producto'].str.strip()
        df = df.sort_values(by='Fecha').reset_index(drop=True)

        return df

    except Exception as e:
        try:
            import streamlit as st
            st.error(f"❌ Error al cargar datos: {e}")
        except:
            print(f"❌ Error al cargar datos: {e}")
        return pd.DataFrame()
