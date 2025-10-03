from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    imagen = db.Column(db.String(100))
    cantidad = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(20), nullable=False)
    precio_venta = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    politica_inventario = db.Column(db.String(50), nullable=False)
    proveedor = db.Column(db.String(100), nullable=False)
    costo_unitario = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Producto {self.nombre}>'