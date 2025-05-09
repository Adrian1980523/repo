# dashboard_incidencias.py
import pandas as pd
import streamlit as st
import altair as alt  # 👈 NUEVA LIBRERÍA

# Cargar datos
df = pd.read_csv('incidencias.csv', sep=';', encoding='latin1')

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

# 📊 Mejora de gráficas con Altair
st.markdown("### Incidencias por Estado")
estado_chart = (
    alt.Chart(df_filtrado)
    .mark_bar()
    .encode(
        x=alt.X('count():Q', title='Cantidad'),
        y=alt.Y('Estado:N', sort='-x', title='Estado'),
        color='Estado:N',
        tooltip=['Estado:N', 'count():Q']
    )
    .properties(height=300)
)
st.altair_chart(estado_chart, use_container_width=True)

st.markdown("### Incidencias por Persona Asignada")
persona_chart = (
    alt.Chart(df_filtrado)
    .mark_bar()
    .encode(
        x=alt.X('count():Q', title='Cantidad'),
        y=alt.Y('Persona asignada:N', sort='-x', title='Persona'),
        color='Persona asignada:N',
        tooltip=['Persona asignada:N', 'count():Q']
    )
    .properties(height=400)
)
st.altair_chart(persona_chart, use_container_width=True)

# Tabla de resultados
st.markdown("### Detalle de Incidencias")
st.dataframe(df_filtrado)



