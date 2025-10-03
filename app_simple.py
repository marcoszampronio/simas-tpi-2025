from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'

# Configuración de la base de datos
DATABASE = 'productos.db'

def init_db():
    """Inicializar la base de datos"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS producto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT UNIQUE NOT NULL,
            imagen TEXT,
            cantidad INTEGER NOT NULL DEFAULT 0,
            estado TEXT NOT NULL DEFAULT 'Activo',
            precio_venta REAL NOT NULL,
            categoria TEXT NOT NULL,
            descripcion TEXT,
            politica_gestion_inventario TEXT,
            proveedor TEXT NOT NULL,
            costo_unitario REAL NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Obtener conexión a la base de datos"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Rutas principales
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/alta')
def alta():
    return render_template('alta.html')

@app.route('/consulta')
def consulta():
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM producto ORDER BY fecha_creacion DESC').fetchall()
    conn.close()
    return render_template('consulta.html', productos=productos)

@app.route('/producto/<int:id>')
def detalle_producto(id):
    conn = get_db_connection()
    producto = conn.execute('SELECT * FROM producto WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if producto is None:
        flash('Producto no encontrado', 'error')
        return redirect(url_for('consulta'))
    
    return render_template('detalle_producto.html', producto=producto)

@app.route('/editar/<int:id>')
def editar_producto(id):
    conn = get_db_connection()
    producto = conn.execute('SELECT * FROM producto WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if producto is None:
        flash('Producto no encontrado', 'error')
        return redirect(url_for('consulta'))
    
    return render_template('editar_producto.html', producto=producto)

# API endpoints
@app.route('/api/productos', methods=['POST'])
def crear_producto():
    try:
        data = request.get_json()
        
        # Validar que el SKU sea único
        conn = get_db_connection()
        existing = conn.execute('SELECT id FROM producto WHERE sku = ?', (data['sku'],)).fetchone()
        if existing:
            conn.close()
            return jsonify({'error': 'El SKU ya existe'}), 400
        
        # Insertar nuevo producto
        conn.execute('''
            INSERT INTO producto (sku, imagen, cantidad, estado, precio_venta, categoria, 
                                 descripcion, politica_gestion_inventario, proveedor, costo_unitario)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['sku'],
            data.get('imagen', ''),
            int(data['cantidad']),
            data.get('estado', 'Activo'),
            float(data['precio_venta']),
            data['categoria'],
            data.get('descripcion', ''),
            data.get('politica_gestion_inventario', ''),
            data['proveedor'],
            float(data['costo_unitario'])
        ))
        
        conn.commit()
        producto_id = conn.lastrowid
        conn.close()
        
        return jsonify({'message': 'Producto creado exitosamente', 'id': producto_id}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    try:
        conn = get_db_connection()
        producto = conn.execute('SELECT * FROM producto WHERE id = ?', (id,)).fetchone()
        
        if producto is None:
            conn.close()
            return jsonify({'error': 'Producto no encontrado'}), 404
        
        data = request.get_json()
        
        # Validar que el SKU sea único (si se está cambiando)
        if data.get('sku') != producto['sku']:
            existing = conn.execute('SELECT id FROM producto WHERE sku = ? AND id != ?', 
                                  (data['sku'], id)).fetchone()
            if existing:
                conn.close()
                return jsonify({'error': 'El SKU ya existe'}), 400
        
        # Actualizar producto
        conn.execute('''
            UPDATE producto SET 
                sku = ?, imagen = ?, cantidad = ?, estado = ?, precio_venta = ?,
                categoria = ?, descripcion = ?, politica_gestion_inventario = ?,
                proveedor = ?, costo_unitario = ?, fecha_modificacion = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            data['sku'],
            data.get('imagen', producto['imagen']),
            int(data['cantidad']),
            data.get('estado', producto['estado']),
            float(data['precio_venta']),
            data['categoria'],
            data.get('descripcion', producto['descripcion']),
            data.get('politica_gestion_inventario', producto['politica_gestion_inventario']),
            data['proveedor'],
            float(data['costo_unitario']),
            id
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Producto actualizado exitosamente'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    try:
        conn = get_db_connection()
        producto = conn.execute('SELECT * FROM producto WHERE id = ?', (id,)).fetchone()
        
        if producto is None:
            conn.close()
            return jsonify({'error': 'Producto no encontrado'}), 404
        
        conn.execute('DELETE FROM producto WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Producto eliminado exitosamente'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)