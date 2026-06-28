import duckdb

# Prueba de conexión usando print
#conexion = print(duckdb.connect())
conexion = duckdb.connect()

# Consultar los primeros registros
consulta = """
SELECT *
FROM read_parquet('outputs/turismo.parquet')
LIMIT 10
"""

print(conexion.execute(consulta).fetchdf())

# Identificar la estructura del conjunto de datos
consulta2 = """
DESCRIBE
SELECT *
FROM read_parquet('outputs/turismo.parquet')
"""

print(conexion.execute(consulta2).fetchdf())

# Número total de registros
consulta3 = """
SELECT COUNT(*) AS total_registros
FROM read_parquet('outputs/turismo.parquet')
"""

print(conexion.execute(consulta3).fetchdf())

# Destinos más visitados
consulta4 = """
SELECT
    "CIUDAD DE DESTINO 1" AS destino,
    COUNT(*) AS visitantes
FROM read_parquet('outputs/turismo.parquet')
GROUP BY destino
ORDER BY visitantes DESC
LIMIT 10
"""

print(conexion.execute(consulta4).fetchdf())