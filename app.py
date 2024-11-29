from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
import pymysql.cursors

app = Flask(__name__)



def connect_to_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='Repositorio_CBC',
        cursorclass=pymysql.cursors.DictCursor,
        ssl_disabled=True
    )

@app.route('/')
def index():       
 return render_template('index.html')


@app.route('/agregar',methods=["GET","POST"])
def ingreso():
    if request.method=="POST":
        Nombre_Rol=request.form["Nombre_Rol"]
        Codigo_Rol=request.form["Codigo_Rol"]
        
        try:
            conn = connect_to_db()
            cur = conn.cursor() 
            cur.execute("INSERT INTO rol (Nombre_Rol, Codigo_Rol) VALUES (%s, %s)",
                        (Nombre_Rol, Codigo_Rol))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('consulta'))
        except Exception:
            return redirect(url_for('index'))
    return render_template('form.html')


@app.route('/consulta')
def consulta():
    try:
        conn = connect_to_db()
        cur = conn.cursor() 
        cur.execute("SELECT * FROM rol")
        data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('consulta.html', roles=data)
    except Exception:
        return render_template('consulta.html', roles=[]) 
    
    
# Ruta para agregar un nuevo usuario
@app.route('/add_Proyecto', methods=['GET', 'POST'])
def add_Proyecto():
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        # Consultamos todas las identificaciones y nombres de los roles para mostrarlos en el formulario
        cur.execute("SELECT ID_Rol,Nombre_Rol, Codigo_Rol FROM rol")
        roless = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        app.logger.error(f"Error al insertar usuario: {e}")
        flash(f"Ocurrió un error: {e}")
        return redirect(url_for('index'))


    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Correo = request.form['Correo']
        Contrasena=request.form['Contrasena']
        Fecha_Registro = request.form['Fecha_Registro']
        
        try:
            conn = connect_to_db()
            cur = conn.cursor()
            # Insertamos los datos en la tabla `usuario`
            cur.execute("INSERT INTO usuario (Nombre, Correo, Contrasena, Fecha_Registro) VALUES ( %s, %s, %s, %s)",
                        (Nombre, Correo, Contrasena, Fecha_Registro))
            conn.commit()
            cur.close()
            conn.close()
            
            return redirect(url_for('consulto2'))
        except Exception as e:
            
            return redirect(url_for('consulto2'))
    return render_template('formusuar.html', roless=roless)


@app.route('/consulto2')
def consulto2():
    try:
        conn = connect_to_db()
        cur = conn.cursor() 
        cur.execute("SELECT * FROM usuario")
        data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('consulto2.html', roless=data)
    except Exception:
        return render_template('consulto2.html', roless=[]) 


    
    # Ruta para eliminar un rol
@app.route('/delete/<string:ID_Rol>', methods=['POST'])
def delete_rol(ID_Rol):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM rol WHERE ID_Rol=%s", (ID_Rol,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('consulta'))
    except Exception as e:
        return redirect(url_for('index'))






    # Ruta para editar un rol existente
@app.route('/edit/<ID_Rol>', methods=['GET', 'POST'])
def edit_rol(ID_Rol):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM rol WHERE ID_Rol=%s", (ID_Rol,))
        rol = cur.fetchone()
        cur.close()
        conn.close()

    except Exception as e:

        return redirect(url_for('index'))
    if request.method == 'POST':
        Nombre_Rol = request.form['Nombre_Rol']
        Codigo_Rol = request.form['Codigo_Rol']
    
        try:
            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute("""UPDATE rol SET  Nombre_Rol=%s, Codigo_Rol=%s WHERE ID_Rol=%s""", 
                ( Nombre_Rol, Codigo_Rol, ID_Rol))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('consulta'))
        except Exception as e:
                return redirect(url_for('index'))
    return render_template('editar.html', rol=rol)


   # Ruta para eliminar un usuario
@app.route('/delete/<string:ID_Usuario>', methods=['POST'])
def delete_usuario(ID_Usuario):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM usuario WHERE ID_Usuario=%s", (ID_Usuario,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('consulto2'))
    except Exception as e:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)


