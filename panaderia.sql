-- ==========================
-- BASE DE DATOS PANADERÍA
-- ==========================

-- Eliminar base si existe para empezar limpio
DROP DATABASE IF EXISTS panaderia;
CREATE DATABASE panaderia;
USE panaderia;

-- ==========================
-- TABLA DE PRODUCTOS
-- ==========================
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    precio INT NOT NULL,
    UNIQUE (nombre)
);

-- ==========================
-- INSERTAR PRODUCTOS
-- ==========================
INSERT INTO productos (nombre, precio) VALUES
('Pan de queso', 2000),
('Pan aliñado', 2000),
('Pan cacho', 2000),
('Gaseosa CocaCola', 3000),
('Buñuelo', 700);

-- ==========================
-- TABLA DE PEDIDOS
-- ==========================
CREATE TABLE pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================
-- TABLA DE DETALLE DE PEDIDOS
-- ==========================
CREATE TABLE pedido_detalle (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- ==========================
-- CONSULTAS DE EJEMPLO
-- ==========================

-- Ver todos los productos
SELECT * FROM productos;

-- Ver detalle de un pedido específico
SELECT 
    p.nombre AS producto,
    d.cantidad,
    p.precio,
    (d.cantidad * p.precio) AS subtotal
FROM pedido_detalle d
JOIN productos p ON d.producto_id = p.id
WHERE d.pedido_id = 1;

-- Calcular total de un pedido específico
SELECT 
    SUM(d.cantidad * p.precio) AS total
FROM pedido_detalle d
JOIN productos p ON d.producto_id = p.id
WHERE d.pedido_id = 1;

-- Mostrar todas las tablas
SHOW TABLES;

-- Revisar estructura de pedido_detalle
DESCRIBE pedido_detalle;
