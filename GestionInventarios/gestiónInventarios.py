import pandas as pd
import mysql.connector
from mysql.connector import Error

# Ruta del archivo CSV
csv_file_path = 'C:\\Users\\chris\\OneDrive\\Escritorio\\GestionInventarios\\orders.csv'

# Leer el archivo CSV usando pandas
data = pd.read_csv(csv_file_path)

# Conexión a la base de datos MySQL
try:
    connection = mysql.connector.connect(
        host='localhost',          # Cambia a tu host de MySQL
        database='inventario',  # Cambia al nombre de tu base de datos
        user='root',            # Cambia a tu usuario de MySQL
        password='123456'      # Cambia a tu contraseña de MySQL
    )

    if connection.is_connected():
        cursor = connection.cursor()

        # Crear la tabla orders si no existe
        create_table_query = """
        CREATE TABLE IF NOT EXISTS orders (
            id INT NOT NULL,
            cantidad INT,
            nombreCliente VARCHAR(255),
            cedulaCliente VARCHAR(255),
            nombreProducto VARCHAR(255),
            valorUnitario DECIMAL(10, 2),
            total DECIMAL(10, 2),
            PRIMARY KEY (id)
        )
        """
        cursor.execute(create_table_query)

        # Insertar los datos del DataFrame en la tabla de MySQL
        for i, row in data.iterrows():
            # Insertar la orden
            sql_insert_order = """
            INSERT INTO orders ( cantidad, nombreCliente, cedulaCliente, nombreProducto, valorUnitario, total) 
            VALUES ( %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_insert_order, (row['cantidad'], row['nombreCliente'], row['cedulaCliente'], row['nombreProducto'], row['valorUnitario'], row['total']))
            
            # Actualizar la cantidad en la tabla productos
            sql_update_product = """
            UPDATE productos 
            SET cantidad = cantidad - %s 
            WHERE nombre = %s
            """
            cursor.execute(sql_update_product, (row['cantidad'], row['nombreProducto']))

        # Confirmar los cambios
        connection.commit()

        print("Datos insertados y cantidades actualizadas correctamente en la tabla MySQL")

except Error as e:
    print(f"Error al conectar a MySQL: {e}")
finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("Conexión a MySQL cerrada")
