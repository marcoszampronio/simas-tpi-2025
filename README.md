# Sistema de Gestión de Productos - CRUD con Flask y SQLite

Este es un sistema completo de gestión de productos desarrollado con Python y Flask que permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) en una base de datos SQLite.

## Características

- **Interfaz web moderna** con diseño responsivo usando Bootstrap 5
- **Base de datos SQLite** para almacenamiento de productos
- **Gestión completa de productos** con los siguientes campos:
  - SKU único del producto
  - Imagen del producto (soporte para PNG, JPG, JPEG, GIF)
  - Cantidad en inventario
  - Estado (Disponible, Agotado, Descontinuado)
  - Precio de venta
  - Categoría
  - Descripción detallada
  - Política de gestión de inventario
  - Proveedor
  - Costo unitario

## Funcionalidades

### 1. Interfaz Principal
- Dos opciones principales:
  - **Alta de Productos**: Crear nuevos productos
  - **Consulta/Modificación/Baja**: Gestionar productos existentes

### 2. Alta de Productos
- Formulario completo para ingresar toda la información del producto
- Validación de campos requeridos
- Subida de imágenes
- Verificación de SKU único

### 3. Consulta de Productos
- Vista en formato de tabla/planilla
- Cada fila representa un producto
- Click en cualquier fila para ver detalles completos
- Información resumida visible (SKU, imagen, cantidad, estado, precio, categoría, proveedor)

### 4. Modificación de Productos
- Formulario pre-llenado con información actual
- Posibilidad de cambiar la imagen
- Validación de datos
- Confirmación de cambios

### 5. Eliminación de Productos
- Confirmación antes de eliminar
- Eliminación automática de imágenes asociadas
- No se puede deshacer

## Instalación y Uso

1. **Requisitos previos:**
   - Python 3.7 o superior
   - Flask
   - Los archivos de la aplicación

2. **Ejecutar la aplicación:**
   ```bash
   python app.py
   ```

3. **Acceder a la aplicación:**
   - Abrir el navegador web
   - Ir a `http://127.0.0.1:5000/`

## Estructura del Proyecto

```
/workspace/
├── app.py                 # Archivo principal de la aplicación Flask
├── productos.db           # Base de datos SQLite (se crea automáticamente)
├── templates/             # Plantillas HTML
│   ├── base.html         # Plantilla base con navegación común
│   ├── index.html        # Página principal con opciones
│   ├── alta.html         # Formulario de alta de productos
│   ├── consulta.html     # Lista de productos tipo planilla
│   ├── detalle.html      # Vista detallada de producto
│   └── modificar.html    # Formulario de modificación
├── static/               # Archivos estáticos
│   ├── css/
│   │   └── style.css     # Estilos adicionales
│   └── uploads/          # Imágenes subidas (se crea automáticamente)
└── README.md             # Esta documentación
```

## Tecnologías Utilizadas

- **Backend:** Python 3, Flask
- **Base de datos:** SQLite
- **Frontend:** HTML5, Bootstrap 5, Font Awesome
- **JavaScript:** Bootstrap JS para componentes interactivos

## Características de Seguridad

- Validación de tipos de archivos para imágenes
- Verificación de SKU único
- Sanitización de nombres de archivos
- Confirmación antes de eliminar productos
- Manejo seguro de archivos subidos

## Uso de la Aplicación

1. **Inicio:** Selecciona "Alta de Productos" o "Consulta/Modificación/Baja"

2. **Crear producto:**
   - Llena todos los campos requeridos (marcados con *)
   - Sube una imagen opcional
   - Haz clic en "Guardar Producto"

3. **Gestionar productos:**
   - Ve la lista en formato de tabla
   - Haz clic en cualquier fila para ver detalles
   - Usa los botones de acción (Ver, Editar, Eliminar)
   - Confirma antes de eliminar

## Desarrollo

Para modificar o extender la aplicación:

- **Agregar campos:** Modificar la estructura de la tabla en `init_db()` y actualizar formularios
- **Cambiar estilos:** Editar `static/css/style.css`
- **Agregar funcionalidades:** Crear nuevas rutas en `app.py` y templates correspondientes

## Notas

- La base de datos se crea automáticamente en el primer inicio
- Las imágenes se almacenan en `static/uploads/`
- El SKU debe ser único para cada producto
- La aplicación incluye validaciones básicas de datos

## Soporte

Para soporte técnico o preguntas sobre el funcionamiento, revisa la documentación o el código fuente proporcionado.