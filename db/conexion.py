import mysql.connector
import os
from urllib.parse import urlparse

def get_conexion():
    db_url = os.getenv("RAILWAY_DB_URL")
    if not db_url:
        raise RuntimeError("No se encontró RAILWAY_DB_URL")

    url = urlparse(db_url)

    conexion = mysql.connector.connect(
        host=url.hostname,
        user=url.username,
        password=url.password,
        database=url.path.lstrip("/"),
        port=url.port
    )

    cursor = conexion.cursor(dictionary=True)
    return conexion, cursor
