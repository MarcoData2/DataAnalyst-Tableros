import pandas as pd
import plotly.express as px

# Cargar los datos desde el archivo CSV
try:
    datos = pd.read_csv('datos.csv')
    print("Columnas del DataFrame:", datos.columns)  # Verifica las columnas
    print("Primeras filas del DataFrame:\n", datos.head())  # Verifica las primeras filas
except FileNotFoundError:
    print("Error: El archivo 'datos.csv' no se encontró.")
    exit()

# Verificar si las columnas necesarias existen
required_columns = ['Segmento del cliente', 'Nombre del producto', 'Cantidad ordenada']
for col in required_columns:
    if col not in datos.columns:
        print(f"Error: La columna '{col}' no existe en el archivo CSV.")
        exit()

# Agrupar por Segmento del cliente y Nombre del producto, y sumar la cantidad ordenada
datos_agrupados = datos.groupby(['Segmento del cliente', 'Nombre del producto'])['Cantidad ordenada'].sum().reset_index()

# Ordenar los datos por Segmento del cliente y Cantidad ordenada en orden descendente
datos_agrupados = datos_agrupados.sort_values(by=['Segmento del cliente', 'Cantidad ordenada'], ascending=[True, False])

# Obtener los 3 productos más comprados por segmento
top_3_por_segmento = datos_agrupados.groupby('Segmento del cliente').head(3)

# Mostrar el resultado en consola
print("Top 3 productos más comprados por segmento:")
print(top_3_por_segmento)

# Crear el gráfico interactivo con plotly
fig = px.bar(top_3_por_segmento, x='Segmento del cliente', y='Cantidad ordenada', color='Nombre del producto',
             title='Top 3 productos más comprados por segmento',
             labels={'Cantidad ordenada': 'Cantidad Total Ordenada', 'Segmento del cliente': 'Segmento del Cliente'},
             text='Nombre del producto')

# Rotar las etiquetas del eje X para mejor visualización
fig.update_layout(
    xaxis_title='Segmento del Cliente', 
    yaxis_title='Cantidad Total Ordenada', 
    legend_title='Producto',
    xaxis_tickangle=-45,  # Rotar las etiquetas del eje X 45 grados
    yaxis_showticklabels=True  # Mostrar las etiquetas del eje Y
)

# Mostrar el gráfico
fig.show()