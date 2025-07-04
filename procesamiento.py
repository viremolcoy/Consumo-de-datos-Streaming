import pandas as pd

def limpiar_datos(df):
    df = df.copy()

    # Eliminar duplicados exactos
    df = df.drop_duplicates()

    # Convertir tipos
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')
    df['monto'] = pd.to_numeric(df['monto'], errors='coerce')

    # Eliminar filas con valores nulos esenciales
    df = df.dropna(subset=['id_cliente', 'id_producto', 'precio', 'cantidad', 'monto'])

    # Estándar en texto
    df['cliente'] = df['cliente'].str.strip().str.title()
    df['producto'] = df['producto'].str.strip().str.title()
    df['forma_pago'] = df['forma_pago'].str.strip().str.capitalize()

    # Ordenar por fecha
    df['fecreg'] = pd.to_datetime(df['fecreg'], errors='coerce')
    df = df.dropna(subset=['fecreg'])
    df = df.sort_values(by='fecreg')

    return df
