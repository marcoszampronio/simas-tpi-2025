#!/usr/bin/env python3
"""
Script de inicio para el Sistema de Gestión de Productos
"""

from app_simple import app, init_db

if __name__ == '__main__':
    print("🚀 Iniciando Sistema de Gestión de Productos...")
    print("📊 Inicializando base de datos...")
    init_db()
    print("✅ Base de datos inicializada correctamente")
    print("🌐 Servidor iniciado en http://localhost:5000")
    print("📱 Presiona Ctrl+C para detener el servidor")
    print("-" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)