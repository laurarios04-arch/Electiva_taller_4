# Práctica 1. ETL dentro del contenedor
import pandas as pd

df = pd.read_csv(
    "data/Visitas_PIT_Boyaca.csv",
    encoding="utf-8"
)

# Líneas para pruebas de lectura del csv y verificar variables
# Inicio de pruebas de lectura
print(df.head())

print(df.shape) 
print(df.info())

# Fin de pruebas de lectura 

# Identificación de valores faltantes
# Inicio de pruebas valores faltantes
print("Valores faltantes")
print(df.isnull().sum())

# Fin de pruebas valores faltantes

df.columns = (
    df.columns
    .str.strip()
    .str.upper()
)
# Estandarización de nombre de columnas
# Inicio de pruebas de nombre de columnas
print(df.columns)
# Fin de pruebas de nombre de columnas

# Eliminar espacios en blanco
columnas_texto = df.select_dtypes( include='object' ).columns 

for col in columnas_texto: df[col] = df[col].str.strip()

# Pruebas para verificar tipos de datos
# Inicio pruebas tipos de datos
print(df.dtypes)
# Fin pruebas tipos de datos

# Guardar temporalmente los datos transformados
df.to_csv(
    "outputs/turismo_limpio.csv",
    index=False
)

df.to_parquet(
    "outputs/turismo.parquet",
    index=False
)

print("Dataset transformado correctamente")

# Bloque de pruebas de lectura archivo parquet
# Inicio de pruebas de lectura parquet
df_parquet = pd.read_parquet(
    "outputs/turismo.parquet"
)

print(df_parquet.head())

# Fin de pruebas de lectura parquet