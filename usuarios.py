from flask import Flask, request
import sqlite3
import hashlib

app = Flask(__name__)

# Crear la base de datos y la tabla de usuarios
def crear_base_datos():
    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()


# Generar hash de la contraseña
def generar_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Agregar un usuario a la base de datos
def agregar_usuario(usuario, password):
    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()

    password_hash = generar_hash(password)

    try:
        cursor.execute(
            "INSERT INTO usuarios (usuario, password_hash) VALUES (?, ?)",
            (usuario, password_hash)
        )
        conexion.commit()
        print(f"Usuario {usuario} creado correctamente.")
    except sqlite3.IntegrityError:
        print(f"El usuario {usuario} ya existe.")

    conexion.close()


# Validar usuario y contraseña
def validar_usuario(usuario, password):
    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()

    password_hash = generar_hash(password)

    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario = ? AND password_hash = ?",
        (usuario, password_hash)
    )

    resultado = cursor.fetchone()
    conexion.close()

    if resultado:
        return True
    return False


@app.route("/", methods=["GET", "POST"])
def inicio():
    mensaje = ""

    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]

        if validar_usuario(usuario, password):
            mensaje = "Usuario y contraseña correctos."
        else:
            mensaje = "Usuario o contraseña incorrectos."

    return f"""
    <html>
        <head>
            <title>Validación de Usuarios</title>
        </head>
        <body>
            <h1>Validación de Usuarios</h1>

            <form method="POST">
                <label>Usuario:</label>
                <input type="text" name="usuario" required><br><br>

                <label>Contraseña:</label>
                <input type="password" name="password" required><br><br>

                <input type="submit" value="Validar">
            </form>

            <h3>{mensaje}</h3>
        </body>
    </html>
    """


if __name__ == "__main__":
    crear_base_datos()

    # Crear los usuarios solicitados
    agregar_usuario("Luis Palacios", "Luis123")
    agregar_usuario("admin", "Admin123")

    app.run(host="0.0.0.0", port=5800)
