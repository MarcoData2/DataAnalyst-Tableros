import pandas as pd
import plotly.express as px

# Cargar los datos desde el archivo CSV
datos = pd.read_csv('datos.csv')

# Convertir la columna 'Fecha de la orden' a tipo datetime
datos['Fecha de la orden'] = pd.to_datetime(datos['Fecha de la orden'])

# Extraer el mes y el año de la fecha de la orden
datos['Mes'] = datos['Fecha de la orden'].dt.to_period('M')

# Agrupar por mes y código postal, y calcular el precio total de envío
datos_agrupados = datos.groupby(['Mes', 'Código Postal'])['Precio de envío'].sum().reset_index()

# Ordenar los datos por mes y por el precio de envío en orden descendente
datos_agrupados = datos_agrupados.sort_values(by=['Mes', 'Precio de envío'], ascending=[True, False])

# Obtener el top 5 de códigos postales más caros por mes
top_5_por_mes = datos_agrupados.groupby('Mes').head(5)

# Convertir el período a string para la visualización
top_5_por_mes['Mes'] = top_5_por_mes['Mes'].astype(str)

# Crear el gráfico interactivo con plotly
fig = px.bar(top_5_por_mes, x='Mes', y='Precio de envío', color='Código Postal',
             title='Top 5 Códigos Postales más caros para envíos por Mes',
             labels={'Precio de envío': 'Precio Total de Envío', 'Mes': 'Mes'},
             text='Código Postal')

# Mostrar el gráfico
fig.show()