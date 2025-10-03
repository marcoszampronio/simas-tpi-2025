#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad CRUD
"""

from app import app, db, Producto
from datetime import datetime, timezone

def test_crud_operations():
    """Prueba las operaciones CRUD básicas"""
    
    with app.app_context():
        # Crear las tablas
        db.create_all()
        
        print("🧪 EJECUTANDO PRUEBAS DEL CRUD")
        print("=" * 50)
        
        # Limpiar datos existentes para la prueba
        Producto.query.delete()
        db.session.commit()
        
        # 1. Crear un producto de prueba (CREATE)
        print("1️⃣ Creando producto de prueba...")
        producto_test = Producto(
            sku="TEST-001",
            imagen="https://via.placeholder.com/300x300",
            cantidad=50,
            estado="Activo",
            precio_venta=99.99,
            categoria="Electrónicos",
            descripcion="Producto de prueba para verificar funcionalidad CRUD",
            politica_inventario="FIFO",
            proveedor="Proveedor Test",
            costo_unitario=60.00
        )
        
        db.session.add(producto_test)
        db.session.commit()
        print("   ✅ Producto creado exitosamente")
        
        # 2. Leer el producto (READ)
        print("2️⃣ Leyendo producto...")
        producto_leido = Producto.query.filter_by(sku="TEST-001").first()
        if producto_leido:
            print(f"   ✅ Producto encontrado: {producto_leido.sku}")
            print(f"      - Categoría: {producto_leido.categoria}")
            print(f"      - Precio: ${producto_leido.precio_venta}")
            print(f"      - Stock: {producto_leido.cantidad}")
        else:
            print("   ❌ Error: Producto no encontrado")
            return False
        
        # 3. Actualizar el producto (UPDATE)
        print("3️⃣ Actualizando producto...")
        producto_leido.cantidad = 75
        producto_leido.precio_venta = 89.99
        producto_leido.fecha_modificacion = datetime.now(timezone.utc)
        db.session.commit()
        
        # Verificar actualización
        producto_actualizado = Producto.query.filter_by(sku="TEST-001").first()
        if producto_actualizado.cantidad == 75 and producto_actualizado.precio_venta == 89.99:
            print("   ✅ Producto actualizado exitosamente")
            print(f"      - Nueva cantidad: {producto_actualizado.cantidad}")
            print(f"      - Nuevo precio: ${producto_actualizado.precio_venta}")
        else:
            print("   ❌ Error: Actualización fallida")
            return False
        
        # 4. Crear productos adicionales para probar la consulta
        print("4️⃣ Creando productos adicionales...")
        productos_adicionales = [
            Producto(
                sku="LAPTOP-001",
                cantidad=10,
                estado="Activo",
                precio_venta=1299.99,
                categoria="Electrónicos",
                descripcion="Laptop para gaming de alta gama",
                costo_unitario=900.00
            ),
            Producto(
                sku="CAMISA-001",
                cantidad=25,
                estado="Activo",
                precio_venta=49.99,
                categoria="Ropa",
                descripcion="Camisa casual de algodón",
                costo_unitario=25.00
            ),
            Producto(
                sku="LIBRO-001",
                cantidad=0,
                estado="Descontinuado",
                precio_venta=29.99,
                categoria="Libros",
                descripcion="Manual de programación Python",
                costo_unitario=15.00
            )
        ]
        
        for producto in productos_adicionales:
            db.session.add(producto)
        db.session.commit()
        print("   ✅ Productos adicionales creados")
        
        # 5. Consultar todos los productos
        print("5️⃣ Consultando todos los productos...")
        todos_productos = Producto.query.all()
        print(f"   ✅ Total de productos en la base de datos: {len(todos_productos)}")
        
        for producto in todos_productos:
            estado_emoji = "🟢" if producto.estado == "Activo" else "🔴" if producto.estado == "Descontinuado" else "🟡"
            stock_emoji = "📦" if producto.cantidad > 10 else "⚠️" if producto.cantidad > 0 else "❌"
            print(f"      {estado_emoji} {stock_emoji} {producto.sku} - {producto.categoria} - Stock: {producto.cantidad}")
        
        # 6. Eliminar producto de prueba (DELETE)
        print("6️⃣ Eliminando producto de prueba...")
        db.session.delete(producto_actualizado)
        db.session.commit()
        
        # Verificar eliminación
        producto_eliminado = Producto.query.filter_by(sku="TEST-001").first()
        if producto_eliminado is None:
            print("   ✅ Producto eliminado exitosamente")
        else:
            print("   ❌ Error: Producto no fue eliminado")
            return False
        
        print("\n🎉 TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("=" * 50)
        print("✅ El sistema CRUD está funcionando correctamente")
        print("🚀 Puedes iniciar la aplicación web con: python3 run.py")
        
        return True

if __name__ == '__main__':
    success = test_crud_operations()
    exit(0 if success else 1)