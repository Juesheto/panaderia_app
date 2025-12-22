import mysql.connector

def get_conexion():
    """
    Devuelve la conexión y cursor de MySQL.
    """
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="juesheto",
        database="panaderia"
    )
    cursor = conexion.cursor(dictionary=True)  # Devuelve resultados como diccionario
    return conexion, cursor
