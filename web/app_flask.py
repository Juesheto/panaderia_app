from flask import Flask, render_template, request, jsonify
from db.conexion import get_conexion
from db.pedidos import crear_pedido

app = Flask(__name__)

@app.route("/")
def menu():
    conexion = get_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT id, nombre, precio FROM productos")
    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template("menu.html", productos=productos)

@app.route("/pedido", methods=["POST"])
def recibir_pedido():
    data = request.json
    pedido_id = crear_pedido(data)
    return jsonify({"pedido_id": pedido_id})

if __name__ == "__main__":
    app.run(debug=True)
