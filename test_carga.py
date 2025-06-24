from src.cargar_datos import cargar_datos
from src.filtro_productos import cargar_productos_validos, filtrar_productos

# Cargar el DataFrame limpio
df = cargar_datos()

# Cargar productos válidos desde TXT
productos_validos = cargar_productos_validos()

# Aplicar el filtro
df_filtrado = filtrar_productos(df, productos_validos)

# Mostrar resultados
print(f"\n✅ Se encontraron {len(df_filtrado)} filas para los productos válidos:")
print(df_filtrado.head(15))
