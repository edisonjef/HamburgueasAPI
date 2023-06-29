#----------------------------------------------
# Importamos el módulo necesario para gestionar
# la base de datos, y los elementos necesarios
# del framework Flask.
#----------------------------------------------
import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

# Nombre del objeto flask.
app = Flask(__name__)
CORS(app)


# Nombre del archivo que contiene la base de datos.
DATABASE = "hamburguesas.db"


#----------------------------------------------
# Conectamos con la base de datos. 
# Retornamos el conector (conn)
#----------------------------------------------
def conectar():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


#----------------------------------------------
# Esta funcion crea la tabla "productos" en la
# base de datos, en caso de que no exista.
#----------------------------------------------
def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    codigo INTEGER PRIMARY KEY ,
                    nombre VARCHARD (50) NOT NULL,
                    descripcion VARCHAR(255) NOT NULL,
                    precio FLOAT NOT NULL,
                    stock INT NOT NULL
                    
                    
                    )
            """)
    conn.commit()
    cursor.close()
    conn.close()

#----------------------------------------------
# Esta funcion da de alta un producto en la
# base de datos.
#----------------------------------------------
@app.route('/productos', methods=['POST'])
def alta_producto():
    data = request.get_json()
    if 'nombre' not in data or 'descripcion' not in data or 'stock' not in data or 'precio' not in data :
        return jsonify({'error': 'Falta uno o más campos requeridos'}), 400
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
                    INSERT INTO productos(nombre, descripcion, precio, stock )
                    VALUES(?,?,?,?) """,
                    (data['nombre'], data['descripcion'],data['precio'], data['stock'] ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'mensaje': 'Alta efectuada correctamente'}), 201
    except:
        return jsonify({'error': 'Error al dar de alta el producto'}), 500
    

    

#----------------------------------------------
# Muestra en la pantalla los datos de un  
# producto a partir de su código.
#----------------------------------------------
@app.route('/productos/<int:codigo>', methods=['GET'])
def consultar_producto(codigo):
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        cursor.execute("""SELECT * FROM productos 
                            WHERE codigo=?""", (codigo,))
        producto = cursor.fetchone()
        
        if producto is None:
            return jsonify({'error': 'Producto no encontrado'}), 404
        else:
            return jsonify({
                'codigo': producto['codigo'],
                'nombre': producto['nombre'],
                'descripcion': producto['descripcion'],
                'precio': producto['precio'],
                'stock': producto['stock']
                
            
            })
    except:
        return jsonify({'error': 'Error al consultar el producto'}), 500


#----------------------------------------------
# Modifica los datos de un producto a partir
# de su código.
#----------------------------------------------
@app.route('/productos/<int:codigo>', methods=['PUT'])
def modificar_producto(codigo):
    data = request.get_json()
    if  'nombre' not in data or 'descripcion' not in data or 'precio' not in data or 'stock' not in data:
        return jsonify({'error': 'Falta uno o más campos requeridos'}), 400
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM productos WHERE codigo=?""", (codigo,))
        producto = cursor.fetchone()
        if producto is None:
            return jsonify({'error': 'Producto no encontrado'}), 404
        else:
            cursor.execute("""UPDATE productos SET nombre=? , descripcion=?, precio=?, stock=?
                                WHERE codigo=?""", (data['nombre'], data['descripcion'], data['precio'], data['stock'], codigo))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'mensaje': 'Producto modificado correctamente'}), 200
    except:
        return jsonify({'error': 'Error al modificar el producto'}), 500


#----------------------------------------------
# Lista todos los productos en la base de datos.
#----------------------------------------------
@app.route('/productos', methods=['GET'])
def listar_productos():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        response = []
        for producto in productos:
            response.append({
                'codigo': producto['codigo'],
                'nombre': producto['nombre'],
                'descripcion': producto['descripcion'],
                'stock': producto['stock'],
                'precio': producto['precio'],
                
            })
        return jsonify(response)
    except:
        return jsonify({'error': 'Error al listar los productos'}), 500
    




@app.route('/')
def hello_world():
    return 'Hola Edison desde Flask!'



#----------------------------------------------
# Ejecutamos la app
#----------------------------------------------
if __name__ == '__main__':
    crear_tabla()
    app.run(debug=True)
