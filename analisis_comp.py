import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import json
import matplotlib.pyplot as plt

# Cargar los datos desde un archivo CSV
data = pd.read_csv('Networks_Components.csv')

# Explorar los datos
print(data.head())  # Muestra las primeras filas del dataset
print(data.columns)
print(data.describe())  # Estadísticas descriptivas del dataset

# Preprocesamiento de datos
# Aquí puedes realizar la limpieza, transformación y selección de características según tus necesidades

# Asegúrate de que todos los datos son numéricos
data = data.apply(pd.to_numeric, errors='coerce')

# Elimina las filas con valores NaN
data = data.dropna()

# Imputar valores faltantes con la media
data = data.fillna(data.mean())

# Ahora deberías poder crear tu pairplot
sns.pairplot(data)
plt.show() 

#Codificación one-hot para la columna 'columna_categorica'
data = pd.get_dummies(data)

# Asegúrate de que las columnas especificadas existen en tu DataFrame
features = ['COSTO ($)', 'Velocidad de Red (Mbps)', 'Year', 'Nro de Puertos']
target = 'recomendacion'

if all(item in data.columns for item in features) and target in data.columns:
    X = data[features]
    y = data[target]
else:
    print("Las columnas especificadas no existen en el DataFrame.")
    exit()

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar un modelo de regresión lineal
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluar el modelo
score = model.score(X_test, y_test)
print(f'Precisión del modelo: {score}')

# Realizar predicciones
predicciones = model.predict(X_test)

# Convertir las predicciones en un DataFrame
df_predicciones = pd.DataFrame(predicciones, columns=['Predicciones'])

# Guardar el DataFrame en un archivo CSV
df_predicciones.to_csv('predicciones.csv', index=False)

# Convertir las predicciones a una lista, reemplazando NaN e infinito con None
predicciones_list = [x if (np.isfinite(x) and not np.isnan(x)) else None for x in predicciones.tolist()]

# Convertir la lista a una cadena JSON
predictions_json = json.dumps(predicciones_list)

# Escribir la cadena JSON en un archivo
with open('predictions.json', 'w') as file:
    file.write(predictions_json)