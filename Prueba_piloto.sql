-- Test queries for SIMAS TPI 2025 - 4-table simplified schema
USE simas_tpi;

-- 1) Listar artículos con detalles de clasificación y costos desde JSON
SELECT id, sku, nombre, marca, categoria, proveedor,
       precio_venta, stock_disponible,
       JSON_EXTRACT(costos_json, '$.costo_compra') AS costo_compra,
       JSON_EXTRACT(costos_json, '$.costo_reorden') AS costo_reorden,
       JSON_EXTRACT(costos_json, '$.costo_mantenimiento') AS costo_mantenimiento
FROM articulos
ORDER BY id;

-- 2) Reconstruir stock teórico por SKU combinando stock_disponible inicial + movimientos
-- (suponiendo stock_disponible ya refleja estado actual, aquí solo calculamos desde movimientos como validación)
SELECT a.sku,
       a.stock_disponible AS snapshot,
       COALESCE(m.mov,0) AS desde_movimientos,
       (a.stock_disponible - COALESCE(m.mov,0)) AS diferencia
FROM articulos a
LEFT JOIN (
  SELECT JSON_UNQUOTE(JSON_EXTRACT(m.value, '$.sku')) AS sku,
         SUM(CASE JSON_UNQUOTE(JSON_EXTRACT(m.value, '$.tipo')) WHEN 'entrada' THEN JSON_EXTRACT(m.value, '$.cantidad') WHEN 'salida' THEN -JSON_EXTRACT(m.value, '$.cantidad') ELSE 0 END) AS mov
  FROM ventas_stock vs
  JOIN JSON_TABLE(vs.movimientos_json, '$[*]' COLUMNS(value JSON PATH '$')) AS m
  GROUP BY sku
) m ON m.sku = a.sku
ORDER BY a.sku;


-- 3) Clientes con dirección y tipo de cliente desde JSON
SELECT id, nombre, apellido,
       JSON_UNQUOTE(JSON_EXTRACT(direccion_json, '$.ciudad')) AS ciudad,
       JSON_UNQUOTE(JSON_EXTRACT(direccion_json, '$.cp')) AS cp,
       JSON_UNQUOTE(JSON_EXTRACT(datos_fiscales_json, '$.tipo_cliente')) AS tipo_cliente
FROM clientes
ORDER BY id;

-- 4) Usuarios y permisos declarados en JSON
SELECT id, nombre, categoria,
       JSON_LENGTH(JSON_EXTRACT(permisos_json, '$.modulos')) AS modulos_habilitados,
       JSON_EXTRACT(permisos_json, '$.permisos') AS permisos
FROM usuarios;

-- 5) Bitácora de acciones de usuarios (acciones_json)
SELECT u.id AS usuario_id, u.nombre,
       JSON_UNQUOTE(JSON_EXTRACT(act.value, '$.accion')) AS accion,
       JSON_UNQUOTE(JSON_EXTRACT(act.value, '$.ts')) AS timestamp
FROM usuarios u
JOIN JSON_TABLE(u.acciones_json, '$[*]' COLUMNS(value JSON PATH '$')) AS act;


-- 6) Ventas: expandir items_json como filas (MariaDB 10.5+: JSON_TABLE no nativo; usar workaround)
-- Ejemplo: listar cada item vendido con su cantidad y precio
SELECT vs.id AS transaccion_id,
       JSON_UNQUOTE(JSON_EXTRACT(j.value, '$.sku')) AS sku,
       JSON_UNQUOTE(JSON_EXTRACT(j.value, '$.nombre')) AS nombre,
       JSON_EXTRACT(j.value, '$.cantidad') AS cantidad,
       JSON_EXTRACT(j.value, '$.precio_unit') AS precio_unit
FROM ventas_stock vs
JOIN JSON_TABLE(vs.items_json, '$[*]' COLUMNS(value JSON PATH '$')) AS j
WHERE vs.tipo_transaccion='venta';

-- 7) Stock neto por SKU calculado desde ventas_stock.movimientos_json
SELECT JSON_UNQUOTE(JSON_EXTRACT(m.value, '$.sku')) AS sku,
       SUM(CASE JSON_UNQUOTE(JSON_EXTRACT(m.value, '$.tipo'))
             WHEN 'entrada' THEN JSON_EXTRACT(m.value, '$.cantidad')
             WHEN 'salida' THEN -JSON_EXTRACT(m.value, '$.cantidad')
             ELSE 0 END) AS stock_neto
FROM ventas_stock vs
JOIN JSON_TABLE(vs.movimientos_json, '$[*]' COLUMNS(value JSON PATH '$')) AS m
GROUP BY 1
ORDER BY 1;

-- 8) Top productos por ingresos (ventas) por total calculado
SELECT JSON_UNQUOTE(JSON_EXTRACT(i.value, '$.sku')) AS sku,
       SUM(JSON_EXTRACT(i.value, '$.cantidad') * JSON_EXTRACT(i.value, '$.precio_unit')) AS importe
FROM ventas_stock vs
JOIN JSON_TABLE(vs.items_json, '$[*]' COLUMNS(value JSON PATH '$')) AS i
WHERE vs.tipo_transaccion='venta'
GROUP BY 1
ORDER BY importe DESC;

-- 9) Ventas por cliente con totales denormalizados
SELECT vs.id, vs.fecha_hora, vs.cliente_id, vs.total
FROM ventas_stock vs
WHERE vs.tipo_transaccion='venta' AND vs.estado_transaccion IN ('completada','devolucion')
ORDER BY vs.fecha_hora DESC;

-- 10) KPIs diarios: ventas, devoluciones y neto del día
SELECT DATE(vs.fecha_hora) AS fecha,
       SUM(CASE WHEN vs.tipo_transaccion='venta' AND vs.estado_transaccion='completada' THEN COALESCE(vs.total,0) ELSE 0 END) AS ventas_totales,
       SUM(CASE WHEN vs.tipo_transaccion='venta' AND vs.estado_transaccion='devolucion' THEN COALESCE(vs.total,0) ELSE 0 END) AS devoluciones_totales,
       SUM(CASE WHEN vs.tipo_transaccion='venta' THEN COALESCE(vs.total,0) ELSE 0 END) AS neto
FROM ventas_stock vs
GROUP BY DATE(vs.fecha_hora)
ORDER BY fecha DESC;

-- 11) Segmentación de clientes por tipo
SELECT JSON_UNQUOTE(JSON_EXTRACT(datos_fiscales_json, '$.tipo_cliente')) AS tipo_cliente,
       COUNT(*) AS cantidad
FROM clientes
GROUP BY tipo_cliente;