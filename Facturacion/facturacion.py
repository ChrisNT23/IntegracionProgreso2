import mysql.connector
from mysql.connector import Error
from fpdf import FPDF
import sys

# Conexión a la base de datos MySQL
try:
    connection = mysql.connector.connect(
        host='localhost',
        database='inventario',
        user='root',
        password='123456'
    )

    if connection.is_connected():
        cursor = connection.cursor()

        # Pedir el ID de la orden de compra al usuario
        order_id = input("Ingrese el ID de la orden de compra: ")

        # Consultar la información de la orden de compra
        sql_query = "SELECT * FROM orders WHERE id = %s"
        cursor.execute(sql_query, (order_id,))
        order = cursor.fetchone()

        if order:
            # Crear el PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            # Agregar el contenido de la orden al PDF
            pdf.cell(200, 10, txt="Factura", ln=True, align='C')
            pdf.cell(200, 10, txt=f"ID de la orden: {order[0]}", ln=True, align='L')
            pdf.cell(200, 10, txt=f"Cantidad: {order[1]}", ln=True, align='L')
            pdf.cell(200, 10, txt=f"Nombre del Cliente: {order[2]}", ln=True, align='L')
            pdf.cell(200, 10, txt=f"Cédula del Cliente: {order[3]}", ln=True, align='L')
            pdf.cell(200, 10, txt=f"Nombre del Producto: {order[4]}", ln=True, align='L')
            pdf.cell(200, 10, txt=f"Valor Unitario: ${order[5]:.2f}", ln=True, align='L')
            pdf.cell(200, 10, txt=f"Total: ${order[6]:.2f}", ln=True, align='L')

            # Guardar el PDF
            pdf_file_path = f"orden_{order_id}.pdf"
            pdf.output(pdf_file_path)

            print(f"PDF generado exitosamente: {pdf_file_path}")
             # Insertar datos en la tabla factura
            insert_query = """
            INSERT INTO facturacion (id, cantidad, nombreCliente, cedulaCliente, nombreProducto, valorUnitario, total)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, order)
            connection.commit()

            print("Datos insertados en la tabla factura")
        else:
            print(f"No se encontró la orden de compra con ID: {order_id}")

except Error as e:
    print(f"Error al conectar a MySQL: {e}")

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("Conexión a MySQL cerrada")
