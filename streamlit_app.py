import streamlit as st
from urllib.parse import urlparse, parse_qs
from db.pedidos import crear_pedido
from db.conexion import get_conexion

# ==========================
# Detectar modo desde URL
# ==========================
query_params = st.experimental_get_query_params()
modo = query_params.get("modo", ["Caja"])[0]  # default Caja

# ==========================
# Cargar productos
# ==========================
def cargar_productos():
    conexion, cursor = get_conexion()
    cursor.execute("SELECT id, nombre, precio FROM productos ORDER BY id")
    productos = cursor.fetchall()
    conexion.close()
    return {p['id']: {"nombre": p['nombre'], "precio": p['precio']} for p in productos}

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
    
    for pid, p in productos.items():
        if st.button(f"{p['nombre']} - ${p['precio']}", key=pid):
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
            st.write(f"{cantidad} x {nombre} = ${subtotal}")
        st.write(f"**Total:** ${total}")
    else:
        st.write("No has agregado productos aún.")

    if st.button("Enviar pedido"):
        if st.session_state.pedido:
            pedido_id = crear_pedido(st.session_state.pedido)
            st.success(f"✅ Pedido #{pedido_id} enviado con éxito!")
            st.session_state.pedido = {}
        else:
            st.warning("⚠ Tu pedido está vacío.")

# ==========================
# Modo Caja
# ==========================
else:
    st.title("🛒 Modo Caja")
    st.write("Aquí va todo tu código de caja: historial, total vendido, registro de pedidos…")
