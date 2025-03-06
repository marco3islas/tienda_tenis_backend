import pandas as pd
import psycopg2
from psycopg2 import Error

# Configuración de la conexión a PostgreSQL
conn_params = {
    "dbname": "tienda_tenis",
    "user": "marco",
    "password": "admin",
    "host": "localhost",
    "port": "5432"
}

try:
    # Conéctate a PostgreSQL
    connection = psycopg2.connect(**conn_params)
    cursor = connection.cursor()

    # Lee el archivo CSV
    df = pd.read_csv("productos.csv", dtype={"Tallas":str})

    print("Datos del csv: ")
    print(df)
    # Convierte los datos a una lista de tuplas para la inserción
    data = [tuple(row) for row in df.values]

    print("Datos a insertar")
    print(data)

    # SQL para insertar los datos (ajusta las columnas según tu tabla)
    insert_query = """
    INSERT INTO productos (id, imagen, titulo, description, precio, tallas)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING;  -- Evita duplicados si el id ya existe
    """

    # Ejecuta la inserción por lotes para mejorar el rendimiento
    cursor.executemany(insert_query, data)
    connection.commit()
    print(f"Migrados {len(data)} productos exitosamente.")

except Error as e:
    print(f"Error al migrar los datos: {e}")
    if connection:
        connection.rollback()

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
