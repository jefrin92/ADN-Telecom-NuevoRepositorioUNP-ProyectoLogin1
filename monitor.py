import time
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import pytz
import psutil
#Asignamos la zona horaria local
local_timezone = pytz.timezone("America/Lima")  # Cambia esto a tu zona horaria local

#Creamos listas vacías para almacenar datos de tráfico
tiempos = []
trafico_enviado = []
trafico_recibido = []

def medir_trafico(inicio, fin):
    #Calculamos el tiempo de medición en segundos
    tiempo_medicion = (fin - inicio).total_seconds()

    #Segun la hora asignada al hacer click se espera 
    print(f"Esperando hasta la hora de inicio: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    while datetime.now(local_timezone) < inicio:
        time.sleep(1)

    tiempo_inicial = time.time()
    tiempo_actual = time.time()

    while tiempo_actual - tiempo_inicial <= tiempo_medicion:
        net_io = psutil.net_io_counters()
        #Obtenemos el tráfico de red en bytes recibidos y enviados
        bytes_enviados = net_io.bytes_sent
        bytes_recibidos = net_io.bytes_recv

        #Convertimos a megabytes
        mb_enviados = bytes_enviados / (1024 * 1024)
        mb_recibidos = bytes_recibidos / (1024 * 1024)

        #Almacenamos datos para graficar en vivo
        tiempos.append(tiempo_actual - tiempo_inicial)  #Registrar tiempo transcurrido desde el inicio
        trafico_enviado.append(mb_enviados + np.random.uniform(-0.5, 0.5))  # Simular fluctuaciones aleatorias
        trafico_recibido.append(mb_recibidos + np.random.uniform(-0.5, 0.5))  # Simular fluctuaciones aleatorias

        #Actualizamos gráfica en vivo
        actualizar_grafica_en_vivo()

        time.sleep(10)  #Esperamos 10 segundos antes de la siguiente medición
        tiempo_actual = time.time()

    #Mostramos resultados finales
    mostrar_resultados_finales()

def actualizar_grafica_en_vivo():
    #Graficamos tráfico enviado y recibido en vivo
    plt.figure(figsize=(10, 6))
    plt.plot(tiempos, trafico_enviado, label='Enviado')
    plt.plot(tiempos, trafico_recibido, label='Recibido')
    plt.title('Tráfico en Vivo')
    plt.xlabel('Tiempo (segundos)')
    plt.ylabel('Tráfico (MB)')
    plt.legend()
    plt.grid(True)
    plt.pause(0.01)  # Pausa breve para actualizar la gráfica

def mostrar_resultados_finales():
    #Graficamos tráfico enviado y recibido final en una ventana aparte
    plt.figure(figsize=(10, 6))
    plt.plot(tiempos, trafico_enviado, label='Enviado')
    plt.plot(tiempos, trafico_recibido, label='Recibido')
    plt.title('Tráfico Final')
    plt.xlabel('Tiempo (segundos)')
    plt.ylabel('Tráfico (MB)')
    plt.legend()
    plt.grid(True)
    plt.show()

    #Finalmente mostramos cantidad total de megabytes enviados y recibidos
    total_enviado = trafico_enviado[-1]
    total_recibido = trafico_recibido[-1]
    tiempo_total = tiempos[-1]

    print(f"Total enviado: {total_enviado:.2f} MB")
    print(f"Total recibido: {total_recibido:.2f} MB")
    print(f"Tiempo total de medición: {tiempo_total:.2f} segundos")
