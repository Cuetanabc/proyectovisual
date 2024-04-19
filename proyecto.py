# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 21:29:23 2024

@author: den_0
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar los conjuntos de datos mensuales
df_ene = pd.read_csv('datos_enero_2021.csv')
df_feb = pd.read_csv('datos_febrero_2021.csv')
df_mar = pd.read_csv('datos_marzo_2021.csv')
df_abr = pd.read_csv('datos_abril_2021.csv')
df_may = pd.read_csv('datos_mayo_2021.csv')
df_jun = pd.read_csv('datos_junio_2021.csv')

# Convertir la columna de fecha a tipo datetime y eliminar las horas
df_ene['Fecha'] = pd.to_datetime(df_ene['Fecha']).dt.date
df_feb['Fecha'] = pd.to_datetime(df_feb['Fecha']).dt.date
df_mar['Fecha'] = pd.to_datetime(df_mar['Fecha']).dt.date
df_abr['Fecha'] = pd.to_datetime(df_abr['Fecha']).dt.date
df_may['Fecha'] = pd.to_datetime(df_may['Fecha']).dt.date
df_jun['Fecha'] = pd.to_datetime(df_jun['Fecha']).dt.date

# Unir los conjuntos de datos en uno solo
df = pd.concat([df_ene, df_feb, df_mar, df_abr, df_may, df_jun])

# Crear gráficos de líneas para NO2 y PM10
fig_lineas = px.line(df, x='Fecha', y=['NO2 (ug/m3)', 'PM10 \n(ug/m3)'], title='Evolución de NO2 y PM10 de enero a junio de 2021',
                     labels={'Fecha': 'Fecha', 'value': 'Concentración (ug/m3)', 'variable': 'Contaminante'},
                     template='plotly_dark')

# Crear un gráfico de dispersión para NO2 vs PM10
fig_dispersion = px.scatter(df, x='NO2 (ug/m3)', y='PM10 \n(ug/m3)', title='Diagrama de dispersión entre NO2 y PM10',
                            labels={'NO2 (ug/m3)': 'NO2 (ug/m3)', 'PM10 \n(ug/m3)': 'PM10 (ug/m3)'},
                            template='plotly_dark')

# Crear una tabla con los datos
tabla = df.copy()
tabla['Fecha'] = pd.to_datetime(tabla['Fecha']).dt.strftime('%Y-%m-%d') # Formatear la fecha
tabla = tabla.rename(columns={'PM10 \n(ug/m3)': 'PM10', 'NO2 (ug/m3)': 'NO2'}) # Renombrar las columnas
tabla = tabla[['Fecha', 'PM10', 'NO2']] # Seleccionar las columnas que queremos mostrar en la tabla

# Crear el dashboard con pestañas
st.title('Dashboard de Calidad del Aire')
st.markdown('Este dashboard muestra la evolución de la calidad del aire durante los primeros seis meses del año 2021.')

# Agregar pestañas
pestañas = st.sidebar.radio("Navegación", ['Gráfico de Líneas', 'Diagrama de Dispersión', 'Datos'])

if pestañas == 'Gráfico de Líneas':
    st.plotly_chart(fig_lineas)

elif pestañas == 'Diagrama de Dispersión':
    # Agregar opciones interactivas para filtrar los datos
    rango_no2 = st.slider("Seleccionar rango de NO2 (ug/m3)", float(df['NO2 (ug/m3)'].min()), float(df['NO2 (ug/m3)'].max()), (float(df['NO2 (ug/m3)'].min()), float(df['NO2 (ug/m3)'].max())))
    rango_pm10 = st.slider("Seleccionar rango de PM10 (ug/m3)", float(df['PM10 \n(ug/m3)'].min()), float(df['PM10 \n(ug/m3)'].max()), (float(df['PM10 \n(ug/m3)'].min()), float(df['PM10 \n(ug/m3)'].max())))
    
    # Filtrar los datos según los rangos seleccionados
    df_filtrado = df[(df['NO2 (ug/m3)'] >= rango_no2[0]) & (df['NO2 (ug/m3)'] <= rango_no2[1]) &
                     (df['PM10 \n(ug/m3)'] >= rango_pm10[0]) & (df['PM10 \n(ug/m3)'] <= rango_pm10[1])]
    
    # Actualizar el gráfico de dispersión con los datos filtrados
    fig_dispersion_filtrado = px.scatter(df_filtrado, x='NO2 (ug/m3)', y='PM10 \n(ug/m3)', title='Diagrama de dispersión entre NO2 y PM10 (Filtrado)',
                                         labels={'NO2 (ug/m3)': 'NO2 (ug/m3)', 'PM10 \n(ug/m3)': 'PM10 (ug/m3)'},
                                         template='plotly_dark')
    st.plotly_chart(fig_dispersion_filtrado)

elif pestañas == 'Datos':
    st.write(tabla)
