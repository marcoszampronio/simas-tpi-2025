# CRUD de Productos - Sistema de Gestión de Inventario

## Descripción

Sistema web completo para la gestión de productos desarrollado con **Python Flask** y **SQLite**. Permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre un inventario de productos con una interfaz web moderna y responsive.

## Características

### Funcionalidades Principales
- ✅ **Alta de Productos**: Formulario completo para registrar nuevos productos
- ✅ **Consulta de Productos**: Vista de tabla con todos los productos registrados
- ✅ **Modificación de Productos**: Edición de información existente
- ✅ **Baja de Productos**: Eliminación con confirmación
- ✅ **Detalle de Productos**: Vista completa de información individual

### Campos de Producto
- **SKU del Producto** (único, requerido)
- **Imagen** (URL opcional)
- **Cantidad** (stock disponible)
- **Estado** (Activo/Inactivo/Descontinuado)
- **Precio de Venta** (requerido)
- **Categoría** (Electrónicos, Ropa, Hogar, etc.)
- **Descripción** (texto libre)
- **Política de Gestión de Inventario** (FIFO, LIFO, etc.)
- **Proveedor** (nombre del proveedor)
- **Costo Unitario** (requerido)
- **Fechas** (creación y modificación automáticas)

### Interfaz de Usuario
- 🎨 **Diseño Moderno**: Bootstrap 5 con estilos personalizados
- 📱 **Responsive**: Adaptable a dispositivos móviles
- 🔍 **Navegación Intuitiva**: Menú claro y accesible
- ⚡ **Interactividad**: Efectos hover y transiciones suaves
- 📊 **Vista de Tabla**: Información organizada y fácil de leer
- 🖼️ **Previsualización**: Imágenes de productos en miniatura

## Instalación y Uso

### Requisitos Previos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecutar la aplicación**:
   ```bash
   python3 app.py
   ```

3. **Acceder a la aplicación**:
   - Abrir navegador web
   - Ir a: `http://localhost:5000`

### Estructura de la Aplicación

```
/workspace/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias Python
├── productos.db          # Base de datos SQLite (se crea automáticamente)
├── templates/            # Plantillas HTML
│   ├── base.html         # Plantilla base
│   ├── index.html        # Página principal
│   ├── alta.html         # Formulario de alta
│   ├── consulta.html     # Vista de consulta/tabla
│   ├── editar.html       # Formulario de edición
│   └── detalle.html      # Vista de detalle
└── static/
    └── css/
        └── style.css     # Estilos personalizados
```

## Guía de Uso

### 1. Página Principal
Al acceder a la aplicación, verás dos opciones principales:
- **Alta de Productos**: Para crear nuevos productos
- **Consulta y Gestión**: Para ver, modificar o eliminar productos

### 2. Crear Producto (Alta)
- Completa el formulario con la información del producto
- Los campos marcados con (*) son obligatorios
- El SKU debe ser único en el sistema
- Selecciona una categoría del menú desplegable
- Opcionalmente agrega una URL de imagen

### 3. Consultar Productos
- Ve todos los productos en formato de tabla
- Haz clic en cualquier fila para ver detalles completos
- Usa los botones de acción para:
  - 👁️ Ver detalles completos
  - ✏️ Editar información
  - 🗑️ Eliminar producto (con confirmación)

### 4. Editar Producto
- Modifica cualquier campo del producto
- Las fechas de creación y modificación se actualizan automáticamente
- Guarda los cambios o cancela para volver

### 5. Ver Detalles
- Vista completa de toda la información del producto
- Cálculo automático del margen de ganancia
- Acceso directo a edición y eliminación

## Características Técnicas

### Base de Datos
- **SQLite**: Base de datos ligera y sin configuración
- **SQLAlchemy**: ORM para manejo de datos
- **Migraciones**: Creación automática de tablas

### Seguridad
- Validación de formularios
- Confirmación para eliminaciones
- Manejo de errores con mensajes informativos

### Interfaz
- **Bootstrap 5**: Framework CSS moderno
- **Font Awesome**: Iconos vectoriales
- **CSS Personalizado**: Estilos únicos y animaciones
- **JavaScript**: Interactividad y confirmaciones

## Personalización

### Agregar Nuevas Categorías
Edita el archivo `templates/alta.html` y `templates/editar.html` en las secciones de select de categoría.

### Modificar Campos
Para agregar o modificar campos del producto:
1. Actualiza el modelo `Producto` en `app.py`
2. Modifica los formularios en las plantillas HTML
3. Ajusta las rutas de creación y actualización

### Cambiar Estilos
Modifica el archivo `static/css/style.css` para personalizar la apariencia.

## Solución de Problemas

### Error de Dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Puerto Ocupado
Si el puerto 5000 está ocupado, modifica la línea final en `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Cambiar puerto
```

### Base de Datos
La base de datos se crea automáticamente. Para reiniciar:
```bash
rm productos.db  # Eliminar base existente
python3 app.py   # Recrear automáticamente
```

## Próximas Mejoras

- 🔍 Búsqueda y filtrado de productos
- 📊 Reportes y estadísticas
- 📤 Exportación de datos (CSV, Excel)
- 🔐 Sistema de autenticación
- 📸 Subida de imágenes local
- 🏷️ Gestión de categorías dinámicas
- 📱 API REST para integración

---

**Desarrollado con Flask y SQLite** - Sistema completo de gestión de inventario