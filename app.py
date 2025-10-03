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
    categoria = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text)
    politica_gestion_inventario = db.Column(db.String(100))
    proveedor = db.Column(db.String(100), nullable=False)
    costo_unitario = db.Column(db.Float, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Producto {self.sku}>'

# Rutas
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

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    try:
        producto = Producto(
            sku=request.form['sku'],
            imagen=request.form['imagen'],
            cantidad=int(request.form['cantidad']),
            estado=request.form['estado'],
            precio_venta=float(request.form['precio_venta']),
            categoria=request.form['categoria'],
            descripcion=request.form['descripcion'],
            politica_gestion_inventario=request.form['politica_gestion_inventario'],
            proveedor=request.form['proveedor'],
            costo_unitario=float(request.form['costo_unitario'])
        )
        
        db.session.add(producto)
        db.session.commit()
        flash('Producto agregado exitosamente', 'success')
        return redirect(url_for('consulta'))
    except Exception as e:
        flash(f'Error al agregar producto: {str(e)}', 'error')
        return redirect(url_for('alta'))

@app.route('/producto/<int:id>')
def detalle_producto(id):
    producto = Producto.query.get_or_404(id)
    return render_template('detalle_producto.html', producto=producto)

@app.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            producto.sku = request.form['sku']
            producto.imagen = request.form['imagen']
            producto.cantidad = int(request.form['cantidad'])
            producto.estado = request.form['estado']
            producto.precio_venta = float(request.form['precio_venta'])
            producto.categoria = request.form['categoria']
            producto.descripcion = request.form['descripcion']
            producto.politica_gestion_inventario = request.form['politica_gestion_inventario']
            producto.proveedor = request.form['proveedor']
            producto.costo_unitario = float(request.form['costo_unitario'])
            producto.fecha_modificacion = datetime.utcnow()
            
            db.session.commit()
            flash('Producto actualizado exitosamente', 'success')
            return redirect(url_for('consulta'))
        except Exception as e:
            flash(f'Error al actualizar producto: {str(e)}', 'error')
    
    return render_template('editar_producto.html', producto=producto)

@app.route('/eliminar_producto/<int:id>', methods=['POST'])
def eliminar_producto(id):
    try:
        producto = Producto.query.get_or_404(id)
        db.session.delete(producto)
        db.session.commit()
        flash('Producto eliminado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar producto: {str(e)}', 'error')
    
    return redirect(url_for('consulta'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)