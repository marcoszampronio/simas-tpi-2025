#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad del sistema de gestión de productos
"""

import sqlite3
import os
from app import init_db, get_db_connection

def test_database_creation():
    """Prueba la creación de la base de datos"""
    print("🔍 Probando creación de base de datos...")
    
    # Verificar que la base de datos existe
    if os.path.exists('productos.db'):
        print("✅ Base de datos 'productos.db' creada correctamente")
    else:
        print("❌ Error: Base de datos no encontrada")
        return False
    
    # Verificar la estructura de la tabla
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='productos'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("✅ Tabla 'productos' creada correctamente")
        else:
            print("❌ Error: Tabla 'productos' no encontrada")
            return False
        
        # Verificar las columnas de la tabla
        cursor.execute("PRAGMA table_info(productos)")
        columns = cursor.fetchall()
        
        expected_columns = [
            'id', 'sku', 'imagen', 'cantidad', 'estado', 'precio_venta',
            'categoria', 'descripcion', 'politica_gestion_inventario',
            'proveedor', 'costo_unitario', 'fecha_creacion', 'fecha_modificacion'
        ]
        
        actual_columns = [col[1] for col in columns]
        
        if all(col in actual_columns for col in expected_columns):
            print("✅ Todas las columnas esperadas están presentes")
        else:
            print("❌ Error: Faltan columnas en la tabla")
            return False
            
    except Exception as e:
        print(f"❌ Error al verificar la estructura: {e}")
        return False
    finally:
        conn.close()
    
    return True

def test_insert_product():
    """Prueba la inserción de un producto de prueba"""
    print("\n🔍 Probando inserción de producto...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Insertar un producto de prueba
        cursor.execute('''
            INSERT INTO productos (sku, imagen, cantidad, estado, precio_venta, categoria, 
                                 descripcion, politica_gestion_inventario, proveedor, costo_unitario)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', ('TEST-001', 'https://via.placeholder.com/150', 10, 'Activo', 99.99, 'Electrónicos', 
              'Producto de prueba', 'FIFO', 'Proveedor Test', 50.00))
        
        conn.commit()
        
        # Verificar que se insertó correctamente
        cursor.execute("SELECT * FROM productos WHERE sku = 'TEST-001'")
        product = cursor.fetchone()
        
        if product:
            print("✅ Producto de prueba insertado correctamente")
            print(f"   SKU: {product['sku']}")
            print(f"   Categoría: {product['categoria']}")
            print(f"   Precio: ${product['precio_venta']}")
            return True
        else:
            print("❌ Error: Producto no encontrado después de la inserción")
            return False
            
    except Exception as e:
        print(f"❌ Error al insertar producto: {e}")
        return False
    finally:
        conn.close()

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas del Sistema de Gestión de Productos\n")
    
    # Inicializar la base de datos
    init_db()
    
    # Ejecutar todas las pruebas
    tests = [
        test_database_creation,
        test_insert_product
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Resultados de las pruebas:")
    print(f"   ✅ Pruebas exitosas: {passed}/{total}")
    print(f"   ❌ Pruebas fallidas: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 ¡Todas las pruebas pasaron! El sistema está funcionando correctamente.")
        print("\n📝 Para usar la aplicación:")
        print("   1. Ejecuta: python3 app.py")
        print("   2. Abre tu navegador en: http://localhost:5001")
        print("   3. ¡Disfruta gestionando tus productos!")
    else:
        print("\n⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")

if __name__ == '__main__':
    main()
