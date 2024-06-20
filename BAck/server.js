const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql2');
const cors = require('cors');
const { Parser } = require('json2csv');
const fs = require('fs');
const multer = require('multer'); // Para manejar la carga de archivos
const { parse } = require('csv-parse/sync'); // Importación correcta de csv-parse

const app = express();
const port = 3000;

app.use(bodyParser.json());
app.use(cors());

// Configuración de la conexión a la base de datos 'ordenescompra'
const dbOrdenesCompra = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '123456',
  database: 'ordenescompra'
});

dbOrdenesCompra.connect((err) => {
  if (err) {
    throw err;
  }
  console.log('Conectado a la base de datos MySQL (ordenescompra)');
});

// Configuración de la conexión a la base de datos 'inventario'
const dbInventario = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '123456',
  database: 'inventario'
});

dbInventario.connect((err) => {
  if (err) {
    throw err;
  }
  console.log('Conectado a la base de datos MySQL (inventario)');
});

// Configuración de multer para la carga de archivos
const upload = multer({ dest: 'uploads/' });

// Ruta para guardar la orden de compra en la base de datos 'ordenescompra'
app.post('/save-order', (req, res) => {
  const order = req.body;
  const sql = 'INSERT INTO orders SET ?';
  dbOrdenesCompra.query(sql, order, (err, result) => {
    if (err) {
      console.error(err);
      res.status(500).send('Error al guardar la orden');
    } else {
      res.send('Orden guardada en la base de datos ordenescompra');
    }
  });
});

// Ruta para cargar el CSV y actualizar el inventario en la base de datos 'inventario'
// Ruta para cargar el CSV y actualizar el inventario en la base de datos 'inventario'
app.post('/upload-csv', upload.single('file'), (req, res) => {
    if (!req.file) {
      return res.status(400).send('No se ha proporcionado ningún archivo');
    }
  
    const csvFilePath = req.file.path;
  
    // Leer el archivo CSV
    fs.readFile(csvFilePath, 'utf8', (err, data) => {
      if (err) {
        console.error(err);
        return res.status(500).send('Error al leer el archivo CSV');
      }
  
      // Parsear el CSV
      const csvData = csvParse(data, {
        columns: true,
        skip_empty_lines: true
      });
  
      // Actualizar el inventario en la base de datos 'inventario'
      csvData.forEach((row) => {
        const { idProducto, cantidad } = row; // Asumiendo que el CSV tiene un campo 'idProducto' y 'cantidad'
        const sql = 'UPDATE productos SET cantidad = cantidad - ? WHERE id = ?';
        dbInventario.query(sql, [cantidad, idProducto], (err, result) => {
          if (err) {
            console.error(err);
          }
        });
      });
  
      res.send('Inventario actualizado correctamente en la base de datos inventario');
    });
  });

// Ruta para descargar el archivo CSV
app.get('/download-csv', (req, res) => {
  const filePath = 'C:\\Users\\chris\\OneDrive\\Escritorio\\BAck\\orders.csv';

  // Verificar si el archivo existe
  fs.access(filePath, fs.constants.F_OK, (err) => {
    if (err) {
      console.error(err);
      return res.status(404).send('Archivo CSV no encontrado');
    }

    // Configurar los encabezados de respuesta para la descarga
    res.setHeader('Content-disposition', 'attachment; filename=orders.csv');
    res.setHeader('Content-type', 'text/csv');

    // Crear un stream de lectura del archivo y transmitirlo como respuesta
    const fileStream = fs.createReadStream(filePath);
    fileStream.pipe(res);
  });
});

// Función para convertir CSV a JSON
function csvParse(csvString, options) {
  const csvParser = new Parser(options);
  return csvParser.parse(csvString);
}
  
  app.listen(port, () => {
    console.log(`Servidor corriendo en http://localhost:${port}`);
  });