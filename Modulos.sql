SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

DROP DATABASE IF EXISTS simas_tpi;
CREATE DATABASE simas_tpi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE simas_tpi;

-- IMPORTANTE: Esquema simplificado con EXACTAMENTE 4 tablas (una por módulo)

-- 1) Módulo: Artículos
CREATE TABLE articulos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  sku VARCHAR(50) NOT NULL UNIQUE,
  nombre VARCHAR(150) NOT NULL,
  descripcion TEXT NULL,
  foto_url VARCHAR(255) NULL,
  clasificacion_json LONGTEXT NULL,
  ubicacion_json LONGTEXT NULL,
  costos_json LONGTEXT NULL,
  precio_venta DECIMAL(12,2) NOT NULL DEFAULT 0.00,
  stock_disponible INT NOT NULL DEFAULT 0,
  inventario_ciclico INT NOT NULL DEFAULT 0,
  stock_seguridad INT NOT NULL DEFAULT 0,
  fecha_alta DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  estado ENUM('activo','inactivo') NOT NULL DEFAULT 'activo',
  -- Columnas generadas para indexar campos frecuentes del JSON
  marca VARCHAR(80) AS (JSON_UNQUOTE(JSON_EXTRACT(clasificacion_json, '$.marca'))) STORED,
  categoria VARCHAR(80) AS (JSON_UNQUOTE(JSON_EXTRACT(clasificacion_json, '$.categoria'))) STORED,
  proveedor VARCHAR(120) AS (JSON_UNQUOTE(JSON_EXTRACT(clasificacion_json, '$.proveedor'))) STORED,
  CHECK (clasificacion_json IS NULL OR JSON_VALID(clasificacion_json)),
  CHECK (ubicacion_json IS NULL OR JSON_VALID(ubicacion_json)),
  CHECK (costos_json IS NULL OR JSON_VALID(costos_json)),
  KEY idx_articulos_marca (marca),
  KEY idx_articulos_categoria (categoria),
  KEY idx_articulos_proveedor (proveedor)
) ENGINE=InnoDB;

-- 2) Módulo: Clientes
CREATE TABLE clientes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(120) NOT NULL,
  apellido VARCHAR(120) NULL,
  doc_tipo ENUM('DNI','CUIT') NOT NULL,
  doc_numero VARCHAR(30) NOT NULL,
  telefono VARCHAR(40) NULL,
  email VARCHAR(120) NULL,
  direccion_json LONGTEXT NULL,
  datos_fiscales_json LONGTEXT NULL,
  fecha_alta DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  fecha_baja DATETIME NULL,
  activo TINYINT(1) NOT NULL DEFAULT 1,
  historial_compras_json LONGTEXT NULL,
  CHECK (direccion_json IS NULL OR JSON_VALID(direccion_json)),
  CHECK (datos_fiscales_json IS NULL OR JSON_VALID(datos_fiscales_json)),
  CHECK (historial_compras_json IS NULL OR JSON_VALID(historial_compras_json)),
  UNIQUE KEY uq_cliente_doc (doc_tipo, doc_numero)
) ENGINE=InnoDB;

-- 3) Módulo: Usuarios
CREATE TABLE usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(150) NOT NULL,
  categoria ENUM('administrador','cajero','operario_deposito','supervisor','invitado') NOT NULL,
  email VARCHAR(120) NOT NULL UNIQUE,
  telefono VARCHAR(40) NULL,
  dni VARCHAR(20) NULL,
  permisos_json LONGTEXT NULL,
  acciones_json LONGTEXT NULL,
  fecha_alta DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  activo TINYINT(1) NOT NULL DEFAULT 1,
  CHECK (permisos_json IS NULL OR JSON_VALID(permisos_json)),
  CHECK (acciones_json IS NULL OR JSON_VALID(acciones_json))
) ENGINE=InnoDB;

-- 4) Módulo: Ventas y Stock (transacciones y movimientos)
CREATE TABLE ventas_stock (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  fecha_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tipo_transaccion ENUM('venta','compra','ajuste') NOT NULL,
  estado_transaccion ENUM('abierta','completada','devolucion','cancelada','recibida','pendiente') NOT NULL DEFAULT 'abierta',
  usuario_id INT NULL,
  cliente_id INT NULL,
  modo_pago VARCHAR(60) NULL,
  items_json LONGTEXT NULL,
  movimientos_json LONGTEXT NULL,
  totales_json LONGTEXT NULL,
  comprobantes_json LONGTEXT NULL,
  -- Denormalizaciones útiles
  subtotal DECIMAL(12,2) NULL,
  iva DECIMAL(12,2) NULL,
  descuento DECIMAL(12,2) NULL,
  total DECIMAL(12,2) NULL,
  CHECK (items_json IS NULL OR JSON_VALID(items_json)),
  CHECK (movimientos_json IS NULL OR JSON_VALID(movimientos_json)),
  CHECK (totales_json IS NULL OR JSON_VALID(totales_json)),
  CHECK (comprobantes_json IS NULL OR JSON_VALID(comprobantes_json)),
  KEY idx_vs_tipo_fecha (tipo_transaccion, fecha_hora),
  KEY idx_vs_usuario (usuario_id),
  KEY idx_vs_cliente (cliente_id)
) ENGINE=InnoDB;

-- Datos de ejemplo enriquecidos

-- Artículos (clasificación, ubicación y costos embebidos en JSON)
INSERT INTO articulos (
  sku, nombre, descripcion, foto_url,
  clasificacion_json, ubicacion_json, costos_json,
  precio_venta, stock_disponible, inventario_ciclico, stock_seguridad
) VALUES
  ('SKU-0001', 'Cargador USB-C 20W', 'Cargador rápido 20W', NULL,
   '{"marca":"ACME","categoria":"Accesorios","proveedor":"Proveedor ACME"}',
   '{"ubicacion":"Depósito Central","almacenes":[{"bin":"A-01"}]}',
   '{"costo_compra":3000,"costo_reorden":500,"costo_mantenimiento":150}',
   5999.00, 48, 20, 10),
  ('SKU-0002', 'Auriculares Bluetooth', 'Over-ear con cancelación', NULL,
   '{"marca":"Globex","categoria":"Electrónica","proveedor":"Proveedor ACME"}',
   '{"ubicacion":"Depósito Central","almacenes":[{"bin":"A-02"}]}',
   '{"costo_compra":15000,"costo_reorden":1000,"costo_mantenimiento":500}',
   34999.00, 19, 10, 5),
  ('SKU-0003', 'Cable HDMI 2.1', 'Cable 2m 8K', NULL,
   '{"marca":"ACME","categoria":"Accesorios","proveedor":"Proveedor ACME"}',
   '{"ubicacion":"Depósito Central","almacenes":[{"bin":"B-01"}]}',
   '{"costo_compra":1200,"costo_reorden":200,"costo_mantenimiento":50}',
   2999.00, 100, 30, 15);

-- Clientes
INSERT INTO clientes (
  nombre, apellido, doc_tipo, doc_numero, telefono, email,
  direccion_json, datos_fiscales_json, activo, historial_compras_json
) VALUES
  ('Juan','Pérez','DNI','12345678','+54 11 2222-2222','juan.perez@example.com',
   '{"calle":"Av. Siempre Viva 742","ciudad":"CABA","cp":"1000"}',
   '{"tipo_cliente":"consumidor_final"}',
   1, NULL),
  ('Empresa','XYZ SA','CUIT','30-87654321-0','+54 11 3333-3333','compras@xyz.com',
   '{"calle":"Av. Industria 1200","ciudad":"CABA","cp":"1100"}',
   '{"tipo_cliente":"empresa"}',
   1, NULL);

-- Usuarios
INSERT INTO usuarios (nombre, categoria, email, telefono, dni, permisos_json, acciones_json)
VALUES
  ('Admin Principal','administrador','admin@simas.local','+54 11 0000-0000','99.999.999',
   '{"modulos":["articulos","clientes","usuarios","ventas_stock"],"permisos":"full"}',
   '[{"accion":"login","ts":"2025-09-01 08:00:00"}]'),
  ('Caja 1','cajero','caja1@simas.local',NULL,NULL,
   '{"modulos":["clientes","ventas_stock"],"permisos":["lectura","escritura"]}',
   '[]'),
  ('Operario Depósito','operario_deposito','operario@simas.local',NULL,NULL,
   '{"modulos":["articulos","ventas_stock"],"permisos":["lectura","movimientos"]}',
   '[]');

-- Ventas y Stock: una compra recibida, una venta completada, una devolución parcial, un ajuste de inventario

-- Compra (ingreso de stock)
INSERT INTO ventas_stock (
  fecha_hora, tipo_transaccion, estado_transaccion, usuario_id, cliente_id, modo_pago,
  items_json, movimientos_json, totales_json, comprobantes_json, subtotal, iva, descuento, total
) VALUES (
  NOW(), 'compra', 'recibida', 1, NULL, 'Transferencia',
  '[{"sku":"SKU-0001","nombre":"Cargador USB-C 20W","cantidad":50,"costo":3000.00},{"sku":"SKU-0002","nombre":"Auriculares Bluetooth","cantidad":20,"costo":15000.00}]',
  '[{"sku":"SKU-0001","tipo":"entrada","cantidad":50},{"sku":"SKU-0002","tipo":"entrada","cantidad":20}]',
  '{"moneda":"ARS"}', '{"factura":"FAC-A-00001"}', 180000.00, 37800.00, 0.00, 217800.00
);

-- Venta (egreso de stock)
INSERT INTO ventas_stock (
  fecha_hora, tipo_transaccion, estado_transaccion, usuario_id, cliente_id, modo_pago,
  items_json, movimientos_json, totales_json, comprobantes_json, subtotal, iva, descuento, total
) VALUES (
  NOW(), 'venta', 'completada', 2, 1, 'Efectivo',
  '[{"sku":"SKU-0001","nombre":"Cargador USB-C 20W","cantidad":2,"precio_unit":5999.00},{"sku":"SKU-0002","nombre":"Auriculares Bluetooth","cantidad":1,"precio_unit":34999.00}]',
  '[{"sku":"SKU-0001","tipo":"salida","cantidad":2},{"sku":"SKU-0002","tipo":"salida","cantidad":1}]',
  '{"moneda":"ARS"}', '{"ticket":"T-C-00001"}', 40997.00, 8610.37, 0.00, 49607.37
);

-- Devolución (retorno parcial de venta)
INSERT INTO ventas_stock (
  fecha_hora, tipo_transaccion, estado_transaccion, usuario_id, cliente_id, modo_pago,
  items_json, movimientos_json, totales_json, comprobantes_json, subtotal, iva, descuento, total
) VALUES (
  NOW(), 'venta', 'devolucion', 2, 1, 'Efectivo',
  '[{"sku":"SKU-0001","nombre":"Cargador USB-C 20W","cantidad":1,"precio_unit":5999.00}]',
  '[{"sku":"SKU-0001","tipo":"entrada","cantidad":1}]',
  '{"moneda":"ARS"}', '{"nota_credito":"NC-00001"}', -5999.00, -1259.79, 0.00, -7258.79
);

-- Ajuste (pérdida inventario)
INSERT INTO ventas_stock (
  fecha_hora, tipo_transaccion, estado_transaccion, usuario_id, cliente_id, modo_pago,
  items_json, movimientos_json, totales_json, comprobantes_json, subtotal, iva, descuento, total
) VALUES (
  NOW(), 'ajuste', 'completada', 3, NULL, NULL,
  '[{"sku":"SKU-0003","nombre":"Cable HDMI 2.1","cantidad":2,"motivo":"rotura"}]',
  '[{"sku":"SKU-0003","tipo":"salida","cantidad":2}]',
  NULL, NULL, NULL, NULL, NULL, NULL
);

-- Índices convenientes
CREATE INDEX idx_articulos_nombre ON articulos(nombre);
CREATE INDEX idx_clientes_nombre ON clientes(nombre, apellido);
CREATE INDEX idx_usuarios_categoria ON usuarios(categoria);

SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
SET SQL_MODE=@OLD_SQL_MODE;

