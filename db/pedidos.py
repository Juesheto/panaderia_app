from db.conexion import get_conexion
from datetime import datetime

# ==========================
# Crear un pedido
# ==========================
def crear_pedido(pedido_dict):
    """
    pedido_dict: {producto_id: cantidad, ...}
    Retorna: id del pedido creado
    """
    conexion, cursor = get_conexion()

    # Insertar pedido
    cursor.execute("INSERT INTO pedidos (fecha) VALUES (%s)", (datetime.now(),))
    conexion.commit()
    pedido_id = cursor.lastrowid

    # Insertar detalles
    for producto_id, cantidad in pedido_dict.items():
        cursor.execute(
            "INSERT INTO pedido_detalle (pedido_id, producto_id, cantidad) VALUES (%s, %s, %s)",
            (pedido_id, producto_id, cantidad)
        )
    conexion.commit()
    conexion.close()
    return pedido_id

# ==========================
# Historial de pedidos del día
# ==========================
def historial_dia(fecha=None):
    """
    Devuelve todos los pedidos y detalles de un día.
    fecha: str "YYYY-MM-DD" o None para hoy
    """
    if fecha is None:
        fecha = datetime.now().strftime("%Y-%m-%d")

    conexion, cursor = get_conexion()
    cursor.execute("""
        SELECT ped.id AS pedido_id, ped.fecha,
               p.nombre AS producto, d.cantidad, p.precio,
               (d.cantidad * p.precio) AS subtotal
        FROM pedidos ped
        JOIN pedido_detalle d ON ped.id = d.pedido_id
        JOIN productos p ON d.producto_id = p.id
        WHERE DATE(ped.fecha) = %s
        ORDER BY ped.id, p.id
    """, (fecha,))
    resultados = cursor.fetchall()
    conexion.close()
    return resultados

# ==========================
# Total vendido del día
# ==========================
def total_dia(fecha=None):
    """
    Retorna la suma de todos los pedidos de un día.
    """
    if fecha is None:
        fecha = datetime.now().strftime("%Y-%m-%d")

    conexion, cursor = get_conexion()
    cursor.execute("""
        SELECT SUM(d.cantidad * p.precio) AS total
        FROM pedidos ped
        JOIN pedido_detalle d ON ped.id = d.pedido_id
        JOIN productos p ON d.producto_id = p.id
        WHERE DATE(ped.fecha) = %s
    """, (fecha,))
    total = cursor.fetchone()['total'] or 0
    conexion.close()
    return total
