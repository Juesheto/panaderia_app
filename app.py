from db.pedidos import crear_pedido, historial_dia, total_dia
from db.conexion import get_conexion
from datetime import datetime

# ==========================
# Cargar productos desde DB
# ==========================
def cargar_productos():
    try:
        conexion = get_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT id, nombre, precio FROM productos ORDER BY id")
        productos = cursor.fetchall()

        cursor.close()
        conexion.close()

        return {
            p['id']: {
                "nombre": p['nombre'],
                "precio": p['precio']
            } for p in productos
        }

    except Exception as e:
        print(f"⚠ Error al cargar productos: {e}")
        return {}

# ==========================
# Mostrar menú en consola
# ==========================
def mostrar_menu(productos):
    if not productos:
        print("⚠ No hay productos disponibles.")
        return

    print("\n========= MENÚ =========\n")
    for pid, p in productos.items():
        print(f"{pid}. {p['nombre']} - ${p['precio']:.2f}")

# ==========================
# Crear pedido desde consola
# ==========================
def crear_pedido_usuario(productos):
    pedido = {}

    while True:
        try:
            opcion = int(input("\nIngrese número del producto (0 para terminar): "))
        except ValueError:
            print("⚠ Ingrese un número válido.")
            continue

        if opcion == 0:
            break

        if opcion not in productos:
            print("⚠ Producto no válido.")
            continue

        try:
            cantidad = int(input("Cantidad: "))
        except ValueError:
            print("⚠ Ingrese una cantidad válida.")
            continue

        if cantidad <= 0:
            print("⚠ La cantidad debe ser mayor a 0.")
            continue

        pedido[opcion] = pedido.get(opcion, 0) + cantidad

    return pedido

# ==========================
# Mostrar historial
# ==========================
def mostrar_historial():
    pedidos = historial_dia()

    if not pedidos:
        print("\n⚠ No hay pedidos hoy.")
        return

    print("\n========= HISTORIAL DEL DÍA =========\n")

    ultimo_id = None
    for item in pedidos:
        if item['pedido_id'] != ultimo_id:
            print(f"\nPedido #{item['pedido_id']} - {item['fecha']}")
            print("{:<3} {:<20} {:<8} {:<10}".format(
                "Cant", "Producto", "Precio", "Subtotal"
            ))
            ultimo_id = item['pedido_id']

        print("{:<3} {:<20} ${:<8.2f} ${:<10.2f}".format(
            item['cantidad'],
            item['producto'],
            item['precio'],
            item['subtotal']
        ))

# ==========================
# Mostrar total del día
# ==========================
def mostrar_total():
    total = total_dia()
    print("\n----------------------------------")
    print(f"TOTAL VENDIDO HOY: ${total:.2f}")
    print("----------------------------------")

# ==========================
# LOOP PRINCIPAL
# ==========================
def main():
    productos = cargar_productos()

    if not productos:
        print("⚠ No hay productos cargados. Verifica la base de datos.")
        return

    while True:
        mostrar_menu(productos)

        pedido_usuario = crear_pedido_usuario(productos)

        if not pedido_usuario:
            print("⚠ No se realizó ningún pedido.")
            continue

        try:
            pedido_id = crear_pedido(pedido_usuario)
            print(f"\n✅ Pedido #{pedido_id} registrado con éxito!")
        except Exception as e:
            print(f"⚠ Error al registrar el pedido: {e}")
            continue

        mostrar_historial()
        mostrar_total()

        otra = input("\n¿Atender otro cliente? (s/n): ").lower()
        if otra != "s":
            break

    print("\n🛑 Caja cerrada.")

if __name__ == "__main__":
    main()
