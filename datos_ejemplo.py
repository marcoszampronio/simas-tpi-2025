#!/usr/bin/env python3
"""
Script para insertar datos de ejemplo en la base de datos
"""

import sqlite3
from datetime import datetime

def insertar_datos_ejemplo():
    """Insertar productos de ejemplo en la base de datos"""
    
    # Conectar a la base de datos
    conn = sqlite3.connect('productos.db')
    cursor = conn.cursor()
    
    # Verificar si ya hay datos
    cursor.execute('SELECT COUNT(*) FROM producto')
    count = cursor.fetchone()[0]
    
    if count > 0:
        print("⚠️  Ya existen productos en la base de datos")
        respuesta = input("¿Desea agregar más productos de ejemplo? (s/n): ")
        if respuesta.lower() != 's':
            conn.close()
            return
    
    # Datos de ejemplo
    productos_ejemplo = [
        {
            'sku': 'LAP001',
            'imagen': 'https://via.placeholder.com/300x200?text=Laptop',
            'cantidad': 25,
            'estado': 'Activo',
            'precio_venta': 899.99,
            'categoria': 'Electrónicos',
            'descripcion': 'Laptop de alta gama con procesador Intel i7, 16GB RAM, SSD 512GB',
            'politica_gestion_inventario': 'FIFO',
            'proveedor': 'TechSupply Corp',
            'costo_unitario': 650.00
        },
        {
            'sku': 'MOUSE002',
            'imagen': 'https://via.placeholder.com/300x200?text=Mouse',
            'cantidad': 150,
            'estado': 'Activo',
            'precio_venta': 29.99,
            'categoria': 'Accesorios',
            'descripcion': 'Mouse inalámbrico ergonómico con sensor óptico de alta precisión',
            'politica_gestion_inventario': 'FIFO',
            'proveedor': 'AccesoriosPro',
            'costo_unitario': 15.50
        },
        {
            'sku': 'TECL003',
            'imagen': 'https://via.placeholder.com/300x200?text=Teclado',
            'cantidad': 75,
            'estado': 'Activo',
            'precio_venta': 89.99,
            'categoria': 'Accesorios',
            'descripcion': 'Teclado mecánico RGB con switches Cherry MX Blue',
            'politica_gestion_inventario': 'FIFO',
            'proveedor': 'AccesoriosPro',
            'costo_unitario': 45.00
        },
        {
            'sku': 'MON004',
            'imagen': 'https://via.placeholder.com/300x200?text=Monitor',
            'cantidad': 40,
            'estado': 'Activo',
            'precio_venta': 299.99,
            'categoria': 'Monitores',
            'descripcion': 'Monitor LED 24 pulgadas Full HD con tiempo de respuesta 1ms',
            'politica_gestion_inventario': 'FIFO',
            'proveedor': 'DisplayTech',
            'costo_unitario': 180.00
        },
        {
            'sku': 'AUD005',
            'imagen': 'https://via.placeholder.com/300x200?text=Auriculares',
            'cantidad': 60,
            'estado': 'Activo',
            'precio_venta': 149.99,
            'categoria': 'Audio',
            'descripcion': 'Auriculares gaming con cancelación de ruido y micrófono retráctil',
            'politica_gestion_inventario': 'FIFO',
            'proveedor': 'AudioMax',
            'costo_unitario': 75.00
        },
        {
            'sku': 'WEB006',
            'imagen': 'https://via.placeholder.com/300x200?text=Webcam',
            'cantidad': 30,
            'estado': 'Activo',
            'precio_venta': 79.99,
            'categoria': 'Accesorios',
            'descripcion': 'Webcam HD 1080p con micrófono integrado y autofocus',
            'politica_gestion_inventario': 'FIFO',
            'proveedor': 'VideoTech',
            'costo_unitario': 35.00
        },
        {
            'sku': 'CAB007',
            'imagen': 'https://via.placeholder.com/300x200?text=Cable',
            'cantidad': 200,
            'estado': 'Activo',
            'precio_venta': 12.99,
            'categoria': 'Cables',
            'descripcion': 'Cable USB-C a USB-A de 2 metros con soporte para carga rápida',
            'politica_gestion_inventario': 'FIFO',
            'proveedor': 'CablePro',
            'costo_unitario': 4.50
        },
        {
            'sku': 'ADAP008',
            'imagen': 'https://via.placeholder.com/300x200?text=Adaptador',
            'cantidad': 45,
            'estado': 'Activo',
            'precio_venta': 24.99,
            'categoria': 'Adaptadores',
            'descripcion': 'Adaptador USB-C multipuerto con HDMI, USB 3.0 y carga',
            'politica_gestion_inventario': 'FIFO',
            'proveedor': 'ConnectTech',
            'costo_unitario': 12.00
        },
        {
            'sku': 'ALM009',
            'imagen': 'https://via.placeholder.com/300x200?text=Almacenamiento',
            'cantidad': 20,
            'estado': 'Activo',
            'precio_venta': 199.99,
            'categoria': 'Almacenamiento',
            'descripcion': 'SSD externo USB 3.0 de 1TB con velocidad de lectura 550MB/s',
            'politica_gestion_inventario': 'FIFO',
            'proveedor': 'StorageMax',
            'costo_unitario': 120.00
        },
        {
            'sku': 'CAR010',
            'imagen': 'https://via.placeholder.com/300x200?text=Tarjeta',
            'cantidad': 0,
            'estado': 'Inactivo',
            'precio_venta': 89.99,
            'categoria': 'Tarjetas',
            'descripcion': 'Tarjeta gráfica externa USB-C con 4GB VRAM',
            'politica_gestion_inventario': 'FIFO',
            'proveedor': 'GraphicsPro',
            'costo_unitario': 45.00
        }
    ]
    
    try:
        # Insertar productos
        for producto in productos_ejemplo:
            cursor.execute('''
                INSERT INTO producto (sku, imagen, cantidad, estado, precio_venta, categoria, 
                                     descripcion, politica_gestion_inventario, proveedor, costo_unitario)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                producto['sku'],
                producto['imagen'],
                producto['cantidad'],
                producto['estado'],
                producto['precio_venta'],
                producto['categoria'],
                producto['descripcion'],
                producto['politica_gestion_inventario'],
                producto['proveedor'],
                producto['costo_unitario']
            ))
        
        conn.commit()
        print(f"✅ Se insertaron {len(productos_ejemplo)} productos de ejemplo exitosamente")
        
        # Mostrar resumen
        cursor.execute('SELECT COUNT(*) FROM producto')
        total = cursor.fetchone()[0]
        print(f"📊 Total de productos en la base de datos: {total}")
        
        cursor.execute('SELECT COUNT(*) FROM producto WHERE estado = "Activo"')
        activos = cursor.fetchone()[0]
        print(f"🟢 Productos activos: {activos}")
        
        cursor.execute('SELECT COUNT(*) FROM producto WHERE cantidad > 0')
        con_stock = cursor.fetchone()[0]
        print(f"📦 Productos con stock: {con_stock}")
        
    except sqlite3.IntegrityError as e:
        print(f"❌ Error de integridad: {e}")
    except Exception as e:
        print(f"❌ Error al insertar datos: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    print("📝 Insertando datos de ejemplo en la base de datos...")
    print("-" * 50)
    insertar_datos_ejemplo()
    print("-" * 50)
    print("🎉 Proceso completado!")
    print("💡 Ahora puedes ejecutar 'python3 run.py' para iniciar la aplicación")