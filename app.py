from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from passlib.hash import pbkdf2_sha256  # ✅ para encriptar contraseñas

app = Flask(__name__)
app.secret_key = 'appsecretkey'

# ---------------------- CONFIGURACIÓN MYSQL ----------------------
app.config['MYSQL_HOST'] = 'b9vpb7eqvdb6e3ndo4hg-mysql.services.clever-cloud.com'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'ufycbz1ourtwdn5v'
app.config['MYSQL_PASSWORD'] = '8E1eCI80ZwvWM3at98YY'
app.config['MYSQL_DB'] = 'b9vpb7eqvdb6e3ndo4hg'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# ---------------------- RUTAS PRINCIPALES ----------------------
@app.route('/')
def index():
    return render_template('index.html')

# ---------------------- LOGIN ----------------------
@app.route('/accesologin', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password_ingresada = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuario WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and pbkdf2_sha256.verify(password_ingresada, user['password']):
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

# ---------------------- REGISTRO ----------------------
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = pbkdf2_sha256.hash(request.form['password'])  # 🔒 Encripta

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuario WHERE email=%s", (email,))
        existe = cursor.fetchone()

        if existe:
            flash("Este correo ya está registrado.", "warning")
            return redirect(url_for('registro'))

        cursor.execute(
            "INSERT INTO usuario (nombre, email, password, id_rol) VALUES (%s, %s, %s, '2')",
            (fullname, email, password)
        )
        mysql.connection.commit()
        cursor.close()
        flash("Registro exitoso, ahora puede iniciar sesión.", "success")
        return redirect(url_for('login'))

    return render_template('registro.html')

# ---------------------- PÁGINAS DE INFORMACIÓN ----------------------
@app.route("/acercade")
def acercade():
    return render_template("acercade.html")

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

# ---------------------- PANEL ADMIN ----------------------
@app.route('/admin')
def admin():
    cur = mysql.connection.cursor()

    # Contar usuarios y vehículos
    cur.execute("SELECT COUNT(*) AS total_usuarios FROM usuario")
    total_usuarios = cur.fetchone()['total_usuarios']

    cur.execute("SELECT COUNT(*) AS total_vehiculos FROM carros")
    total_vehiculos = cur.fetchone()['total_vehiculos']

    cur.close()

    return render_template('admin.html',
                           total_usuarios=total_usuarios,
                           total_vehiculos=total_vehiculos)

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
    password = pbkdf2_sha256.hash(request.form['password'])  # 🔒 encripta
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

    if password:
        hashed_password = pbkdf2_sha256.hash(password)
        cursor.execute(
            "UPDATE usuario SET nombre=%s, email=%s, password=%s WHERE id=%s",
            (nombre, email, hashed_password, id)
        )
    else:
        cursor.execute(
            "UPDATE usuario SET nombre=%s, email=%s WHERE id=%s",
            (nombre, email, id)
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
@app.route('/listar_productos_agregados')
def listar_productos_agregados():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM carros")
    productos = cur.fetchall()
    cur.close()
    return render_template('listar_productos_agregados.html', productos=productos)

@app.route('/listar_productos')
def listar_productos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM carros")
    productos = cur.fetchall()
    cur.close()
    return render_template('listar_productos.html', productos=productos)

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    nombre = request.form['nombre']
    precio = request.form['precio']
    descripcion = request.form['descripcion']
    fecha = request.form['fecha']
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO carros (nombre, precio, descripcion, fecha) VALUES (%s, %s, %s, %s)",
        (nombre, precio, descripcion, fecha)
    )
    mysql.connection.commit()
    cur.close()
    flash("Carro agregado correctamente", "success")
    return redirect(url_for('listar_productos_agregados'))

@app.route('/editar_producto', methods=['POST'])
def editar_producto():
    id = request.form['id']
    nombre = request.form['nombre']
    precio = request.form['precio']
    descripcion = request.form['descripcion']
    fecha = request.form['fecha']
    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE carros SET nombre=%s, precio=%s, descripcion=%s, fecha=%s WHERE id=%s",
        (nombre, precio, descripcion, fecha, id)
    )
    mysql.connection.commit()
    cur.close()
    flash("Producto actualizado correctamente", "success")
    return redirect(url_for('listar_productos'))

@app.route('/borrar_producto/<int:id>')
def borrar_producto(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM carros WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    flash("Carro eliminado correctamente", "success")
    return redirect(url_for('listar_productos'))



# ---------------------- MAIN ----------------------
if __name__ == '__main__':
    app.run(debug=True, port=8000)
