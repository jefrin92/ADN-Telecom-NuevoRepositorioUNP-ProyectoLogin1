# -*- coding: utf-8 -*-
"""sistema_de_recomendaciones (1).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gqGBVXase72I6pFOWZuzxYT7R5jhMQeo
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors
import numpy as np

"""###Carga y Preprocesamiento de Datos"""

# Cargar los datos
df = pd.read_csv('Red_Components_transformed.csv')


# Convertir la columna 'Year' a tipo numérico
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

# Función para convertir 'VELOCIDAD DE RED' a tipo numérico
def convert_speed(speed):
    if 'Gbps' in speed:
        return float(speed.replace('Gbps', '').strip()) * 1000
    elif 'Mbps' in speed:
        return float(speed.replace('Mbps', '').strip())
    else:
        return float(speed)

df.dropna(inplace=True)

# Convertir las columnas categóricas a valores numéricos utilizando LabelEncoder
label_encoders = {}
for column in ['EQUIPO', 'MODELO', 'MARCA', 'Estructura_de_Red']:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

# Verificar el dataframe transformado
print(df.head())

"""###Modelo de Recomendaciones"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Seleccionar las características para el sistema de recomendaciones
features = df.drop('approval_Index', axis=1)

# Crear y entrenar el modelo KNN
knn = NearestNeighbors(n_neighbors=5, metric='cosine')
knn.fit(features)

# Función para hacer recomendaciones
def recommend(input_data, knn_model, data):
    distances, indices = knn_model.kneighbors([input_data])
    recommendations = data.iloc[indices[0]]
    return recommendations

new_data = [1, 2, 3, 200, 1000, 2019, 1, 10, 0]  # Modificar según las características del dataset

recommendations = recommend(new_data, knn, df)
print(recommendations)

recommendations = recommend(new_data, knn, df)
print("Recomendaciones:")
print(recommendations)

print("Recomendaciones:")
for index, row in recommendations.iterrows():
    print(f"\nComponente recomendado {index + 1}:")
    print(f"iD: {row['iD']}")
    print(f"Equipo: {row['EQUIPO']}")
    print(f"Modelo: {row['MODELO']}")
    print(f"Marca: {row['MARCA']}")
    print(f"Año: {row['Year']}")
    print(f"Estructura de Red: {row['Estructura_de_Red']}")
    print(f"approval_Index: {row['approval_Index']}")
    print(f"\nEsta recomendación se basa en las similitudes encontradas con las siguientes características ingresadas:")
    print(f"Equipo: {new_data[0]}")
    print(f"Modelo: {new_data[1]}")
    print(f"Marca: {new_data[2]}")
    print(f"Velocidad de Red: {new_data[3]} Mbps")
    print(f"Costo: {new_data[4]}")
    print(f"Año: {new_data[5]}")
    print(f"Estructura de Red: {new_data[6]}")
    print(f"Otra característica: {new_data[7]}")
    print(f"Adicional: {new_data[8]}")

import json

# Inicializa una lista vacía para almacenar las recomendaciones
recommendations_list = []

# Itera sobre cada fila del DataFrame recommendations
for index, row in recommendations.iterrows():
    # Crea un diccionario para almacenar los datos de la recomendación
    recommendation_dict = {
        "Componente recomendado": index + 1,
        "iD": row['iD'],
        "Equipo": row['EQUIPO'],
        "Modelo": row['MODELO'],
        "Marca": row['MARCA'],
        "Año": row['Year'],
        "Estructura de Red": row['Estructura_de_Red'],
        "approval_Index": row['approval_Index'],
        "Características ingresadas": {
            "Equipo": new_data[0],
            "Modelo": new_data[1],
            "Marca": new_data[2],
            "Velocidad de Red": f"{new_data[3]} Mbps",
            "Costo": new_data[4],
            "Año": new_data[5],
            "Estructura de Red": new_data[6],
            "Otra característica": new_data[7],
            "Adicional": new_data[8]
        }
    }
    # Agrega el diccionario a la lista de recomendaciones
    recommendations_list.append(recommendation_dict)

# Convierte la lista de recomendaciones a una cadena JSON
json_recommendations = json.dumps(recommendations_list)

# Guarda la cadena JSON en un archivo
with open('recomendaciones.json', 'w') as file:
    file.write(json_recommendations)

print("Recomendaciones guardadas en el archivo 'recomendaciones.json'")