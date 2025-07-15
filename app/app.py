import streamlit as st
import sys
import os

# 👉 Agrega la ruta al proyecto para importar src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.cargar_datos import cargar_datos
from src.filtro_productos import cargar_productos_validos, filtrar_productos
from src.procesar_datos import interfaz_procesar  # ✅ Esta debe estar al final, luego de verificar ruta

st.set_page_config(page_title="Ventas Artisan", layout="wide")
st.title("📊 Reporte de Ventas Semanales - Artisan")

# 📁 Subida de archivo
archivo = st.file_uploader("📁 Sube el archivo Excel con las ventas", type=["xlsx"])

if archivo:
    df_limpio = cargar_datos(archivo)

    if df_limpio.empty:
        st.warning("⚠️ El archivo no tiene datos válidos.")
    else:
        st.success("✅ Archivo cargado correctamente.")
        st.write(f"Registros totales: {len(df_limpio)}")

        productos_validos = cargar_productos_validos()

        if productos_validos:
            df_filtrado = filtrar_productos(df_limpio, productos_validos)

            # ✅ Solo se muestra la interfaz final
            st.markdown("---")
            interfaz_procesar(df_filtrado)
        else:
            st.warning("⚠️ No se encontraron productos válidos en config/productos_validos.txt")
else:
    st.info("⬆️ Por favor sube un archivo Excel para comenzar.")
