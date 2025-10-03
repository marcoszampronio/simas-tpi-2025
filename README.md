# Sistema de Gestión de Productos - CRUD Web con Flask

Un sistema completo de gestión de productos desarrollado con Python Flask y SQLite que permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre productos de inventario.

## 🚀 Características

- **Interfaz intuitiva** con diseño moderno y responsivo
- **Gestión completa de productos** con todos los campos necesarios
- **Base de datos SQLite** para almacenamiento local
- **Validaciones** en frontend y backend
- **Interfaz de tabla** para consulta rápida de productos
- **Modales** para confirmaciones y detalles
- **Diseño responsivo** que funciona en dispositivos móviles

## 📋 Campos del Producto

Cada producto incluye los siguientes campos:

- **SKU del Producto** (único, requerido)
- **Imagen** (URL opcional)
- **Cantidad** (stock disponible)
- **Estado** (Activo, Inactivo, Descontinuado)
- **Precio de Venta** (requerido)
- **Categoría** (requerido)
- **Descripción** (opcional)
- **Política de Gestión de Inventario** (FIFO, LIFO, Promedio, Específico)
- **Proveedor** (requerido)
- **Costo Unitario** (requerido)
- **Fechas** de creación y modificación automáticas

## 🛠️ Instalación y Configuración

### Requisitos Previos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   # Si tienes git instalado
   git clone <url-del-repositorio>
   cd sistema-productos-flask
   ```

2. **Crear un entorno virtual (recomendado)**
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
   # Opción 1: Usar el script de inicio
   python3 run.py
   
   # Opción 2: Ejecutar directamente
   python3 app_simple.py
   ```

5. **Acceder a la aplicación**
   - Abrir el navegador en: `http://localhost:5000`
   - La base de datos SQLite se creará automáticamente

## 📱 Uso del Sistema

### Página Principal
- **Alta de Productos**: Acceso directo al formulario de creación
- **Consulta y Gestión**: Acceso a la tabla de productos existentes

### Alta de Productos
1. Completar el formulario con los datos del producto
2. Los campos marcados con * son obligatorios
3. Confirmar la creación en el modal de confirmación
4. El sistema validará que el SKU sea único

### Consulta y Gestión
1. **Vista de tabla**: Lista todos los productos con información resumida
2. **Click en fila**: Ver detalles completos del producto
3. **Botones de acción**:
   - 👁️ **Ver**: Mostrar detalles completos
   - ✏️ **Editar**: Modificar el producto
   - 🗑️ **Eliminar**: Borrar el producto (con confirmación)

### Detalles del Producto
- Información completa del producto
- Cálculo automático de margen de ganancia
- Valor total del stock
- Historial de fechas de creación y modificación

### Edición de Productos
- Formulario pre-cargado con datos actuales
- Validación de SKU único (si se modifica)
- Confirmación antes de guardar cambios
- Opción de eliminar desde la edición

## 🗄️ Estructura de la Base de Datos

La base de datos SQLite (`productos.db`) se crea automáticamente con la siguiente estructura:

```sql
CREATE TABLE producto (
    id INTEGER PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    imagen VARCHAR(200),
    cantidad INTEGER NOT NULL DEFAULT 0,
    estado VARCHAR(20) NOT NULL DEFAULT 'Activo',
    precio_venta FLOAT NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    descripcion TEXT,
    politica_gestion_inventario VARCHAR(100),
    proveedor VARCHAR(100) NOT NULL,
    costo_unitario FLOAT NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🎨 Características de la Interfaz

- **Diseño moderno** con Bootstrap 5
- **Iconos FontAwesome** para mejor UX
- **Colores semánticos** para estados y acciones
- **Animaciones suaves** y transiciones
- **Responsive design** para móviles y tablets
- **Modales** para confirmaciones y detalles
- **Validaciones en tiempo real**

## 🔧 API Endpoints

El sistema incluye endpoints REST para integración:

- `POST /api/productos` - Crear nuevo producto
- `PUT /api/productos/<id>` - Actualizar producto
- `DELETE /api/productos/<id>` - Eliminar producto
- `GET /producto/<id>` - Ver detalles del producto

## 📁 Estructura del Proyecto

```
sistema-productos-flask/
├── app_simple.py          # Aplicación principal Flask (versión simplificada)
├── run.py                 # Script de inicio con mensajes informativos
├── requirements.txt       # Dependencias Python
├── README.md             # Este archivo
├── productos.db           # Base de datos SQLite (se crea automáticamente)
├── templates/            # Templates HTML
│   ├── base.html         # Template base
│   ├── index.html        # Página principal
│   ├── alta.html         # Formulario de alta
│   ├── consulta.html     # Tabla de productos
│   ├── detalle_producto.html  # Detalles del producto
│   └── editar_producto.html   # Formulario de edición
└── static/               # Archivos estáticos
    ├── css/
    │   └── style.css     # Estilos personalizados
    └── js/
        └── main.js       # JavaScript personalizado
```

## 🚀 Funcionalidades Avanzadas

- **Cálculo automático de márgenes** en tiempo real
- **Validación de URLs** para imágenes
- **Búsqueda en tiempo real** en la tabla
- **Estados visuales** con badges de colores
- **Confirmaciones** antes de acciones destructivas
- **Mensajes de éxito/error** automáticos
- **Preview de imágenes** al cargar URLs

## 🛡️ Validaciones

- **SKU único** en toda la base de datos
- **Campos obligatorios** marcados claramente
- **Validación de tipos** (números, URLs, fechas)
- **Confirmaciones** para acciones críticas
- **Manejo de errores** con mensajes informativos

## 📱 Compatibilidad

- **Navegadores**: Chrome, Firefox, Safari, Edge
- **Dispositivos**: Desktop, Tablet, Mobile
- **Sistemas**: Windows, macOS, Linux

## 🔮 Posibles Mejoras Futuras

- Autenticación de usuarios
- Categorías dinámicas
- Importación/exportación de datos
- Reportes y estadísticas
- Búsqueda avanzada con filtros
- Historial de cambios
- Backup automático de la base de datos

## 📞 Soporte

Para consultas o problemas con el sistema, revisar:
1. Los logs de la consola del navegador
2. Los mensajes de error en la aplicación
3. La estructura de la base de datos
4. Las dependencias instaladas

---

**Desarrollado con ❤️ usando Python Flask y Bootstrap**