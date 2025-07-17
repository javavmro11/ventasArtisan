import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt
from io import BytesIO
from src.generar_pdf import exportar_pdf

def formatear_miles(valor):
    return f"${valor:,.0f}".replace(",", ".") + " $"

# 🟡 Ahora recibe nombre_sucursal como argumento
def interfaz_procesar(df_filtrado, nombre_sucursal=""):
    st.header("📊 Procesamiento de Datos")
    df_filtrado = df_filtrado.copy()
    if 'Total' in df_filtrado.columns:
        df_filtrado.rename(columns={"Total": "Monto"}, inplace=True)

    opciones = {
        "Por día": "D",
        "Por semana": "W",
        "Por rango de fechas": "R"
    }

    agrupacion = st.radio("¿Cómo deseas agrupar las ventas?", list(opciones.keys()))
    campo_agrupacion = "Agrupador"

    if agrupacion == "Por rango de fechas":
        col1, col2 = st.columns(2)
        fecha_inicio = col1.date_input("Desde", value=df_filtrado["Fecha"].min().date())
        fecha_fin = col2.date_input("Hasta", value=df_filtrado["Fecha"].max().date())
        rango_dias = (fecha_fin - fecha_inicio).days + 1

        df_filtrado = df_filtrado[
            (df_filtrado["Fecha"].dt.date >= fecha_inicio) & 
            (df_filtrado["Fecha"].dt.date <= fecha_fin)
        ]

        if rango_dias > 7:
            df_filtrado["Semana"] = df_filtrado["Fecha"].dt.to_period("W").apply(lambda r: r.start_time)
            semanas = sorted(df_filtrado["Semana"].unique())
            semana_labels = {
                fecha: f"Semana {i + 1} - ({fecha.strftime('%d/%m')} - {(fecha + pd.Timedelta(days=6)).strftime('%d/%m')})"
                for i, fecha in enumerate(semanas)
            }
            df_filtrado["Agrupador"] = df_filtrado["Semana"].map(semana_labels)
        else:
            df_filtrado["Agrupador"] = "Rango personalizado"
    elif agrupacion == "Por semana":
        df_filtrado["Semana"] = df_filtrado["Fecha"].dt.to_period("W").apply(lambda r: r.start_time)
        semanas = sorted(df_filtrado["Semana"].unique())
        semana_labels = {
            fecha: f"Semana {i + 1} - ({fecha.strftime('%d/%m')} - {(fecha + pd.Timedelta(days=6)).strftime('%d/%m')})"
            for i, fecha in enumerate(semanas)
        }
        df_filtrado["Agrupador"] = df_filtrado["Semana"].map(semana_labels)
    else:
        df_filtrado["Agrupador"] = df_filtrado["Fecha"].dt.strftime("%d/%m/%Y")

    productos_disponibles = sorted(df_filtrado["Producto"].unique().tolist())
    productos_seleccionados = st.multiselect(
        "Selecciona hasta 10 productos para comparar:",
        productos_disponibles,
        max_selections=100
    )

    if st.button("🚀 Procesar"):
        df_filtrado = df_filtrado[df_filtrado["Producto"].isin(productos_seleccionados)]

        df_agrupado = df_filtrado.groupby([campo_agrupacion, "Producto"]).agg(
            Cantidad=("Cantidad", "sum"),
            Monto=("Monto", "sum")
        ).reset_index()

        resumen = df_agrupado.groupby("Producto").agg(
            Cantidad=("Cantidad", "sum"),
            Monto=("Monto", "sum")
        ).reset_index().sort_values(by="Cantidad", ascending=False)

        resumen["Monto"] = resumen["Monto"].apply(formatear_miles)

        st.session_state["resumen"] = resumen
        st.session_state["df_agrupado"] = df_agrupado
        st.session_state["agrupaciones"] = df_agrupado[campo_agrupacion].unique()
        st.session_state["campo_agrupacion"] = campo_agrupacion
        st.session_state["productos_seleccionados"] = productos_seleccionados
        st.session_state["tipo_agrupacion"] = agrupacion

    if "resumen" in st.session_state:
        st.subheader("📌 Resumen por Producto")
        st.dataframe(st.session_state["resumen"], use_container_width=True, hide_index=True)

        st.subheader("📉 Gráficos de Productos")
        st.markdown("**🔷 Productos seleccionados:**")
        colores = plt.get_cmap("tab10").colors
        mapa_colores = {
            prod: colores[i % len(colores)]
            for i, prod in enumerate(st.session_state["productos_seleccionados"])
        }

        n_columnas = 7
        columnas = st.columns(n_columnas)

        for idx, producto in enumerate(st.session_state["productos_seleccionados"]):
            color = mapa_colores.get(producto, (0.5, 0.5, 0.5))
            color_hex = '#%02x%02x%02x' % tuple(int(c * 255) for c in color)
            cantidad_total = df_filtrado[df_filtrado["Producto"] == producto]["Cantidad"].sum()
            col = columnas[idx % n_columnas]
            col.markdown(
                f"<span style='font-size:12px; color:{color_hex}'>●</span> "
                f"<span style='font-size:12px'>{producto} - {cantidad_total:.1f} und</span>",
                unsafe_allow_html=True
            )

        columnas = st.columns(3)
        for i, agrupador in enumerate(st.session_state["agrupaciones"]):
            datos = st.session_state["df_agrupado"][st.session_state["df_agrupado"][campo_agrupacion] == agrupador]
            cantidades = datos["Cantidad"].tolist()
            productos = datos["Producto"].tolist()
            colores_locales = [mapa_colores.get(p, (0.5, 0.5, 0.5)) for p in productos]

            fig, ax = plt.subplots(figsize=(1.8, 1.8))
            ax.pie(cantidades, labels=None, colors=colores_locales, startangle=90)
            titulo = (
                f"<div style='text-align:center; font-size:12px; font-weight:bold;'>"
                f"{agrupador}<br>{sum(cantidades):.1f} und<br>{formatear_miles(datos['Monto'].sum())}</div>"
            )
            columnas[i % 3].markdown(titulo, unsafe_allow_html=True)
            columnas[i % 3].pyplot(fig)

        st.subheader("📤 Exportar análisis a PDF")
        if st.button("📄 Exportar a PDF"):
            buffer = exportar_pdf(
                resumen=st.session_state["resumen"],
                productos_seleccionados=st.session_state["productos_seleccionados"],
                tipo_agrupacion=st.session_state["tipo_agrupacion"],
                agrupaciones=st.session_state["agrupaciones"],
                df_agrupado=st.session_state["df_agrupado"],
                campo_agrupacion=st.session_state["campo_agrupacion"],
                nombre_sucursal=nombre_sucursal  # ✅ nuevo argumento
            )

            st.download_button(
                label="📥 Descargar PDF",
                data=buffer,
                file_name="resumen_ventas.pdf",
                mime="application/pdf"
            )
