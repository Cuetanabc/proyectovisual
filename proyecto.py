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
fig = px.line(df, x='Fecha', y=['NO2 (ug/m3)', 'PM10 \n(ug/m3)'], title='Evolución de NO2 y PM10 de enero a junio de 2021',
              labels={'Fecha': 'Fecha', 'value': 'Concentración (ug/m3)', 'variable': 'Contaminante'},
              template='plotly_dark')

# Mostrar el gráfico en Streamlit
st.write(fig.to_html(full_html=False), unsafe_allow_html=True)
