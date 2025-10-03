from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Crear directorio de uploads si no existe
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_db_connection():
    conn = sqlite3.connect('productos.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT NOT NULL UNIQUE,
            imagen TEXT,
            cantidad INTEGER NOT NULL,
            estado TEXT NOT NULL,
            precio_venta REAL NOT NULL,
            categoria TEXT NOT NULL,
            descripcion TEXT,
            politica_inventario TEXT,
            proveedor TEXT,
            costo_unitario REAL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/alta')
def alta():
    return render_template('alta.html')

@app.route('/crear_producto', methods=['POST'])
def crear_producto():
    sku = request.form['sku']
    cantidad = int(request.form['cantidad'])
    estado = request.form['estado']
    precio_venta = float(request.form['precio_venta'])
    categoria = request.form['categoria']
    descripcion = request.form['descripcion']
    politica_inventario = request.form['politica_inventario']
    proveedor = request.form['proveedor']
    costo_unitario = float(request.form['costo_unitario'])

    # Manejo de imagen
    imagen_filename = None
    if 'imagen' in request.files:
        file = request.files['imagen']
        if file and allowed_file(file.filename):
            imagen_filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_filename))

    conn = get_db_connection()
    try:
        conn.execute('''
            INSERT INTO productos (sku, imagen, cantidad, estado, precio_venta, categoria, descripcion, politica_inventario, proveedor, costo_unitario)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (sku, imagen_filename, cantidad, estado, precio_venta, categoria, descripcion, politica_inventario, proveedor, costo_unitario))
        conn.commit()
        flash('Producto creado exitosamente!')
    except sqlite3.IntegrityError:
        flash('Error: El SKU ya existe!')
    finally:
        conn.close()

    return redirect(url_for('alta'))

@app.route('/consulta')
def consulta():
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM productos ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('consulta.html', productos=productos)

@app.route('/producto/<int:id>')
def detalle_producto(id):
    conn = get_db_connection()
    producto = conn.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('detalle.html', producto=producto)

@app.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modificar_producto(id):
    conn = get_db_connection()
    producto = conn.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        sku = request.form['sku']
        cantidad = int(request.form['cantidad'])
        estado = request.form['estado']
        precio_venta = float(request.form['precio_venta'])
        categoria = request.form['categoria']
        descripcion = request.form['descripcion']
        politica_inventario = request.form['politica_inventario']
        proveedor = request.form['proveedor']
        costo_unitario = float(request.form['costo_unitario'])

        # Manejo de imagen
        imagen_filename = producto['imagen']
        if 'imagen' in request.files and request.files['imagen'].filename != '':
            file = request.files['imagen']
            if file and allowed_file(file.filename):
                # Eliminar imagen anterior si existe
                if producto['imagen']:
                    old_path = os.path.join(app.config['UPLOAD_FOLDER'], producto['imagen'])
                    if os.path.exists(old_path):
                        os.remove(old_path)

                imagen_filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_filename))

        conn.execute('''
            UPDATE productos
            SET sku = ?, imagen = ?, cantidad = ?, estado = ?, precio_venta = ?, categoria = ?, descripcion = ?, politica_inventario = ?, proveedor = ?, costo_unitario = ?
            WHERE id = ?
        ''', (sku, imagen_filename, cantidad, estado, precio_venta, categoria, descripcion, politica_inventario, proveedor, costo_unitario, id))
        conn.commit()
        flash('Producto actualizado exitosamente!')
        return redirect(url_for('consulta'))

    conn.close()
    return render_template('modificar.html', producto=producto)

@app.route('/eliminar/<int:id>')
def eliminar_producto(id):
    conn = get_db_connection()
    producto = conn.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()

    # Eliminar imagen si existe
    if producto['imagen']:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], producto['imagen'])
        if os.path.exists(image_path):
            os.remove(image_path)

    conn.execute('DELETE FROM productos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Producto eliminado exitosamente!')
    return redirect(url_for('consulta'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)