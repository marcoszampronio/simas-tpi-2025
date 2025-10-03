# CRUD de Productos Web con Flask

Sistema web completo para la gestión de productos con operaciones CRUD (Crear, Leer, Actualizar, Eliminar) desarrollado en Python con Flask y SQLite.

## 🚀 Características

- **Interfaz intuitiva** con Bootstrap 5 y Font Awesome
- **Base de datos SQLite** para almacenamiento local
- **Operaciones CRUD completas** para productos
- **Validación de datos** en frontend y backend
- **Interfaz responsive** adaptable a dispositivos móviles
- **Gestión de inventario** con políticas configurables

## 📋 Campos del Producto

Cada producto incluye los siguientes campos:

- **SKU del Producto** (único, requerido)
- **Imagen** (URL opcional)
- **Cantidad** (requerido)
- **Estado** (Activo/Inactivo/Descontinuado)
- **Precio de Venta** (requerido)
- **Categoría** (requerido)
- **Descripción** (opcional)
- **Política de Gestión de Inventario** (FIFO/LIFO/PROMEDIO/ESPECÍFICO)
- **Proveedor** (requerido)
- **Costo Unitario** (requerido)

## 🛠️ Instalación

### Requisitos Previos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   # Si tienes el código en un repositorio
   git clone <url-del-repositorio>
   cd crud-productos-flask
   ```

2. **Crear entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   
   # En Windows
   venv\Scripts\activate
   
   # En Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```

5. **Abrir en el navegador**
   ```
   http://localhost:5000
   ```

## 📁 Estructura del Proyecto

```
crud-productos-flask/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias del proyecto
├── README.md             # Este archivo
├── templates/            # Plantillas HTML
│   ├── base.html         # Plantilla base
│   ├── index.html        # Página principal
│   ├── alta.html         # Formulario de alta
│   ├── consulta.html     # Tabla de productos
│   ├── detalle_producto.html  # Vista detallada
│   └── editar_producto.html   # Formulario de edición
└── static/               # Archivos estáticos
    ├── css/
    │   └── style.css     # Estilos personalizados
    └── js/
        └── script.js     # JavaScript personalizado
```

## 🎯 Funcionalidades

### Página Principal
- Selección entre **Alta** y **Consulta/Modificación/Baja**
- Información del sistema y campos disponibles

### Alta de Productos
- Formulario completo con validación
- Campos obligatorios y opcionales claramente marcados
- Validación de SKU único
- Cálculo automático de margen de ganancia

### Consulta de Productos
- Tabla responsive con todos los productos
- Información visual del estado del inventario
- Acciones rápidas: Ver, Editar, Eliminar
- Filas clickeables para ver detalles

### Detalle de Producto
- Vista completa de la información del producto
- Información financiera calculada automáticamente
- Acciones de edición y navegación

### Edición de Productos
- Formulario pre-llenado con datos actuales
- Validación de cambios
- Actualización de fecha de modificación

## 🔧 Configuración

### Base de Datos
La aplicación utiliza SQLite por defecto. La base de datos se crea automáticamente al ejecutar la aplicación por primera vez.

### Personalización
- **Clave secreta**: Cambiar en `app.py` línea 8
- **Base de datos**: Modificar la URI en `app.py` línea 9
- **Estilos**: Editar `static/css/style.css`
- **Funcionalidad**: Modificar `static/js/script.js`

## 🚀 Uso

1. **Iniciar la aplicación**
   ```bash
   python app.py
   ```

2. **Acceder a la interfaz web**
   - Abrir navegador en `http://localhost:5000`

3. **Gestionar productos**
   - **Alta**: Agregar nuevos productos
   - **Consulta**: Ver, editar o eliminar productos existentes

## 📊 Características Técnicas

- **Framework**: Flask 2.3.3
- **Base de datos**: SQLite con SQLAlchemy
- **Frontend**: Bootstrap 5 + Font Awesome
- **Validación**: HTML5 + JavaScript + Python
- **Responsive**: Diseño adaptable a móviles

## 🔒 Seguridad

- Validación de datos en frontend y backend
- Protección contra inyección SQL (SQLAlchemy ORM)
- Sanitización de entradas de usuario
- Confirmación antes de eliminar productos

## 🐛 Solución de Problemas

### Error de dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Error de puerto ocupado
Cambiar el puerto en `app.py`:
```python
app.run(debug=True, port=5001)
```

### Error de base de datos
Eliminar el archivo `productos.db` y reiniciar la aplicación.

## 📝 Notas de Desarrollo

- La aplicación se ejecuta en modo debug por defecto
- Los cambios en archivos estáticos requieren recarga del navegador
- La base de datos se crea automáticamente en la primera ejecución

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el proyecto
2. Crear una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

## 📞 Soporte

Para soporte o preguntas, crear un issue en el repositorio del proyecto.