#!/usr/bin/env python3
"""
Script de inicio para el CRUD de Productos
Ejecuta la aplicación Flask con configuración optimizada
"""

import os
import sys
from app import app, db

def main():
    """Función principal para iniciar la aplicación"""
    
    print("=" * 60)
    print("🚀 INICIANDO CRUD DE PRODUCTOS")
    print("=" * 60)
    
    # Crear las tablas si no existen
    with app.app_context():
        db.create_all()
        print("✅ Base de datos inicializada correctamente")
    
    print("📊 Sistema de Gestión de Inventario")
    print("🌐 Accede a la aplicación en:")
    print("   • Local: http://localhost:5000")
    print("   • Red:   http://0.0.0.0:5000")
    print("\n💡 Funcionalidades disponibles:")
    print("   • Alta de productos")
    print("   • Consulta y modificación")
    print("   • Eliminación con confirmación")
    print("   • Vista detallada de productos")
    
    print("\n🔧 Para detener el servidor: Ctrl+C")
    print("=" * 60)
    
    try:
        # Iniciar la aplicación
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 Aplicación detenida correctamente")
        print("¡Gracias por usar el CRUD de Productos!")
    except Exception as e:
        print(f"\n❌ Error al iniciar la aplicación: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()