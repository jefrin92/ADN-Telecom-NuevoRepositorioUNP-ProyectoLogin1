from flask import Flask
from flask import render_template, redirect, request,Response,session
from flask_mysqldb import MySQL,MySQLdb
from werkzeug.security import generate_password_hash
import json

app= Flask(__name__,template_folder='templates')

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='adn_telecom'
app.config['MYSQL_CURSORCLASS']='DictCursor'

mysql=MySQL(app)



def transform_data(recomend):
    for item in recomend:
        for key, value in item.items():
            if isinstance(value, float) and value.is_integer():
                item[key] = int(value)
    return recomend

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/usuario')
def usuario():
    return render_template('usuario.html')

@app.route('/componentes')
def componentes():
    return render_template('/usuario/componentes.html')

@app.route('/estadisticas')
def estadisticas():
    return render_template('/usuario/estadisticas.html')

@app.route('/recomendaciones')
def recomendaciones():
    with open('recomendaciones.json', 'r') as file:
            recomend_json = file.read()

# Convertir la cadena JSON a una lista de Python
    recomend = json.loads(recomend_json)
    
    recomend = transform_data(recomend)
    
    return render_template('/usuario/recomendaciones.html',recomend=recomend)

@app.route('/resultados')
def resultados():

    with open('recomendaciones.json', 'r') as file:
            recomend_json = file.read()

# Convertir la cadena JSON a una lista de Python
    recomend2 = json.loads(recomend_json)
    
    recomend2 = transform_data(recomend2)
    
    return render_template('/usuario/resultados.html',recomend2=recomend2)

#funcion de acceso-login

@app.route('/acceso-login',methods=['GET','POST'])
def adn_telecom():
    
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword':
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']
       
        cur=mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo = %s AND password = %s',(_correo,_password))
        account = cur.fetchone()
       
        if account:
           session['logueado']=True
           session['id']=account['id']
           session['id_rol']=account['id_rol']	
           
           if session['id_rol']==1:
               return render_template('admin.html')	
           elif session['id_rol']==2:
               return render_template('usuario.html')
          
        else:    
            return render_template('index.html', mensaje='Usuario o contraseña incorrecta')

#-------------REGISTRAR USUARIOS-------------------
@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/crear-registro',methods=['GET','POST'])
def crear_registro():
    
    nombre=request.form['txtNombre']
    correo=request.form['txtCorreo']
    password=request.form['txtPassword']
    
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO usuarios(nombre, correo, password, id_rol) VALUES(%s,%s,%s,2)',(nombre,correo,password))
    mysql.connection.commit()
    
    return render_template('index.html',mensaje2='Registro exitoso')


#--------------------------------

#-------------LISTAR USUARIOS-------------------

@app.route('/listar',methods=['GET','POST'])
def listar():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios WHERE id_rol != 1')
    usuarios=cur.fetchall()
    cur.close()
    
    return render_template('listar_usuarios.html',usuarios=usuarios)
#--------------------------------

#-------------ELIMINAR USUARIOS-------------------

@app.route('/eliminar/<string:id>')
def eliminar(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM usuarios WHERE id = {0}'.format(id))
    mysql.connection.commit()
    
    return redirect('/listar')

@app.route('/actualizar/<int:id>', methods=['POST'])  # Asegúrate de que solo acepte POST
def actualizar(id):
    # Verificar que la petición es POST se maneja con el decorador, por lo que no es necesario aquí
    nombre = request.form['txtNombre']
    correo = request.form['txtCorreo']
    password = request.form['txtPassword']

    cur = mysql.connection.cursor()
    try:
        cur.execute('UPDATE usuarios SET nombre = %s, correo = %s, password = %s WHERE id = %s', (nombre, correo, password, id))
        mysql.connection.commit()
    finally:
        cur.close()  # Asegurarse de cerrar el cursor incluso si hay una excepción

    return redirect('/listar')




#--------------------------------

#-------------MODIFICAR USUARIOS-------------------

@app.route('/modificar/<id>', methods=['GET', 'POST'])
def modificar(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios WHERE id = %s',(id,))
    usuarios = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        nombre = request.form['txtNombre']
        correo = request.form['txtCorreo']
        password = request.form['txtPassword']
        
        cur = mysql.connection.cursor()
        cur.execute('UPDATE usuarios SET nombre=%s, correo=%s, password=%s WHERE id=%s', (nombre, correo, password, int(id)))
        mysql.connection.commit()
        cur.close()
        return redirect('/listar')
    
    return render_template('editar_usuarios.html', usuarios=usuarios)

@app.route('/estructura', methods=['GET', 'POST'])
def listar_estructura():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM estructura WHERE id = %s',(id,))
    estructura = cur.fetchall()
    cur.close()
    if request.method == 'POST':
        equipo = request.form['txtEquipo']
        modelo = request.form['txtModelo']
        marca = request.form['txtMarca']
        caracteristica = request.form['txtCaracteristica']
        costo = request.form['txtCosto']
        
        cur = mysql.connection.cursor()
        cur.execute('UPDATE usuarios SET equipo=%s, modelo=%s, marca=%s, caracteristica=%s, costo=%s password=%s WHERE id=%s', (equipo, modelo, marca, caracteristica, costo, int(id)))
        mysql.connection.commit()
        cur.close()
        return redirect('/listar')
    
    return render_template('estructura.html', estructura=estructura)
    
    

    
#--------------------------------

#-------------JSON-------------------

#--------------------------------

#para iniciar 
if __name__ == '__main__':
    app.secret_key="frank"
    app.run(debug=True,host='0.0.0.0', port=5000,threaded=True)