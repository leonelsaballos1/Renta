from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'appsecretkey'

# ---------------------- CONFIGURACIÓN MYSQL ----------------------
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ventas1'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# ---------------------- RUTAS PRINCIPALES ----------------------
@app.route('/')
def index():
    return render_template('index.html')

# LOGIN
@app.route('/accesologin', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuario WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['logueado'] = True
            session['id'] = user['id']
            session['id_rol'] = user['id_rol']
            if user['id_rol'] == 1:
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('usuario'))
        else:
            flash("Usuario o contraseña incorrectos", "error")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/registro')
def registro():
    return render_template('registro.html')

# PÁGINAS DE INFORMACIÓN
@app.route("/acercade")
def acercade():
    return render_template("acercade.html")

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/usuario')
def usuario():
    return render_template('usuario.html')

# ---------------------- USUARIOS ----------------------
@app.route('/listar')
def listar():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuario")
    usuarios = cur.fetchall()
    cur.close()
    return render_template("listar.html", usuarios=usuarios)

@app.route('/crearusuario', methods=['POST'])
def crearusuario():
    nombre = request.form['nombre']
    email = request.form['email']
    password = request.form['password']
    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO usuario (nombre, email, password, id_rol) VALUES (%s, %s, %s, '2')",
        (nombre, email, password)
    )
    mysql.connection.commit()
    cursor.close()
    flash("Usuario agregado correctamente", "success")
    return redirect(url_for('listar'))

@app.route('/updateUsuario', methods=['POST'])
def updateUsuario():
    id = request.form['id']
    nombre = request.form['nombre']
    email = request.form['email']
    password = request.form['password']
    cursor = mysql.connection.cursor()
    cursor.execute(
        "UPDATE usuario SET nombre=%s, email=%s, password=%s WHERE id=%s",
        (nombre, email, password, id)
    )
    mysql.connection.commit()
    cursor.close()
    flash("Usuario actualizado correctamente", "success")
    return redirect(url_for('listar'))

@app.route('/borrarUser/<int:id>')
def borrarUser(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM usuario WHERE id=%s", (id,))
    mysql.connection.commit()
    cursor.close()
    flash("Usuario eliminado correctamente", "success")
    return redirect(url_for('listar'))

# ---------------------- PRODUCTOS ----------------------

# ✅ Página con formulario + tabla (agrega productos)
@app.route('/listar_productos_agregados')
def listar_productos_agregados():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM carros")
    productos = cur.fetchall()
    cur.close()
    return render_template('listar_productos_agregados.html', productos=productos)

# ✅ Página con tabla + editar/eliminar (sin formulario)
@app.route('/listar_productos')
def listar_productos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM carros")
    productos = cur.fetchall()
    cur.close()
    return render_template('listar_productos.html', productos=productos)

# Agregar producto
@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    nombre = request.form['nombre']
    precio = request.form['precio']
    descripcion = request.form['descripcion']
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO carros (nombre, precio, descripcion) VALUES (%s, %s, %s)",
        (nombre, precio, descripcion)
    )
    mysql.connection.commit()
    cur.close()
    flash("carros agregado correctamente", "success")
    return redirect(url_for('listar_productos_agregados'))

# Editar producto
@app.route('/editar_producto', methods=['POST'])
def editar_producto():
    id = request.form['id']
    nombre = request.form['nombre']
    precio = request.form['precio']
    descripcion = request.form['descripcion']
    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE carros SET nombre=%s, precio=%s, descripcion=%s WHERE id=%s",
        (nombre, precio, descripcion, id)
    )
    mysql.connection.commit()
    cur.close()
    flash("Producto actualizado correctamente", "success")
    return redirect(url_for('listar_productos'))

# Eliminar producto
@app.route('/borrar_producto/<int:id>')
def borrar_producto(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM carros WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    flash("carros eliminado correctamente", "success")
    return redirect(url_for('listar_productos'))

# ------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True, port=8000)
