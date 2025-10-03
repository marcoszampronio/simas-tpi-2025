# Sistema de Gestión de Productos con Flask

Un sistema web completo para la gestión de productos con operaciones CRUD (Crear, Leer, Actualizar, Eliminar) desarrollado en Python con Flask y SQLite.

## Características

- ✅ **Interfaz Principal**: Menú con dos opciones principales (Alta y Gestión)
- ✅ **Alta de Productos**: Formulario completo para agregar nuevos productos
- ✅ **Gestión de Productos**: Tabla interactiva para consultar, modificar y eliminar productos
- ✅ **Base de Datos SQLite**: Almacenamiento local de datos
- ✅ **Interfaz Moderna**: Diseño responsive con Bootstrap y CSS personalizado
- ✅ **Validaciones**: Control de datos y validaciones del lado cliente y servidor

## Campos del Producto

Cada producto incluye los siguientes campos:

- **SKU del Producto**: Identificador único (obligatorio)
- **Imagen**: URL de la imagen del producto
- **Cantidad**: Stock disponible (obligatorio)
- **Estado**: Activo, Inactivo, Descontinuado (obligatorio)
- **Precio de Venta**: Precio al público (obligatorio)
- **Categoría**: Clasificación del producto (obligatorio)
- **Descripción**: Descripción detallada del producto
- **Política de Gestión de Inventario**: FIFO, LIFO, Precio Promedio, Específico
- **Proveedor**: Nombre del proveedor
- **Costo Unitario**: Costo de adquisición (obligatorio)

## Instalación y Uso

### Requisitos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   # Si tienes git instalado
   git clone <url-del-repositorio>
   cd sistema-gestion-productos
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```

4. **Acceder a la aplicación**
   - Abrir el navegador web
   - Ir a: `http://localhost:5000`

### Estructura del Proyecto

```
sistema-gestion-productos/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias del proyecto
├── README.md             # Este archivo
├── productos.db          # Base de datos SQLite (se crea automáticamente)
├── templates/            # Plantillas HTML
│   ├── base.html         # Plantilla base
│   ├── index.html        # Página principal
│   ├── alta.html         # Formulario de alta
│   ├── gestion.html      # Lista de productos
│   └── producto_detalle.html # Detalle y edición
└── static/               # Archivos estáticos
    ├── css/
    │   └── style.css     # Estilos personalizados
    └── js/
        └── main.js       # JavaScript personalizado
```

## Funcionalidades

### 1. Página Principal (`/`)
- Interfaz de bienvenida con dos opciones principales
- Diseño moderno y responsive
- Información del sistema

### 2. Alta de Productos (`/alta`)
- Formulario completo con todos los campos
- Validaciones en tiempo real
- Categorías predefinidas
- Validación de precios (precio de venta >= costo unitario)

### 3. Gestión de Productos (`/gestion`)
- Tabla interactiva con todos los productos
- Búsqueda en tiempo real
- Estados visuales del stock (alto, medio, bajo)
- Acciones rápidas (ver, eliminar)
- Filas clickeables para ver detalles

### 4. Detalle de Producto (`/producto/<id>`)
- Vista completa de la información del producto
- Modo de edición con toggle
- Validaciones de datos
- Confirmación antes de eliminar
- Historial de modificaciones

## Características Técnicas

### Base de Datos
- **SQLite**: Base de datos local, no requiere configuración adicional
- **Tabla productos**: Estructura optimizada con índices automáticos
- **Timestamps**: Registro de fechas de creación y modificación

### Seguridad
- **Validación de datos**: Tanto en cliente como servidor
- **Prevención de duplicados**: SKU único por producto
- **Confirmaciones**: Para operaciones destructivas

### Interfaz de Usuario
- **Bootstrap 5**: Framework CSS moderno
- **Font Awesome**: Iconografía profesional
- **Responsive**: Adaptable a dispositivos móviles
- **Animaciones**: Transiciones suaves y efectos visuales

## Uso del Sistema

### Agregar un Producto
1. Ir a la página principal
2. Hacer clic en "Agregar Producto"
3. Completar el formulario con los datos requeridos
4. Hacer clic en "Guardar Producto"

### Gestionar Productos Existentes
1. Ir a la página principal
2. Hacer clic en "Gestionar Productos"
3. En la tabla, puedes:
   - **Buscar**: Usar el campo de búsqueda
   - **Ver detalles**: Hacer clic en cualquier fila
   - **Eliminar**: Usar el botón de eliminar (con confirmación)

### Editar un Producto
1. Desde la lista de productos, hacer clic en una fila
2. En la página de detalle, hacer clic en "Editar"
3. Modificar los campos necesarios
4. Hacer clic en "Guardar Cambios"

## Solución de Problemas

### Error de Puerto en Uso
Si el puerto 5000 está ocupado, modifica la última línea de `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Cambiar puerto
```

### Problemas con la Base de Datos
- La base de datos se crea automáticamente al ejecutar la aplicación
- Si hay problemas, elimina el archivo `productos.db` y reinicia la aplicación

### Dependencias Faltantes
```bash
pip install Flask==2.3.3 Werkzeug==2.3.7
```

## Desarrollo y Personalización

### Agregar Nuevas Categorías
Editar el archivo `templates/alta.html` y `templates/producto_detalle.html`:
```html
<option value="Nueva Categoría">Nueva Categoría</option>
```

### Modificar Campos
1. Actualizar la tabla en `app.py` (función `init_db()`)
2. Modificar los formularios en las plantillas HTML
3. Actualizar las rutas de Flask según sea necesario

### Personalizar Estilos
Editar el archivo `static/css/style.css` para cambiar colores, fuentes y diseño.

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Soporte

Para reportar problemas o solicitar nuevas funcionalidades, crear un issue en el repositorio del proyecto.