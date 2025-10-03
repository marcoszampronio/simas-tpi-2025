from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, Producto
from routes import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///productos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/alta')
def alta():
    return render_template('alta.html')

@app.route('/administrar')
def administrar():
    productos = Producto.query.all()
    return render_template('administrar.html', productos=productos)

@app.route('/producto/<int:id>')
def ver_producto(id):
    producto = Producto.query.get_or_404(id)
    return render_template('producto.html', producto=producto)

@app.route('/producto/<int:id>/editar', methods=['GET', 'POST'])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)

    if request.method == 'POST':
        producto.sku = request.form['sku']
        producto.nombre = request.form['nombre']
        producto.cantidad = int(request.form['cantidad'])
        producto.estado = request.form['estado']
        producto.precio_venta = float(request.form['precio_venta'])
        producto.categoria = request.form['categoria']
        producto.descripcion = request.form['descripcion']
        producto.politica_inventario = request.form['politica_inventario']
        producto.proveedor = request.form['proveedor']
        producto.costo_unitario = float(request.form['costo_unitario'])

        if 'imagen' in request.files:
            imagen = request.files['imagen']
            if imagen.filename != '':
                producto.imagen = imagen.filename  # En producción usarías un sistema de archivos

        db.session.commit()
        flash('Producto actualizado exitosamente')
        return redirect(url_for('administrar'))

    return render_template('editar_producto.html', producto=producto)

@app.route('/producto/<int:id>/eliminar')
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado exitosamente')
    return redirect(url_for('administrar'))

if __name__ == '__main__':
    app.run(debug=True)