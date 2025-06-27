import streamlit as st
import sys
import os

# 👇 Agregar ruta al proyecto para importar src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.cargar_datos import cargar_datos
from src.filtro_productos import cargar_productos_validos, filtrar_productos

st.set_page_config(page_title="Ventas Artisan", layout="wide")

st.title("📊 Reporte de Ventas Semanales - Artisan")

# 📁 Subida de archivo
archivo = st.file_uploader("📁 Sube el archivo Excel con las ventas", type=["xlsx"])

if archivo:
    # 🧼 Cargar y limpiar archivo
    df_limpio = cargar_datos(archivo)

    if df_limpio.empty:
        st.warning("⚠️ El archivo no tiene datos válidos.")
    else:
        st.success("✅ Archivo cargado correctamente.")
        st.write(f"Registros totales: {len(df_limpio)}")

        # 🔍 Mostrar productos encontrados (opcional)
        st.subheader("🛒 Productos encontrados en el archivo:")
        productos_unicos = sorted(df_limpio['Producto'].unique())
        st.write(productos_unicos)

        # 📂 Cargar productos válidos desde TXT
        productos_validos = cargar_productos_validos()

        if productos_validos:
            # ✅ Filtrar por productos válidos
            df_filtrado = filtrar_productos(df_limpio, productos_validos)

            # 🗂️ Mostrar categorías disponibles
            categorias = sorted(df_filtrado['CATEGORÍA'].unique())
            categoria_seleccionada = st.multiselect("🎯 Filtrar por categoría:", categorias, default=categorias)

            # Filtrar por categorías seleccionadas
            df_filtrado = df_filtrado[df_filtrado['CATEGORÍA'].isin(categoria_seleccionada)]

            st.subheader("📋 Resultados filtrados:")
            st.write(f"Registros después del filtro: {len(df_filtrado)}")
            st.dataframe(df_filtrado.head(20))

        else:
            st.warning("⚠️ No se encontraron productos válidos en config/productos_validos.txt")
else:
    st.info("⬆️ Por favor sube un archivo Excel para comenzar.")