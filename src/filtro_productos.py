def cargar_productos_validos(ruta_txt='config/productos_validos.txt'):
    """
    Lee el archivo productos_validos.txt y devuelve la lista de productos permitidos.

    Parámetros:
        ruta_txt (str): Ruta al archivo con los nombres válidos.

    Retorna:
        list: Lista de productos válidos.
    """
    try:
        with open(ruta_txt, 'r', encoding='utf-8') as f:
            productos = [line.strip() for line in f if line.strip()]
        return productos
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {ruta_txt}")
        return []
    except Exception as e:
        print(f"❌ Error al leer productos válidos: {e}")
        return []

def filtrar_productos(df, lista_productos_validos):
    """
    Filtra el DataFrame para dejar solo las filas con productos válidos.

    Parámetros:
        df (pd.DataFrame): DataFrame con columna 'Producto'.
        lista_productos_validos (list): Lista de productos válidos.

    Retorna:
        pd.DataFrame: DataFrame filtrado.
    """
    if 'Producto' not in df.columns:
        print("❌ El DataFrame no contiene la columna 'Producto'.")
        return df

    df_filtrado = df[df['Producto'].isin(lista_productos_validos)].copy()
    return df_filtrado
