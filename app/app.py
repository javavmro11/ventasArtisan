import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from src.cargar_datos import cargar_datos
from src.filtro_productos import cargar_productos_validos, filtrar_productos

st.set_page_config(page_title="Ventas Artisan", layout="wide")

st.title("📊 Reporte de Ventas Semanales - Artisan")

# Paso 1: Cargar archivo
archivo = st.file_uploader("📁 Sube el archivo Excel con las ventas", type=["xlsx"])

if archivo:
    df_limpio = cargar_datos(archivo)

    if df_limpio.empty:
        st.warning("⚠️ El archivo no tiene datos válidos.")
    else:
        # Mostrar productos encontrados (opcional)
        st.subheader("🛒 Productos en el archivo:")
        productos_unicos = df_limpio['Producto'].unique()
        st.write(sorted(productos_unicos))

        # Paso 2: Cargar productos válidos desde TXT
        productos_validos = cargar_productos_validos()

        if productos_validos:
            df_filtrado = filtrar_productos(df_limpio, productos_validos)

            st.success(f"✅ Registros filtrados: {len(df_filtrado)}")
            st.dataframe(df_filtrado)

        else:
            st.warning("⚠️ No se encontraron productos válidos en config/productos_validos.txt")
