import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors
import numpy as np
import json

# Función para convertir las columnas categóricas a tipo string y eliminar espacios en blanco
def clean_categorical_data(df, columns):
    for column in columns:
        if df[column].dtype == 'object':
            df[column] = df[column].astype(str).str.strip()
    return df

# Cargar los datos
df = pd.read_csv('Red_Components_transformed.csv')

# Mostrar las columnas del DataFrame para depuración
print("Columnas del DataFrame:", df.columns)

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

# Limpiar datos categóricos
df = clean_categorical_data(df, ['EQUIPO', 'MODELO', 'MARCA', 'Estructura_de_Red'])

# Convertir las columnas categóricas a valores numéricos utilizando LabelEncoder
label_encoders = {}
for column in ['EQUIPO', 'MODELO', 'MARCA', 'Estructura_de_Red']:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

# Seleccionar las características para el sistema de recomendaciones
features = df.drop('approval_Index', axis=1)

# Crear y entrenar el modelo KNN
knn = NearestNeighbors(metric='cosine')
knn.fit(features)

# Función para hacer recomendaciones
def recommend(input_data, knn_model, data, num_recommendations):
    knn_model.set_params(n_neighbors=len(data))  # Considerar todos los vecinos para poder ordenar después
    distances, indices = knn_model.kneighbors([input_data])
    recommendations = data.iloc[indices[0]]
    
    # Ordenar las recomendaciones por el índice de aprobación en orden descendente
    recommendations = recommendations.sort_values(by='approval_Index', ascending=False)
    
    # Limitar la cantidad de recomendaciones
    return recommendations.head(num_recommendations)

# Número de recomendaciones a generar (puedes cambiar este valor o hacer que sea dinámico)
num_recommendations = 10

# Datos de entrada para la recomendación
new_data = [1, 2, 3, 200, 1000, 2019, 1, 10, 0]  # Modificar según las características del dataset

# Obtener recomendaciones basadas en el índice de aprobación
recommendations = recommend(new_data, knn, df, num_recommendations=num_recommendations)
print(recommendations)

# Generar JSON de recomendaciones
recommendations_list = []
for index, row in recommendations.iterrows():
    recommendation_dict = {
        "Componente recomendado": index + 1,
        "iD": row['iD'],  # Asegúrate de que 'iD' está presente en 'df'
        "Equipo": row['EQUIPO'],
        "Modelo": row['MODELO'],
        "Marca": row['MARCA'],
        "Año": row['Year'],
        "Estructura de Red": row['Estructura_de_Red'],
        "Velocidad de Red": row['VELOCIDAD DE RED EN GB'],  # Asegúrate de que este campo coincide con el nombre de la columna en tu DataFrame  
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
    recommendations_list.append(recommendation_dict)

# Convierte la lista de recomendaciones a una cadena JSON
json_recommendations = json.dumps(recommendations_list)

# Guarda la cadena JSON en un archivo
with open('recomendaciones.json', 'w') as file:
    file.write(json_recommendations)
 
# Imprimir el JSON generado para verificar
print(json.dumps(recommendations_list, indent=4))

print("Recomendaciones guardadas en el archivo 'recomendaciones.json'")