from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Producto

def crear_producto():
    """Función para crear un nuevo producto"""
    nuevo_producto = Producto(
        sku=request.form['sku'],
        nombre=request.form['nombre'],
        cantidad=int(request.form['cantidad']),
        estado=request.form['estado'],
        precio_venta=float(request.form['precio_venta']),
        categoria=request.form['categoria'],
        descripcion=request.form['descripcion'],
        politica_inventario=request.form['politica_inventario'],
        proveedor=request.form['proveedor'],
        costo_unitario=float(request.form['costo_unitario'])
    )

    if 'imagen' in request.files:
        imagen = request.files['imagen']
        if imagen.filename != '':
            nuevo_producto.imagen = imagen.filename  # En producción usarías un sistema de archivos

    db.session.add(nuevo_producto)
    db.session.commit()

    return nuevo_producto