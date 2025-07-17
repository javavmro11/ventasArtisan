import streamlit as st
import sys
import os

# 👉 Agrega la ruta al proyecto para importar src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.cargar_datos import cargar_datos
from src.filtro_productos import cargar_productos_validos, filtrar_productos
from src.procesar_datos import interfaz_procesar

st.set_page_config(page_title="Ventas Artisan", layout="wide")
st.title("📊 Reporte de Ventas Semanales - Artisan")

# 🏪 Selección de punto de venta
opciones_sucursal = {
    "Artisan Chía": ("data/data_chia.xlsx", "config/productos_validos_chia.txt"),
    "Artisan Express": ("data/data_express.xlsx", "config/productos_validos_express.txt"),
    "Artisan Cajicá": ("data/data_cajica.xlsx", "config/productos_validos_cajica.txt")
}

sucursal = st.selectbox("🏪 Selecciona el punto de venta", list(opciones_sucursal.keys()))

if sucursal:
    archivo_excel, archivo_txt = opciones_sucursal[sucursal]

    df_limpio = cargar_datos(archivo_excel)

    if df_limpio.empty:
        st.warning("⚠️ No se pudo cargar el archivo de ventas.")
    else:
        st.success(f"✅ Archivo de ventas para {sucursal} cargado correctamente.")
        st.write(f"Registros totales: {len(df_limpio)}")

        productos_validos = cargar_productos_validos(archivo_txt)

        if productos_validos:
            df_filtrado = filtrar_productos(df_limpio, productos_validos)

            st.markdown("---")
            # 🔁 Ahora pasamos también el nombre de la sucursal:
            interfaz_procesar(df_filtrado, nombre_sucursal=sucursal)
        else:
            st.warning("⚠️ No se encontraron productos válidos para esta sucursal.")
