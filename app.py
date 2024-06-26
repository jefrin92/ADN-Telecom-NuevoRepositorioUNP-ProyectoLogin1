from flask import Flask, render_template,jsonify, redirect, request, session,url_for,send_from_directory
from flask_mysqldb import MySQL, MySQLdb
import json
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors
from datetime import datetime, timedelta
import pytz
import psutil
import time  # Import the time module
import numpy as np  # Import the numpy module
import matplotlib.pyplot as plt  # Import the matplotlib module
import os
from uuid import uuid4
import threading

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
        2: "https://http2.mlstatic.com/D_NQ_NP_703457-MLA31353406875_072019-O.webp",
        3: "https://th.bing.com/th/id/OIP.F0D7ICcmz6u0U4i2alqjzQHaHa?rs=1&pid=ImgDetMain",
        4: "https://th.bing.com/th/id/OIP.X7FYsfkFmdP5hsbqJIsRwQAAAA?rs=1&pid=ImgDetMain",
        5: "https://s.alicdn.com/@sc04/kf/U5924c2cf05b64cb9a64670126f0de427N.jpg_720x720q50.jpg",
        6: "https://th.bing.com/th/id/OIP.9jqNniLD-c1cJT5D6O0gawHaHa?rs=1&pid=ImgDetMain",
        7: "https://th.bing.com/th/id/OIP.KTsT3tv5Sr2ldEywx11qzQHaHa?rs=1&pid=ImgDetMain",
        8: "https://th.bing.com/th/id/OIP.g-ai8Qmzfbz1gy30DqPftgHaHa?rs=1&pid=ImgDetMain",
        9: "https://th.bing.com/th/id/OIP.fkZq0sp71cxtuOfxz4rrsgHaHa?rs=1&pid=ImgDetMain",
        10: "https://th.bing.com/th/id/OIP.BwivpHBDhkgmKd4XQauJHQHaHa?rs=1&pid=ImgDetMain",
        11: "https://americadigital.com.gt/wp-content/uploads/2022/02/EO145NZTEZXA10C320a.jpg",
        12: "https://www.henanliyuan.com/Uploads/5d9176ab20d872779.jpg",
        13: "https://http2.mlstatic.com/D_NQ_NP_2X_730541-MLB44905216280_022021-F.jpg",
        14: "https://cdn.myshoptet.com/usr/www.ponplanet.eu/user/shop/big/579_v1600gs-o32.jpg?65361b70",
        15: "https://th.bing.com/th/id/OIP.R4_bV-hPjneL98gl34on7wAAAA?rs=1&pid=ImgDetMain",
        16: "https://www.cyberteam.pl/_image/product/7746/7746_7746-fibertechnic-olt-gpon-fd1608s-b0-8xgpon-2x10gbit-4x1g-uplink-combo--2xac_03.jpg",
        17: "https://www.comx-computers.co.za/i/mikrotik/52907_IMG1.jpg",
        18: "https://www.wisp.pl/galerie/m/mikrotik-cloud-core-router-cc_12697.jpg",
        19: "https://m.media-amazon.com/images/I/71Qp4cPJNIL._AC_SL1500_.jpg",
        20: "https://www.aibitech.com/3405-large_default/router-routerboard-mikrotik-rb951ui-2hnd-wireless-1000mw-24ghz-80211bgn-5-ethernet-1usb-l4.jpg",
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
        component_id = int(component.get("iD", -1))  # Utiliza un valor predeterminado en caso de que "ID" no esté presente
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
                component['Velocidad_Red'] = db_row['Velocidad_Red']
                component['Año'] = db_row['Year']  
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
    # Aquí se obtiene y se muestran los componentes de la base de datos
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM componentes")
    data = cur.fetchall()
    cur.close()
    return render_template('/usuario/componentes.html', componentes=data)


@app.route('/agregar_componente', methods=['GET', 'POST'])
def agregar_componente():
    if request.method == 'POST':
        equipo = request.form['EQUIPO']
        modelo = request.form['MODELO']
        marca = request.form['MARCA']
        costo = request.form['COSTO']
        velocidad_red = request.form['Velocidad_Red']
        year = request.form['Year']
        estructura_red = request.form['Estructura_Red']
        nro_puertos = request.form['Nro_Puertos']
        descripcion = request.form['descripcion']
        imagen = request.form['Imagen']
        create_component(mysql, equipo, modelo, marca, costo, velocidad_red, year, estructura_red, nro_puertos, descripcion, imagen)
        return redirect(url_for('componentes'))
    return render_template('/usuario/agregar_componente.html')

def create_component(mysql, equipo, modelo, marca, costo, velocidad_red, year, estructura_red, nro_puertos, descripcion, imagen):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO componentes (EQUIPO, MODELO, MARCA, COSTO, Velocidad_Red, Year, Estructura_Red, Nro_Puertos, descripcion, Imagen)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (equipo, modelo, marca, costo, velocidad_red, year, estructura_red, nro_puertos, descripcion, imagen))
    mysql.connection.commit()
    cur.close()
 
    
@app.route('/editar_componente/<int:id>', methods=['GET', 'POST'])
def editar_componente(id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        equipo = request.form['EQUIPO']
        modelo = request.form['MODELO']
        marca = request.form['MARCA']
        costo = request.form['COSTO']
        velocidad_red = request.form['Velocidad_Red']
        year = request.form['Year']
        estructura_red = request.form['Estructura_Red']
        nro_puertos = request.form['Nro_Puertos']
        
        descripcion = request.form['descripcion']
        imagen = request.form['Imagen']

        cur.execute("""
            UPDATE componentes
            SET EQUIPO=%s, MODELO=%s, MARCA=%s, COSTO=%s, Velocidad_Red=%s, Year=%s, Estructura_Red=%s, Nro_Puertos=%s, descripcion=%s, Imagen=%s
            WHERE ID=%s
        """, (equipo, modelo, marca, costo, velocidad_red, year, estructura_red, nro_puertos, descripcion, imagen, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('componentes'))
    else:
        cur.execute("SELECT * FROM componentes WHERE ID = %s", (id,))
        componente = cur.fetchone()
        cur.close()
        return render_template('usuario/editar_componente.html', componente=componente)



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

    session['approval_indices'] = [
        {'MODELO': rec['Modelo'], 'approval_Index': rec['approval_Index']}
        for rec in updated_recomend
    ]

    return render_template('/usuario/recomendaciones.html', recomend=updated_recomend, num_recommendations=num_recommendations)

@app.route('/estadisticas')
def estadisticas():
    # Obtener los datos de la base de datos
    df = get_components_from_db()
    
    # Calcular porcentajes de aprobación
    df['approval_Index'] = df['approval_Index'].apply(lambda x: round((x / 10) * 100, 2))
    
    # Obtener las recomendaciones almacenadas en la sesión
    approval_indices = session.get('approval_indices', [])

    # Calcular estadísticas, por ejemplo, contar la cantidad de cada tipo de equipo
    equipo_counts = df['EQUIPO'].value_counts().reset_index()
    equipo_counts.columns = ['Equipo', 'Cantidad']

    # Definir el número de recomendaciones
    num_recommendations = session.get('num_recommendations', min(len(df), 10))  # Recuperar el valor de la sesión o usar el valor por defecto
    total_components = 27  # Total de componentes

    # Convertir tipos para serializar correctamente
    equipo_counts = equipo_counts.astype({'Equipo': str, 'Cantidad': int})

    estadisticas_data = {
        "equipo_counts": equipo_counts.to_dict(orient='records'),
        "num_recommendations": int(num_recommendations),
        "total_components": int(total_components),
        "approval_indices": approval_indices
    }

    recomendaciones_global = df.to_dict(orient='records')  # Asegúrate de que tienes la variable recomendaciones_global
    
    return render_template('/usuario/estadisticas.html', estadisticas=estadisticas_data, recomendaciones=recomendaciones_global)

@app.route('/resultados')
def resultados():
    with open('recomendaciones.json', 'r') as file:
        recomend_json = file.read()

    # Convertir la cadena JSON a una lista de Python
    recomend2 = json.loads(recomend_json)
    
    recomend2 = transform_data(recomend2)

    # Agregar campo de imagen
    recomend2 = add_image_field(recomend2)

    # Obtener los datos de la base de datos
    df = get_components_from_db()

    # Actualizar los datos de los componentes
    updated_recomend2 = update_component_data(recomend2, df)
    
    # Ordenar los resultados por índice de aprobación en orden descendente
    updated_recomend2 = sorted(updated_recomend2, key=lambda x: x['approval_Index'], reverse=True)
    
    return render_template('/usuario/resultados.html', recomend2=updated_recomend2)

@app.route('/acceso-login', methods=['GET', 'POST'])
def adn_telecom():
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form:
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']
       
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo = %s AND password = %s', (_correo, _password))
        account = cur.fetchone()
        
        print(f"Datos de la cuenta obtenidos: {account}")  # Depuración
       
        if account:
            session['logueado'] = True
            session['id'] = account['id']
            session['id_rol'] = account['id_rol']
           
            if session['id_rol'] == 1:
                return render_template('admin.html')   
            elif session['id_rol'] == 2:
                return render_template('usuario.html')
          
        else:
            print("Correo o contraseña incorrectos")  # Depuración    
            return render_template('index.html', mensaje='Usuario o contraseña incorrecta')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/crear-registro', methods=['GET', 'POST'])
def crear_registro():
    if request.method == 'POST':
        nombre = request.form['txtNombre']
        correo = request.form['txtCorreo']
        password = request.form['txtPassword']
        
        # Verificar si el correo ya existe
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM usuarios WHERE correo = %s', (correo,))
        account = cur.fetchone()
        
        if account:
            return render_template('registro.html', mensaje='El correo ya está registrado, elija otro.')

        cur.execute('INSERT INTO usuarios(nombre, correo, password, id_rol) VALUES(%s, %s, %s, 2)', (nombre, correo, password))
        mysql.connection.commit()
        cur.close()
        
        mensaje2 = 'Registro exitoso'
        return render_template('registro.html', mensaje2=mensaje2)
    return render_template('registro.html')

@app.route('/listar', methods=['GET', 'POST'])
def listar():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios WHERE id_rol != 1')
    usuarios = cur.fetchall()
    cur.close()
    
    return render_template('listar_usuarios.html', usuarios=usuarios)

def eliminar(id):
    print(f"Eliminando usuario con ID: {id}")  # Agregar esto para depuración
    cur = mysql.connection.cursor()
    try:
        cur.execute('DELETE FROM usuarios WHERE ID = %s', (id,))
        mysql.connection.commit()
    finally:
        cur.close()
    return redirect(url_for('listar'))

@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    nombre = request.form['txtNombre']
    correo = request.form['txtCorreo']
    password = request.form['txtPassword']

    cur = mysql.connection.cursor()
    try:
        cur.execute('UPDATE usuarios SET nombre = %s, correo = %s, password = %s WHERE ID = %s', (nombre, correo, password, id))
        mysql.connection.commit()
    finally:
        cur.close()

    return redirect('/listar')

@app.route('/modificar/<id>', methods=['GET', 'POST'])
def modificar(id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        nombre = request.form['txtNombre']
        correo = request.form['txtCorreo']
        password = request.form['txtPassword']
        
        # Actualizar el usuario
        cur.execute('UPDATE usuarios SET nombre=%s, correo=%s, password=%s WHERE ID=%s', (nombre, correo, password, id))
        mysql.connection.commit()
        cur.close()
        return redirect('/listar')
    else:
        # Obtener los datos del usuario
        cur.execute('SELECT * FROM usuarios WHERE ID = %s', (id,))
        usuario = cur.fetchone()
        cur.close()
        
        return render_template('editar_usuarios.html', usuario=usuario)
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


#luis ###################
@app.route('/trafico', methods=['GET', 'POST'])
def trafico():
    if request.method == 'POST':
        fecha_inicio = request.form['fecha_inicio']
        hora_inicio = request.form['hora_inicio']
        fecha_fin = request.form['fecha_fin']
        hora_fin = request.form['hora_fin']

        try:
            inicio = local_timezone.localize(datetime.strptime(f"{fecha_inicio} {hora_inicio}", "%Y-%m-%d %H:%M"))
            fin = local_timezone.localize(datetime.strptime(f"{fecha_fin} {hora_fin}", "%Y-%m-%d %H:%M"))

            if inicio <= datetime.now(local_timezone):
                error = "La hora de inicio ya ha pasado."
                return render_template('/usuario/trafico.html', error=error)

            if fin <= inicio:
                error = "La hora de fin debe ser posterior a la hora de inicio."
                return render_template('/usuario/trafico.html', error=error)

            plot_paths, resumen = medir_trafico(inicio, fin)
            session['plot_paths'] = plot_paths  # Almacenar las rutas en la sesión
            session['resumen'] = resumen  # Almacenar el resumen en la sesión
            return redirect(url_for('mostrar_trafico'))
        except ValueError:
            error = "Formato de fecha y hora incorrecto."
            return render_template('/usuario/trafico.html', error=error)

    return render_template('/usuario/trafico.html')

#Asignamos la zona horaria local
local_timezone = pytz.timezone("America/Lima")  # Cambia esto a tu zona horaria local


# Directorio temporal para guardar las gráficas
TEMP_DIR = 'static/temp_plots'

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)


 
#Creamos listas vacías para almacenar datos de tráfico
tiempos = []
trafico_enviado = []
trafico_recibido = []

# Lista para almacenar rutas de gráficas
plot_paths = []

def save_plot():
    filename = os.path.join(TEMP_DIR, f'{uuid4().hex}.png')
    plt.savefig(filename)
    plt.close()
    # Devolver la ruta relativa desde el directorio 'static'
    relative_path = os.path.relpath(filename, start='static').replace('\\', '/')
    print(f"Imagen guardada en: {relative_path}")  # Agregar impresión para depuración
    return relative_path

def medir_trafico(inicio, fin):
    global plot_paths
    plot_paths = []

    # Calculamos el tiempo de medición en segundos
    tiempo_medicion = (fin - inicio).total_seconds()

    # Esperamos hasta la hora de inicio
    print(f"Esperando hasta la hora de inicio: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    while datetime.now(local_timezone) < inicio:
        time.sleep(1)

    tiempo_inicial = time.time()
    tiempo_actual = time.time()

    while tiempo_actual - tiempo_inicial <= tiempo_medicion:
        net_io = psutil.net_io_counters()
        # Obtenemos el tráfico de red en bytes recibidos y enviados
        bytes_enviados = net_io.bytes_sent
        bytes_recibidos = net_io.bytes_recv

        # Convertimos a megabytes
        mb_enviados = bytes_enviados / (1024 * 1024)
        mb_recibidos = bytes_recibidos / (1024 * 1024)

        # Almacenamos datos para graficar en vivo
        tiempos.append(tiempo_actual - tiempo_inicial)  # Registrar tiempo transcurrido desde el inicio
        trafico_enviado.append(mb_enviados + np.random.uniform(-0.5, 0.5))  # Simular fluctuaciones aleatorias
        trafico_recibido.append(mb_recibidos + np.random.uniform(-0.5, 0.5))  # Simular fluctuaciones aleatorias

        # Actualizamos gráfica en vivo y guardamos la ruta
        plot_path = actualizar_grafica_en_vivo(tiempos, trafico_enviado, trafico_recibido)
        plot_paths.append(plot_path)
        print(f"Ruta de la gráfica actualizada: {plot_path}")  # Depuración

        time.sleep(10)  # Esperamos 10 segundos antes de la siguiente medición
        tiempo_actual = time.time()

    # Mostramos resultados finales y guardamos la ruta de la gráfica final
    final_plot_path = mostrar_resultados_finales(tiempos, trafico_enviado, trafico_recibido)
    plot_paths.append(final_plot_path)
    print(f"Ruta de la gráfica final: {final_plot_path}")  # Depuración

    # Finalmente mostramos cantidad total de megabytes enviados y recibidos
    total_enviado = trafico_enviado[-1]
    total_recibido = trafico_recibido[-1]
    tiempo_total = tiempos[-1]

    resumen = {
        "total_enviado": f"{total_enviado:.2f} MB",
        "total_recibido": f"{total_recibido:.2f} MB",
        "tiempo_total": f"{tiempo_total:.2f} segundos"
    }
    print(f"Resumen: {resumen}")  # Depuración

    return plot_paths, resumen

def actualizar_grafica_en_vivo(tiempos, trafico_enviado, trafico_recibido):
    # Graficamos tráfico enviado y recibido en vivo
    plt.figure(figsize=(10, 6))
    plt.plot(tiempos, trafico_enviado, label='Enviado')
    plt.plot(tiempos, trafico_recibido, label='Recibido')
    plt.title('Tráfico en Vivo')
    plt.xlabel('Tiempo (segundos)')
    plt.ylabel('Tráfico (MB)')
    plt.legend()
    plt.grid(True)
    plt.pause(0.01)  # Pausa breve para actualizar la gráfica
    
    return save_plot()

def mostrar_resultados_finales(tiempos, trafico_enviado, trafico_recibido):
    # Graficamos tráfico enviado y recibido final en una ventana aparte
    plt.figure(figsize=(10, 6))
    plt.plot(tiempos, trafico_enviado, label='Enviado')
    plt.plot(tiempos, trafico_recibido, label='Recibido')
    plt.title('Tráfico Final')
    plt.xlabel('Tiempo (segundos)')
    plt.ylabel('Tráfico (MB)')
    plt.legend()
    plt.grid(True)

    # Guardamos la gráfica final
    final_plot_path = save_plot()

    # Finalmente mostramos cantidad total de megabytes enviados y recibidos
    total_enviado = trafico_enviado[-1]
    total_recibido = trafico_recibido[-1]
    tiempo_total = tiempos[-1]

    print(f"Total enviado: {total_enviado:.2f} MB")
    print(f"Total recibido: {total_recibido:.2f} MB")
    print(f"Tiempo total de medición: {tiempo_total:.2f} segundos")
    
    return final_plot_path

@app.route('/mostrar_trafico')
def mostrar_trafico():
    plot_paths = session.get('plot_paths')
    resumen = session.get('resumen')
    
    if not plot_paths or not resumen:
        return "No se pudo cargar la gráfica.", 404

    subtitles = [f"Imagen {i + 1}" for i in range(len(plot_paths))]

    return render_template('/usuario/mostrar_trafico.html', plot_paths=plot_paths, resumen=resumen, subtitles=subtitles, enumerate=enumerate, json=json)
#apr alimpiar  el buffer de plot

@app.route('/limpiar_archivos_y_volver')
def limpiar_archivos_y_volver():
    plot_paths = session.get('plot_paths')
    if plot_paths:
        eliminar_archivos(plot_paths)
    session.pop('plot_paths', None)  # Limpiar la sesión
    session.pop('resumen', None)  # Limpiar la sesión
    return redirect(url_for('trafico'))

def eliminar_archivos(plot_paths):
    for plot_path in plot_paths:
        try:
            # Construir la ruta absoluta desde el directorio 'static'
            absolute_path = os.path.join('static', plot_path)
            print(f"Intentando eliminar: {absolute_path}")  # Para depuración
            if os.path.exists(absolute_path):
                os.remove(absolute_path)
                print(f"Eliminado: {absolute_path}")
            else:
                print(f"El archivo {absolute_path} no existe")
        except Exception as e:
            print(f"Error al eliminar el archivo {absolute_path}: {e}")

#main ejecucion
if __name__ == '__main__':
    app.secret_key = "frank"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)






