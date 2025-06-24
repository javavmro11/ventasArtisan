def productos_unicos(df):
    """
    Extrae y retorna una lista ordenada de productos únicos del DataFrame.

    Parámetros:
        df (pd.DataFrame): DataFrame limpio con columna 'Producto'.

    Retorna:
        list: Lista de productos únicos ordenados alfabéticamente.
    """
    if 'Producto' not in df.columns:
        print("❌ El DataFrame no contiene la columna 'Producto'.")
        return []

    # Quitar nulos por si acaso
    productos = df['Producto'].dropna().unique()

    # Ordenar alfabéticamente
    productos_ordenados = sorted(productos)

    return productos_ordenados
