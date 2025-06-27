from src.cargar_datos import cargar_datos
from src.filtro_productos import cargar_productos_validos, filtrar_productos

# Paso 1: Cargar el archivo limpio
df_limpio = cargar_datos()

# Paso 2: Cargar productos válidos desde el archivo .txt
productos_validos = cargar_productos_validos()

# Paso 3: Filtrar los productos
df_final = filtrar_productos(df_limpio, productos_validos)

# Mostrar los resultados
print(f"\n✅ Filas totales después del filtro: {len(df_final)}")
print(df_final.head(10))