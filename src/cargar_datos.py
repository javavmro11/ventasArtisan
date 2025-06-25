import pandas as pd
import os

def cargar_datos(ruta_archivo):
    try:
        if not ruta_archivo:
            raise ValueError("⚠️ No se ha proporcionado un archivo válido.")

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
        import streamlit as st
        st.error(str(e))
        return pd.DataFrame()
