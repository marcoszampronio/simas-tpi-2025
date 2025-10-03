from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///productos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Producto
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    imagen = db.Column(db.String(200), nullable=True)
    cantidad = db.Column(db.Integer, nullable=False, default=0)
    estado = db.Column(db.String(20), nullable=False, default='Activo')
    precio_venta = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    politica_inventario = db.Column(db.String(100), nullable=False)
    proveedor = db.Column(db.String(100), nullable=False)
    costo_unitario = db.Column(db.Float, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Producto {self.sku}>'

    def to_dict(self):
        return {
            'id': self.id,
            'sku': self.sku,
            'imagen': self.imagen,
            'cantidad': self.cantidad,
            'estado': self.estado,
            'precio_venta': self.precio_venta,
            'categoria': self.categoria,
            'descripcion': self.descripcion,
            'politica_inventario': self.politica_inventario,
            'proveedor': self.proveedor,
            'costo_unitario': self.costo_unitario,
            'fecha_creacion': self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_actualizacion else None
        }

# Rutas
@app.route('/')
def index():
    """Página principal con las dos opciones"""
    return render_template('index.html')

@app.route('/alta')
def alta():
    """Formulario para dar de alta un producto"""
    return render_template('alta.html')

@app.route('/consulta')
def consulta():
    """Página de consulta/modificación/baja de productos"""
    productos = Producto.query.all()
    return render_template('consulta.html', productos=productos)

@app.route('/crear_producto', methods=['POST'])
def crear_producto():
    """Crear un nuevo producto"""
    try:
        producto = Producto(
            sku=request.form['sku'],
            imagen=request.form.get('imagen', ''),
            cantidad=int(request.form['cantidad']),
            estado=request.form['estado'],
            precio_venta=float(request.form['precio_venta']),
            categoria=request.form['categoria'],
            descripcion=request.form.get('descripcion', ''),
            politica_inventario=request.form['politica_inventario'],
            proveedor=request.form['proveedor'],
            costo_unitario=float(request.form['costo_unitario'])
        )
        
        db.session.add(producto)
        db.session.commit()
        flash('Producto creado exitosamente!', 'success')
        return redirect(url_for('alta'))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear el producto: {str(e)}', 'error')
        return redirect(url_for('alta'))

@app.route('/producto/<int:id>')
def ver_producto(id):
    """Ver detalles de un producto específico"""
    producto = Producto.query.get_or_404(id)
    return render_template('producto_detalle.html', producto=producto)

@app.route('/editar/<int:id>')
def editar_producto(id):
    """Formulario para editar un producto"""
    producto = Producto.query.get_or_404(id)
    return render_template('editar.html', producto=producto)

@app.route('/actualizar_producto/<int:id>', methods=['POST'])
def actualizar_producto(id):
    """Actualizar un producto existente"""
    try:
        producto = Producto.query.get_or_404(id)
        
        producto.sku = request.form['sku']
        producto.imagen = request.form.get('imagen', '')
        producto.cantidad = int(request.form['cantidad'])
        producto.estado = request.form['estado']
        producto.precio_venta = float(request.form['precio_venta'])
        producto.categoria = request.form['categoria']
        producto.descripcion = request.form.get('descripcion', '')
        producto.politica_inventario = request.form['politica_inventario']
        producto.proveedor = request.form['proveedor']
        producto.costo_unitario = float(request.form['costo_unitario'])
        producto.fecha_actualizacion = datetime.utcnow()
        
        db.session.commit()
        flash('Producto actualizado exitosamente!', 'success')
        return redirect(url_for('consulta'))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar el producto: {str(e)}', 'error')
        return redirect(url_for('editar_producto', id=id))

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    """Eliminar un producto"""
    try:
        producto = Producto.query.get_or_404(id)
        db.session.delete(producto)
        db.session.commit()
        flash('Producto eliminado exitosamente!', 'success')
        return redirect(url_for('consulta'))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el producto: {str(e)}', 'error')
        return redirect(url_for('consulta'))

@app.route('/api/productos')
def api_productos():
    """API endpoint para obtener todos los productos"""
    productos = Producto.query.all()
    return jsonify([producto.to_dict() for producto in productos])

@app.route('/api/producto/<int:id>')
def api_producto(id):
    """API endpoint para obtener un producto específico"""
    producto = Producto.query.get_or_404(id)
    return jsonify(producto.to_dict())

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)