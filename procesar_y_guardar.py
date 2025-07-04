import pandas as pd
from procesamiento import limpiar_datos  # archivo con la función que definimos antes

# Cargar los datos recibidos en bruto
df_original = pd.read_csv("datos_realtime.csv")

# Limpiar
df_limpio = limpiar_datos(df_original)

# Guardar en nuevo archivo
df_limpio.to_csv("datos_limpiados.csv", index=False)

print("✅ Datos procesados y guardados como datos_limpiados.csv")
