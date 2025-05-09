# dashboard_incidencias.py
import pandas as pd
import streamlit as st

# Cargar datos
df = pd.read_csv('/Users/luisadrianlopezmesa/Documents/Curso analisis y visualizacion de datos/incidencias.csv', sep=';', encoding='latin1')  # Usa sep='\t' si el CSV está separado por tabulaciones

print(df.columns.tolist())
print(df.head())

st.title("📊 Dashboard de Incidencias")

# Filtros
st.sidebar.header("Filtros")
tipo = st.sidebar.multiselect("Tipo de Incidencia", options=df['Tipo de Incidencia'].unique(), default=df['Tipo de Incidencia'].unique())
estado = st.sidebar.multiselect("Estado", options=df['Estado'].dropna().unique(), default=df['Estado'].dropna().unique())
asignado = st.sidebar.multiselect("Persona Asignada", options=df['Persona asignada'].dropna().unique(), default=df['Persona asignada'].dropna().unique())

# Aplicar filtros
df_filtrado = df[
    (df['Tipo de Incidencia'].isin(tipo)) &
    (df['Estado'].isin(estado)) &
    (df['Persona asignada'].isin(asignado))
]

# Métricas principales
st.markdown("### Métricas Generales")
col1, col2, col3 = st.columns(3)
col1.metric("Total de Incidencias", len(df_filtrado))
col2.metric("Tipos Distintos", df_filtrado['Tipo de Incidencia'].nunique())
col3.metric("Personas Involucradas", df_filtrado['Persona asignada'].nunique())

# Gráficas
st.markdown("### Incidencias por Estado")
st.bar_chart(df_filtrado['Estado'].value_counts())

st.markdown("### Incidencias por Persona Asignada")
st.bar_chart(df_filtrado['Persona asignada'].value_counts())

# Tabla de resultados
st.markdown("### Detalle de Incidencias")
st.dataframe(df_filtrado)


