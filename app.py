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
    imagen = db.Column(db.String(200))
    cantidad = db.Column(db.Integer, nullable=False, default=0)
    estado = db.Column(db.String(20), nullable=False, default='Activo')
    precio_venta = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    politica_gestion_inventario = db.Column(db.String(100))
    proveedor = db.Column(db.String(100), nullable=False)
    costo_unitario = db.Column(db.Float, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Producto {self.sku}>'

# Rutas principales
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/alta')
def alta():
    return render_template('alta.html')

@app.route('/consulta')
def consulta():
    productos = Producto.query.all()
    return render_template('consulta.html', productos=productos)

@app.route('/producto/<int:id>')
def detalle_producto(id):
    producto = Producto.query.get_or_404(id)
    return render_template('detalle_producto.html', producto=producto)

@app.route('/editar/<int:id>')
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    return render_template('editar_producto.html', producto=producto)

# API endpoints
@app.route('/api/productos', methods=['POST'])
def crear_producto():
    try:
        data = request.get_json()
        
        # Validar que el SKU sea único
        if Producto.query.filter_by(sku=data['sku']).first():
            return jsonify({'error': 'El SKU ya existe'}), 400
        
        producto = Producto(
            sku=data['sku'],
            imagen=data.get('imagen', ''),
            cantidad=int(data['cantidad']),
            estado=data.get('estado', 'Activo'),
            precio_venta=float(data['precio_venta']),
            categoria=data['categoria'],
            descripcion=data.get('descripcion', ''),
            politica_gestion_inventario=data.get('politica_gestion_inventario', ''),
            proveedor=data['proveedor'],
            costo_unitario=float(data['costo_unitario'])
        )
        
        db.session.add(producto)
        db.session.commit()
        
        return jsonify({'message': 'Producto creado exitosamente', 'id': producto.id}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    try:
        producto = Producto.query.get_or_404(id)
        data = request.get_json()
        
        # Validar que el SKU sea único (si se está cambiando)
        if data.get('sku') != producto.sku:
            if Producto.query.filter_by(sku=data['sku']).first():
                return jsonify({'error': 'El SKU ya existe'}), 400
        
        producto.sku = data['sku']
        producto.imagen = data.get('imagen', producto.imagen)
        producto.cantidad = int(data['cantidad'])
        producto.estado = data.get('estado', producto.estado)
        producto.precio_venta = float(data['precio_venta'])
        producto.categoria = data['categoria']
        producto.descripcion = data.get('descripcion', producto.descripcion)
        producto.politica_gestion_inventario = data.get('politica_gestion_inventario', producto.politica_gestion_inventario)
        producto.proveedor = data['proveedor']
        producto.costo_unitario = float(data['costo_unitario'])
        producto.fecha_modificacion = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({'message': 'Producto actualizado exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    try:
        producto = Producto.query.get_or_404(id)
        db.session.delete(producto)
        db.session.commit()
        
        return jsonify({'message': 'Producto eliminado exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)