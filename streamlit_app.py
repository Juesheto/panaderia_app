import streamlit as st
from db.pedidos import crear_pedido
from db.conexion import get_conexion
from datetime import datetime

# ==========================
# Detectar modo desde URL
# ==========================
query_params = st.query_params
modo = query_params.get("modo", ["Caja"])[0]  # default Caja

# ==========================
# Cargar productos desde DB
# ==========================
def cargar_productos():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()

        cursor.close()
        conn.close()

        return productos

    except Exception as e:
        print(f"⚠ Error al cargar productos: {e}")
        return []


productos = cargar_productos()

# ==========================
# Variables de sesión
# ==========================
if "pedido" not in st.session_state:
    st.session_state.pedido = {}

# ==========================
# Modo Cliente
# ==========================
if modo.lower() == "cliente":
    st.title("🛒 Menú Cliente")
    
    if not productos:
        st.warning("⚠ No hay productos disponibles.")
    else:
        for pid, p in productos.items():
            if st.button(f"{p['nombre']} - ${p['precio']:.2f}", key=pid):
                if pid in st.session_state.pedido:
                    st.session_state.pedido[pid] += 1
                else:
                    st.session_state.pedido[pid] = 1
        
        st.subheader("Tu pedido")
        total = 0
        if st.session_state.pedido:
            for pid, cantidad in st.session_state.pedido.items():
                nombre = productos[pid]['nombre']
                precio = productos[pid]['precio']
                subtotal = precio * cantidad
                total += subtotal
                st.write(f"{cantidad} x {nombre} = ${subtotal:.2f}")
            st.write(f"**Total:** ${total:.2f}")
        else:
            st.write("No has agregado productos aún.")

        if st.button("Enviar pedido"):
            if st.session_state.pedido:
                try:
                    pedido_id = crear_pedido(st.session_state.pedido)
                    st.success(f"✅ Pedido #{pedido_id} enviado con éxito!")
                    st.session_state.pedido = {}
                except Exception as e:
                    st.error(f"⚠ Error al enviar el pedido: {e}")
            else:
                st.warning("⚠ Tu pedido está vacío.")

# ==========================
# Modo Caja
# ==========================
else:
    st.title("🛒 Modo Caja")
    st.subheader("Historial de pedidos del día")

    try:
        conexion = get_conexion()
        cursor = conexion.cursor(dictionary=True)

        hoy = datetime.now().date()
        cursor.execute("""
            SELECT p.id as pedido_id, p.fecha, d.producto_id, d.cantidad, pr.nombre, pr.precio
            FROM pedidos p
            JOIN pedido_detalle d ON p.id = d.pedido_id
            JOIN productos pr ON d.producto_id = pr.id
            WHERE DATE(p.fecha) = %s
            ORDER BY p.id, d.id
        """, (hoy,))
        pedidos = cursor.fetchall()
        conexion.close()

        if pedidos:
            historial = {}
            total_vendido = 0
            for item in pedidos:
                pid = item['pedido_id']
                if pid not in historial:
                    historial[pid] = {
                        "fecha": item['fecha'],
                        "detalle": []
                    }
                subtotal = item['precio'] * item['cantidad']
                total_vendido += subtotal
                historial[pid]["detalle"].append({
                    "nombre": item['nombre'],
                    "cantidad": item['cantidad'],
                    "precio": item['precio'],
                    "subtotal": subtotal
                })
            
            for pid, data in historial.items():
                st.write(f"**Pedido #{pid} - {data['fecha']}**")
                for det in data['detalle']:
                    st.write(f"{det['cantidad']} x {det['nombre']} = ${det['subtotal']:.2f}")
                st.markdown("---")
            
            st.subheader(f"Total vendido hoy: ${total_vendido:.2f}")
        else:
            st.info("No hay pedidos registrados hoy.")

    except Exception as e:
        st.error(f"⚠ Error al obtener historial: {e}")
