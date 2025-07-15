from fpdf import FPDF
import matplotlib.pyplot as plt
from io import BytesIO
import tempfile
import os

class PDF(FPDF):
    def __init__(self, tipo_agrupacion):
        super().__init__()
        self.tipo_agrupacion = tipo_agrupacion
        self.imagenes_temp = []  # para limpiar luego

    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Resumen de Ventas - Artisan Burguer", ln=True, align="C")
        self.set_font("Arial", "", 10)
        self.cell(0, 10, f"Tipo de agrupación: {self.tipo_agrupacion}", ln=True, align="C")
        self.ln(5)

    def leyendas_productos(self, productos, cantidades, colores):
        self.set_font("Arial", "B", 10)
        self.cell(0, 10, "Productos seleccionados:", ln=True)
        self.set_font("Arial", "", 9)

        for i in range(0, len(productos), 2):
            linea = ""
            for j in range(2):
                if i + j < len(productos):
                    producto = productos[i + j]
                    cantidad = cantidades[i + j]
                    color = colores[i + j]
                    color_hex = '#%02x%02x%02x' % tuple(int(c * 255) for c in color)
                    linea += f"- {producto} ({cantidad:.1f} und)   ".ljust(45)
            self.cell(0, 8, linea, ln=True)
        self.ln(5)

    def insertar_grafico(self, fig, x, y):
        tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        fig.savefig(tmpfile.name, format='png', dpi=150, bbox_inches='tight')
        self.imagenes_temp.append(tmpfile.name)  # guardamos para borrar después
        self.image(tmpfile.name, x=x, y=y, w=60)

    def insertar_tabla_resumen(self, resumen_df):
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 10, "Resumen por Producto", ln=True)
        self.ln(4)

        # Encabezados
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(230, 230, 230)
        self.cell(100, 8, "Producto", border=1, fill=True)
        self.cell(30, 8, "Cantidad", border=1, fill=True)
        self.cell(40, 8, "Monto", border=1, ln=True, fill=True)

    # Filas
        self.set_font("Helvetica", "", 9)
        for index, row in resumen_df.iterrows():
            producto = str(row["Producto"])
            cantidad = str(row["Cantidad"])
            monto = str(row["Monto"])

            # Calcular altura necesaria según el texto
            line_height = 8
            producto_height = self.get_string_width(producto) / 90
            lines = int(producto_height) + 1

            # Verificar salto de página
            if self.get_y() + (line_height * lines) > 270:
                self.add_page()
                self.set_font("Helvetica", "B", 9)
                self.set_fill_color(230, 230, 230)
                self.cell(100, 8, "Producto", border=1, fill=True)
                self.cell(30, 8, "Cantidad", border=1, fill=True)
                self.cell(40, 8, "Monto", border=1, ln=True, fill=True)
                self.set_font("Helvetica", "", 9)

            # Guardar posición actual
            x = self.get_x()
            y = self.get_y()

            # Insertar celdas alineadas
            self.multi_cell(100, line_height, producto, border=1)
            self.set_xy(x + 100, y)
            self.cell(30, line_height * lines, cantidad, border=1)
            self.cell(40, line_height * lines, monto, border=1, ln=True)


def exportar_pdf(resumen, agrupaciones, df_agrupado, campo_agrupacion, productos_seleccionados, tipo_agrupacion):
    pdf = PDF(tipo_agrupacion)
    pdf.add_page()
    pdf.insertar_tabla_resumen(resumen)

    colores = plt.get_cmap("tab10").colors
    mapa_colores = {prod: colores[i % len(colores)] for i, prod in enumerate(productos_seleccionados)}
    cantidades = [resumen[resumen["Producto"] == p]["Cantidad"].values[0] for p in productos_seleccionados]
    colores_lista = [mapa_colores[p] for p in productos_seleccionados]

    pdf.leyendas_productos(productos_seleccionados, cantidades, colores_lista)

    # Dibujar gráficos de torta
    x_positions = [15, 75, 135]
    y = pdf.get_y()
    contador = 0

    for agrupador in agrupaciones:
        datos = df_agrupado[df_agrupado[campo_agrupacion] == agrupador]
        if datos.empty:
            continue

        cantidades = datos["Cantidad"].tolist()
        productos = datos["Producto"].tolist()
        colores_locales = [mapa_colores.get(p, (0.5, 0.5, 0.5)) for p in productos]

        fig, ax = plt.subplots(figsize=(2, 2))
        ax.pie(cantidades, labels=None, colors=colores_locales, startangle=90)
        ax.set_title(str(agrupador), fontsize=8)

        x = x_positions[contador % 3]
        pdf.insertar_grafico(fig, x, y)

        contador += 1
        if contador % 3 == 0:
            y += 60
            if y > 240:
                pdf.add_page()
                y = 20

    # Guardar PDF como binario
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    buffer = BytesIO(pdf_bytes)

    # ✅ Limpiar imágenes temporales
    for img in pdf.imagenes_temp:
        try:
            os.remove(img)
        except Exception:
            pass

    return buffer
