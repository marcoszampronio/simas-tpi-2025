from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

# Configuración de la base de datos
DATABASE = 'productos.db'

def init_db():
    """Inicializa la base de datos con la tabla de productos"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT UNIQUE NOT NULL,
            imagen TEXT,
            cantidad INTEGER NOT NULL DEFAULT 0,
            estado TEXT NOT NULL DEFAULT 'Activo',
            precio_venta REAL NOT NULL,
            categoria TEXT NOT NULL,
            descripcion TEXT,
            politica_gestion_inventario TEXT,
            proveedor TEXT,
            costo_unitario REAL NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Obtiene una conexión a la base de datos"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Página principal con opciones de navegación"""
    return render_template('index.html')

@app.route('/alta')
def alta():
    """Página para agregar nuevos productos"""
    return render_template('alta.html')

@app.route('/gestion')
def gestion():
    """Página para gestionar productos existentes"""
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM productos ORDER BY fecha_modificacion DESC').fetchall()
    conn.close()
    return render_template('gestion.html', productos=productos)

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    """Agrega un nuevo producto a la base de datos"""
    try:
        conn = get_db_connection()
        
        # Obtener datos del formulario
        sku = request.form['sku']
        imagen = request.form['imagen']
        cantidad = int(request.form['cantidad'])
        estado = request.form['estado']
        precio_venta = float(request.form['precio_venta'])
        categoria = request.form['categoria']
        descripcion = request.form['descripcion']
        politica_gestion = request.form['politica_gestion_inventario']
        proveedor = request.form['proveedor']
        costo_unitario = float(request.form['costo_unitario'])
        
        # Verificar si el SKU ya existe
        existing = conn.execute('SELECT id FROM productos WHERE sku = ?', (sku,)).fetchone()
        if existing:
            flash('El SKU ya existe. Por favor, use un SKU diferente.', 'error')
            return redirect(url_for('alta'))
        
        # Insertar nuevo producto
        conn.execute('''
            INSERT INTO productos (sku, imagen, cantidad, estado, precio_venta, categoria, 
                                 descripcion, politica_gestion_inventario, proveedor, costo_unitario)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (sku, imagen, cantidad, estado, precio_venta, categoria, descripcion, 
              politica_gestion, proveedor, costo_unitario))
        
        conn.commit()
        conn.close()
        
        flash('Producto agregado exitosamente!', 'success')
        return redirect(url_for('gestion'))
        
    except Exception as e:
        flash(f'Error al agregar el producto: {str(e)}', 'error')
        return redirect(url_for('alta'))

@app.route('/producto/<int:id>')
def ver_producto(id):
    """Muestra los detalles de un producto específico"""
    conn = get_db_connection()
    producto = conn.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if producto is None:
        flash('Producto no encontrado', 'error')
        return redirect(url_for('gestion'))
    
    return render_template('producto_detalle.html', producto=producto)

@app.route('/editar_producto/<int:id>', methods=['POST'])
def editar_producto(id):
    """Edita un producto existente"""
    try:
        conn = get_db_connection()
        
        # Obtener datos del formulario
        sku = request.form['sku']
        imagen = request.form['imagen']
        cantidad = int(request.form['cantidad'])
        estado = request.form['estado']
        precio_venta = float(request.form['precio_venta'])
        categoria = request.form['categoria']
        descripcion = request.form['descripcion']
        politica_gestion = request.form['politica_gestion_inventario']
        proveedor = request.form['proveedor']
        costo_unitario = float(request.form['costo_unitario'])
        
        # Verificar si el SKU ya existe en otro producto
        existing = conn.execute('SELECT id FROM productos WHERE sku = ? AND id != ?', (sku, id)).fetchone()
        if existing:
            flash('El SKU ya existe en otro producto. Por favor, use un SKU diferente.', 'error')
            return redirect(url_for('ver_producto', id=id))
        
        # Actualizar producto
        conn.execute('''
            UPDATE productos 
            SET sku = ?, imagen = ?, cantidad = ?, estado = ?, precio_venta = ?, 
                categoria = ?, descripcion = ?, politica_gestion_inventario = ?, 
                proveedor = ?, costo_unitario = ?, fecha_modificacion = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (sku, imagen, cantidad, estado, precio_venta, categoria, descripcion, 
              politica_gestion, proveedor, costo_unitario, id))
        
        conn.commit()
        conn.close()
        
        flash('Producto actualizado exitosamente!', 'success')
        return redirect(url_for('ver_producto', id=id))
        
    except Exception as e:
        flash(f'Error al actualizar el producto: {str(e)}', 'error')
        return redirect(url_for('ver_producto', id=id))

@app.route('/eliminar_producto/<int:id>', methods=['POST'])
def eliminar_producto(id):
    """Elimina un producto de la base de datos"""
    try:
        conn = get_db_connection()
        
        # Verificar que el producto existe
        producto = conn.execute('SELECT sku FROM productos WHERE id = ?', (id,)).fetchone()
        if producto is None:
            flash('Producto no encontrado', 'error')
            return redirect(url_for('gestion'))
        
        # Eliminar producto
        conn.execute('DELETE FROM productos WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        
        flash(f'Producto {producto["sku"]} eliminado exitosamente!', 'success')
        return redirect(url_for('gestion'))
        
    except Exception as e:
        flash(f'Error al eliminar el producto: {str(e)}', 'error')
        return redirect(url_for('gestion'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5001)