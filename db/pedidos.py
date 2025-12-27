from db.conexion import get_conexion

def crear_pedido(pedido):
    conexion = get_conexion()
    cursor = conexion.cursor()

    # Crear pedido
    cursor.execute("INSERT INTO pedidos (fecha) VALUES (NOW())")
    pedido_id = cursor.lastrowid

    # Insertar detalle
    for producto_id, cantidad in pedido.items():
        cursor.execute("""
            INSERT INTO pedido_detalle (pedido_id, producto_id, cantidad)
            VALUES (%s, %s, %s)
        """, (pedido_id, producto_id, cantidad))

    conexion.commit()
    cursor.close()
    conexion.close()

    return pedido_id
