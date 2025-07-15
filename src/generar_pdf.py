from fpdf import FPDF
import matplotlib.pyplot as plt
from io import BytesIO
import os
import tempfile

class PDF(FPDF):
    def __init__(self, tipo_agrupacion):
        super().__init__()
        self.tipo_agrupacion = tipo_agrupacion

    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Resumen de Ventas - Artisan Burguer", ln=True, align="C")
        self.set_font("Arial", "", 10)
        self.cell(0, 10, f"Tipo de agrupación: {self.tipo_agrupacion}", ln=True, align="C")
        self.ln(5)

    def leyendas_productos(self, productos):
        self.set_font("Arial", "B", 10)
        self.cell(0, 10, "Productos seleccionados:", ln=True)
        self.set_font("Arial", "", 10)

        for i in range(0, len(productos), 2):
            linea = "  - " + productos[i]
            if i + 1 < len(productos):
                linea += "     |     - " + productos[i + 1]
            self.cell(0, 8, linea, ln=True)
        self.ln(3)

    def insertar_grafico(self, fig):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            fig.savefig(tmpfile.name, format='png', dpi=150, bbox_inches='tight')
            tmpfile.flush()
            self.image(tmpfile.name, w=60)  # tamaño pequeño para 3 por fila

        # 🔁 Elimina el archivo después de cerrar la figura (fuera del with)
        try:
            os.unlink(tmpfile.name)
        except PermissionError:
            pass  # Windows a veces bloquea el archivo si se usa muy rápido temporal

def exportar_pdf(resumen, agrupaciones, df_agrupado, campo_agrupacion, productos_seleccionados, tipo_agrupacion):
    pdf = PDF(tipo_agrupacion)
    pdf.add_page()

    # ✅ Leyendas de productos seleccionados
    pdf.leyendas_productos(productos_seleccionados)

    # ✅ Gráficos por agrupación (3 por fila)
    colores = plt.get_cmap("tab10").colors
    mapa_colores = {prod: colores[i % len(colores)] for i, prod in enumerate(productos_seleccionados)}

    contador = 0
    for agrupador in agrupaciones:
        datos = df_agrupado[df_agrupado[campo_agrupacion] == agrupador]
        if datos.empty:
            continue

        cantidades = datos["Cantidad"].tolist()
        productos = datos["Producto"].tolist()
        colores_locales = [mapa_colores.get(p, (0.5, 0.5, 0.5)) for p in productos]

        fig, ax = plt.subplots(figsize=(2.2, 2.2))
        ax.pie(cantidades, labels=None, colors=colores_locales, startangle=90, textprops={'fontsize': 6})
        ax.set_title(str(agrupador), fontsize=8)

        if contador % 3 == 0 and contador != 0:
            pdf.ln(55)
        pdf.insertar_grafico(fig)
        contador += 1

    # ✅ Codificación como binario para descargar en Streamlit
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    return BytesIO(pdf_bytes)