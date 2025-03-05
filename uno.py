import pandas as pd
import plotly.express as px

# Cargar el archivo CSV
try:
    df = pd.read_csv('datos.csv')
    print("Columnas del DataFrame:", df.columns)  # Verifica las columnas
    print("Primeras filas del DataFrame:\n", df.head())  # Verifica las primeras filas
except FileNotFoundError:
    print("Error: El archivo 'datos.csv' no se encontró.")
    exit()

# Verificar si la columna 'Fecha de la orden' existe
if 'Fecha de la orden' not in df.columns:
    print("Error: La columna 'Fecha de la orden' no existe en el archivo CSV.")
    print("Columnas disponibles:", df.columns)
    exit()

# Convertir la columna 'Fecha de la orden' a tipo datetime
df['Fecha de la orden'] = pd.to_datetime(df['Fecha de la orden'])

# Extraer solo el mes (en formato numérico)
df['Mes'] = df['Fecha de la orden'].dt.month  # Extrae el número del mes (1 para enero, 2 para febrero, etc.)

# Verificar si las columnas necesarias existen
required_columns = ['Estado', 'Nombre del producto', 'Cantidad ordenada']
for col in required_columns:
    if col not in df.columns:
        print(f"Error: La columna '{col}' no existe en el archivo CSV.")
        exit()

# Agrupar por Estado, Mes y Producto, y sumar la cantidad ordenada
df_agrupado = df.groupby(['Estado', 'Mes', 'Nombre del producto'])['Cantidad ordenada'].sum().reset_index()

# Encontrar el producto más vendido por estado y mes
df_max = df_agrupado.loc[df_agrupado.groupby(['Estado', 'Mes'])['Cantidad ordenada'].idxmax()]

# Renombrar la columna 'Nombre del producto' a 'Producto más vendido'
df_max.rename(columns={'Nombre del producto': 'Producto más vendido'}, inplace=True)

# Seleccionar solo las columnas necesarias
df_final = df_max[['Estado', 'Mes', 'Producto más vendido']]

# Mostrar el resultado en consola
print("Producto más vendido por estado y mes:")
print(df_final)

# Convertir el número del mes a nombre del mes para mejor visualización
meses = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
    7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}
df_final['Mes'] = df_final['Mes'].map(meses)

# Definir el orden correcto de los meses
orden_meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
               'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

# Convertir la columna 'Mes' a un tipo categórico con el orden correcto
df_final['Mes'] = pd.Categorical(df_final['Mes'], categories=orden_meses, ordered=True)

# Visualización interactiva con Plotly
fig = px.bar(df_final, x='Estado', y='Mes', color='Producto más vendido', 
             title='Producto más vendido por mes y por estado',
             labels={'Mes': 'Mes', 'Estado': 'Estado', 'Producto más vendido': 'Producto más vendido'},
             text='Producto más vendido',
             category_orders={"Mes": orden_meses})  # Asegurar el orden de los meses

# Rotar las etiquetas del eje X para que los estados se vean verticalmente
fig.update_layout(
    xaxis_title='Estado', 
    yaxis_title='Mes', 
    legend_title='Producto más vendido',
    xaxis_tickangle=-90,  # Rotar las etiquetas del eje X 90 grados (vertical)
    yaxis_showticklabels=False  # Ocultar las etiquetas del eje Y
)

# Abrir el gráfico directamente en el navegador
fig.show(renderer="browser")