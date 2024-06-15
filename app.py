from flask import Flask, render_template,jsonify, redirect, request, session
from flask_mysqldb import MySQL, MySQLdb
import json
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__, template_folder='templates')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'adn_telecom'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

def transform_data(recomend):
    for item in recomend:
        for key, value in item.items():
            if isinstance(value, float) and value.is_integer():
                item[key] = int(value)
    return recomend

def get_components_from_db():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM componentes")
    rows = cur.fetchall()
    cur.close()
    df = pd.DataFrame(rows)
    print("Columnas del DataFrame de la base de datos:", df.columns)  # Añadir esto para depuración
    return df


def clean_categorical_data(df, columns):
    for column in columns:
        df[column] = df[column].astype(str).str.strip()
    return df

def add_image_field(components):
    image_urls = {
        1: "https://th.bing.com/th/id/OIP.Pz4mXqbEYL9zS-cYyZk80AHaE8?rs=1&pid=ImgDetMain",
        2: "http://www.qftth.net/uploads/202115580/small/zte-dual-band-onu-f670l30346472761.jpg",
        3: "https://th.bing.com/th/id/OIP.F0D7ICcmz6u0U4i2alqjzQHaHa?rs=1&pid=ImgDetMain",
        4: "https://th.bing.com/th/id/OIP.X7FYsfkFmdP5hsbqJIsRwQAAAA?rs=1&pid=ImgDetMain",
        5: "https://th.bing.com/th/id/OIP.SrMdiRtk-JGEq0ALDnxylwHaGU?rs=1&pid=ImgDetMain",
        6: "https://th.bing.com/th/id/OIP.9jqNniLD-c1cJT5D6O0gawHaHa?rs=1&pid=ImgDetMain",
        7: "https://th.bing.com/th/id/OIP.KTsT3tv5Sr2ldEywx11qzQHaHa?rs=1&pid=ImgDetMain",
        8: "https://th.bing.com/th/id/OIP.g-ai8Qmzfbz1gy30DqPftgHaHa?rs=1&pid=ImgDetMain",
        9: "https://th.bing.com/th/id/OIP.fkZq0sp71cxtuOfxz4rrsgHaHa?rs=1&pid=ImgDetMain",
        10: "https://th.bing.com/th/id/OIP.BwivpHBDhkgmKd4XQauJHQHaHa?rs=1&pid=ImgDetMain",
        11: "https://th.bing.com/th/id/R.55895c3a2777e5688e7bfb5898211b41?rik=t2tnnU%2fmy4Fn5g&riu=http%3a%2f%2fgponsolution.com%2fwp-content%2fuploads%2f2016%2f03%2fZTE-C320-GPON-OLT-Specification.jpg&ehk=a8JXRHAhajQlBCMNECp9Y%2fAM%2fPSX81bQQRKw6lkBbwY%3d&risl=&pid=ImgRaw&r=0",
        12: "https://www.henanliyuan.com/Uploads/5d9176ab20d872779.jpg",
        13: "https://http2.mlstatic.com/D_NQ_NP_2X_730541-MLB44905216280_022021-F.jpg",
        14: "https://cdn.myshoptet.com/usr/www.ponplanet.eu/user/shop/big/579_v1600gs-o32.jpg?65361b70",
        15: "https://th.bing.com/th/id/OIP.R4_bV-hPjneL98gl34on7wAAAA?rs=1&pid=ImgDetMain",
        16: "https://www.cyberteam.pl/_image/product/7746/7746_7746-fibertechnic-olt-gpon-fd1608s-b0-8xgpon-2x10gbit-4x1g-uplink-combo--2xac_03.jpg",
        17: "https://www.comx-computers.co.za/i/mikrotik/52907_IMG1.jpg",
        18: "https://www.wisp.pl/galerie/m/mikrotik-cloud-core-router-cc_12697.jpg",
        19: "https://m.media-amazon.com/images/I/71Qp4cPJNIL._AC_SL1500_.jpg",
        20: "https://th.bing.com/th/id/R.d235b555a51be21b18a891bdf5a596bc?rik=8oWkqeMTR8b1kw&riu=http%3a%2f%2f2.bp.blogspot.com%2f-FyvJAjN_eSE%2fVI6-poG_XQI%2fAAAAAAAABe0%2fugzRXU_rqtI%2fs1600%2frb951g-2hnd-2.jpg&ehk=3wsR2nuJbAPPFaFAQtqaVauA2EZB52uwLx4DeGVnbi8%3d&risl=&pid=ImgRaw&r=0",
        21: "https://i5.walmartimages.com/asr/c5ed70d8-aac4-4d60-8635-b631c8cf2a75.22c9c4934f589681eb65695ba5115cda.jpeg",
        22: "https://http2.mlstatic.com/D_NQ_NP_2X_875988-MLA40175220158_122019-F.jpg",
        23: "https://www.media-rdc.com/medias/7f8c8641686c3c249d8455738091d3b3/switch-ethernet-dlink-dgs-105-dlink.jpg?cimgnr=CbzVv",
        24: "https://www.startechstore.com/wp-content/uploads/2020/09/NETGEAR-GS108LP-100EUS-121.jpg",
        25: "https://th.bing.com/th/id/OIP.LUVQMn4D8uOxQJ7geOtK-QAAAA?rs=1&pid=ImgDetMain",
        26: "https://th.bing.com/th/id/OIP.2mpkDZy8Dz2oMe27PFzjoAHaHa?rs=1&pid=ImgDetMain",
        27: "https://th.bing.com/th/id/OIP.RUDBP-TbO7bUc1uNzelY4QHaHa?rs=1&pid=ImgDetMain"
        # Agrega más ID y URLs según sea necesario
    }
    for component in components:
        component_id = int(component["iD"])
        component["Imagen"] = image_urls.get(component_id, "https://example.com/default.jpg")  # Usa una imagen por defecto si no se encuentra el ID
    return components
def update_component_data(components, df):
    updated_components = []
    for component in components:
        print("Component:", component)  # Añadir esto para depuración
        if 'iD' in component:
            component_id = int(component['iD'])
            print("Buscando componente con iD:", component_id)  # Añadir esto para depuración

            # Utiliza el nombre de columna correcto del DataFrame
            db_row = df[df['ID'] == component_id]  # Asegúrate de usar 'ID' en lugar de 'iD' si ese es el nombre correcto
            
            if not db_row.empty:
                db_row = db_row.iloc[0]
                component['Equipo'] = db_row['EQUIPO']
                component['Modelo'] = db_row['MODELO']
                component['Marca'] = db_row['MARCA']
                component['Costo'] = f"${db_row['COSTO']:,.2f}"  # Formatear costo con símbolo de moneda
                component['approval_Index'] = round((db_row['approval_Index'] / 10) * 100, 2)  # Convert to percentage
                updated_components.append(component)
            else:
                print(f"No se encontró un componente con iD: {component_id}")  # Añadir esto para depuración
        else:
            print("Llave 'iD' no encontrada en componente:", component)  # Añadir esto para depuración
    
    return updated_components


def recommend(input_data, knn_model, data, num_recommendations=5):
    knn_model.set_params(n_neighbors=len(data))  # Considerar todos los vecinos para poder ordenar después
    distances, indices = knn_model.kneighbors([input_data])
    recommendations = data.iloc[indices[0]]
    # Ordenar las recomendaciones por el índice de aprobación en orden descendente
    recommendations = recommendations.sort_values(by='approval_Index', ascending=False)
    
    # Limitar la cantidad de recomendaciones
    return recommendations.head(num_recommendations)

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
    # Obtener los datos de la base de datos
    df = get_components_from_db()
    
    # Calcular porcentajes de aprobación
    df['approval_Index'] = df['approval_Index'].apply(lambda x: round((x / 10) * 100, 2))
    
    # Ordenar y seleccionar las 10 recomendaciones más cercanas al 100%
    top_recommendations = df.sort_values(by='approval_Index', ascending=False).head(10)
    
    # Calcular estadísticas, por ejemplo, contar la cantidad de cada tipo de equipo
    equipo_counts = df['EQUIPO'].value_counts().reset_index()
    equipo_counts.columns = ['Equipo', 'Cantidad']

    # Definir el número de recomendaciones
    num_recommendations = min(len(df), 10)  # Asegurar que no exceda el máximo de 10
    total_components = 27  # Total de componentes

    estadisticas_data = {
        "equipo_counts": equipo_counts.to_dict(orient='records'),
        "num_recommendations": num_recommendations,
        "total_components": total_components,
        "approval_indices": top_recommendations[['MODELO', 'approval_Index']].to_dict(orient='records')
    }

    recomendaciones_global = df.to_dict(orient='records')  # Asegúrate de que tienes la variable recomendaciones_global
    
    return render_template('/usuario/estadisticas.html', estadisticas=estadisticas_data, recomendaciones=recomendaciones_global)
@app.route('/recomendaciones', methods=['GET', 'POST'])
def recomendaciones():
    if request.method == 'POST':
        num_recommendations_str = request.form.get('num_recommendations', '5')
        if num_recommendations_str:
            try:
                num_recommendations = int(float(num_recommendations_str))
            except ValueError:
                num_recommendations = 5  # Valor por defecto si hay un error en la conversión
        else:
            num_recommendations = 5  # Valor por defecto si el campo está vacío
        session['num_recommendations'] = num_recommendations  # Guardar el valor en la sesión
    else:
        num_recommendations = session.get('num_recommendations', 5)  # Recuperar el valor de la sesión o usar el valor por defecto

    with open('recomendaciones.json', 'r') as file:
        recomend_json = file.read()

    recomend = json.loads(recomend_json)
    recomend = transform_data(recomend)

    # Agregar campo de imagen
    recomend = add_image_field(recomend)

    # Obtener los datos de la base de datos
    df = get_components_from_db()

    # Actualizar los datos de los componentes
    updated_recomend = update_component_data(recomend, df)

    # Ordenar las recomendaciones actualizadas por índice de aprobación
    updated_recomend = sorted(updated_recomend, key=lambda x: x['approval_Index'], reverse=True)

    # Limitar la cantidad de recomendaciones
    updated_recomend = updated_recomend[:num_recommendations]

    return render_template('/usuario/recomendaciones.html', recomend=updated_recomend, num_recommendations=num_recommendations)

@app.route('/resultados')
def resultados():

    with open('recomendaciones.json', 'r') as file:
            recomend_json = file.read()

# Convertir la cadena JSON a una lista de Python
    recomend2 = json.loads(recomend_json)
    
    recomend2 = transform_data(recomend2)
    
    return render_template('/usuario/resultados.html',recomend2=recomend2)

@app.route('/acceso-login', methods=['GET', 'POST'])
def adn_telecom():
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form:
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']
       
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo = %s AND password = %s', (_correo, _password))
        account = cur.fetchone()
       
        if account:
            session['logueado'] = True
            session['id'] = account['id']
            session['id_rol'] = account['id_rol']
           
            if session['id_rol'] == 1:
                return render_template('admin.html')   
            elif session['id_rol'] == 2:
                return render_template('usuario.html')
          
        else:    
            return render_template('index.html', mensaje='Usuario o contraseña incorrecta')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/crear-registro', methods=['GET', 'POST'])
def crear_registro():
    nombre = request.form['txtNombre']
    correo = request.form['txtCorreo']
    password = request.form['txtPassword']
    
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO usuarios(nombre, correo, password, id_rol) VALUES(%s,%s,%s,2)', (nombre, correo, password))
    mysql.connection.commit()
    
    return render_template('index.html', mensaje2='Registro exitoso')

@app.route('/listar', methods=['GET', 'POST'])
def listar():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios WHERE id_rol != 1')
    usuarios = cur.fetchall()
    cur.close()
    
    return render_template('listar_usuarios.html', usuarios=usuarios)

@app.route('/eliminar/<string:id>')
def eliminar(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM usuarios WHERE id = {0}'.format(id))
    mysql.connection.commit()
    
    return redirect('/listar')

@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    nombre = request.form['txtNombre']
    correo = request.form['txtCorreo']
    password = request.form['txtPassword']

    cur = mysql.connection.cursor()
    try:
        cur.execute('UPDATE usuarios SET nombre = %s, correo = %s, password = %s WHERE id = %s', (nombre, correo, password, id))
        mysql.connection.commit()
    finally:
        cur.close()

    return redirect('/listar')

@app.route('/modificar/<id>', methods=['GET', 'POST'])
def modificar(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios WHERE id = %s', (id,))
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
    
    return render_template('usuario/estructura.html', estructura=estructura)

    # Ruta para obtener la respuesta del bot
@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json.get('message').lower()  # Obtener el mensaje del usuario en minúsculas
    bot_response = generate_bot_response(user_message)
    return jsonify({'response': bot_response})

# Función para generar la respuesta del bot
def generate_bot_response(message):
    with open('respuestas.json', 'r', encoding='utf-8') as file:
        responses = json.load(file)
    
    return responses.get(message, "Lo siento, no entiendo tu mensaje.")

if __name__ == '__main__':
    app.secret_key = "frank"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)

'''
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

local_timezone = pytz.timezone("America/Lima")  #Designamos esto a tu zona horaria local

@app.route('/', methods=['GET', 'POST'])
def trafico():
    if request.method == 'POST':
        fecha_inicio = request.form['fecha_inicio']
        hora_inicio = request.form['hora_inicio']
        fecha_fin = request.form['fecha_fin']
        hora_fin = request.form['hora_fin']

        try:
            #Convertimos a objetos datetime en la zona horaria local
            inicio = local_timezone.localize(datetime.strptime(f"{fecha_inicio} {hora_inicio}", "%Y-%m-%d %H:%M"))
            fin = local_timezone.localize(datetime.strptime(f"{fecha_fin} {hora_fin}", "%Y-%m-%d %H:%M"))

            #Verificamos las horas ingresadas
            if inicio <= datetime.now(local_timezone):
                error = "La hora de inicio ya ha pasado."
                return render_template('trafico.html', error=error)

            if fin <= inicio:
                error = "La hora de fin debe ser posterior a la hora de inicio."
                return render_template('trafico.html', error=error)

            #Iniciamos la medición
            medir_trafico(inicio, fin)

            return redirect(url_for('trafico'))

        except ValueError:
            error = "Formato de fecha y hora incorrecto."
            return render_template('trafico.html', error=error)

    return render_template('trafico.html')

if __name__ == '_main_':
    app.run(debug=True)
'''
