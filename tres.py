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
required_columns = ['Nombre del producto', 'Descuento']
for col in required_columns:
    if col not in df.columns:
        print(f"Error: La columna '{col}' no existe en el archivo CSV.")
        exit()

# Agrupar por Mes y Producto, y encontrar el máximo descuento
df_agrupado = df.groupby(['Mes', 'Nombre del producto'])['Descuento'].max().reset_index()

# Encontrar el producto con el mayor descuento por mes
df_max_descuento = df_agrupado.loc[df_agrupado.groupby('Mes')['Descuento'].idxmax()]

# Renombrar la columna 'Nombre del producto' a 'Producto con mayor descuento'
df_max_descuento.rename(columns={'Nombre del producto': 'Producto con mayor descuento'}, inplace=True)

# Seleccionar solo las columnas necesarias
df_final = df_max_descuento[['Mes', 'Producto con mayor descuento', 'Descuento']]

# Mostrar el resultado en consola
print("Producto con mayor descuento por mes:")
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
fig = px.bar(df_final, x='Mes', y='Descuento', color='Producto con mayor descuento', 
             title='Producto con mayor descuento por mes',
             labels={'Mes': 'Mes', 'Descuento': 'Porcentaje de descuento', 'Producto con mayor descuento': 'Producto'},
             text='Producto con mayor descuento',
             category_orders={"Mes": orden_meses})  # Asegurar el orden de los meses

# Rotar las etiquetas del eje X para mejor visualización
fig.update_layout(
    xaxis_title='Mes', 
    yaxis_title='Porcentaje de descuento', 
    legend_title='Producto con mayor descuento',
    xaxis_tickangle=-45,  # Rotar las etiquetas del eje X 45 grados
    yaxis_showticklabels=True  # Mostrar las etiquetas del eje Y
)

# Abrir el gráfico directamente en el navegador
fig.show(renderer="browser")