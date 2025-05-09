import pandas as pd
import streamlit as st
import altair as alt

# Cargar datos
df = pd.read_csv('incidencias.csv', sep=';', encoding='latin1')

# Título del dashboard
st.title("📊 Dashboard de Incidencias")

# Filtros en la barra lateral
st.sidebar.header("Filtros")
tipo = st.sidebar.multiselect("Tipo de Incidencia", options=df['Tipo de Incidencia'].dropna().unique(), default=df['Tipo de Incidencia'].dropna().unique())
estado = st.sidebar.multiselect("Estado", options=df['Estado'].dropna().unique(), default=df['Estado'].dropna().unique())
proyecto = st.sidebar.multiselect("Nombre del Proyecto", options=df['Nombre del proyecto'].dropna().unique(), default=df['Nombre del proyecto'].dropna().unique())
asignado = st.sidebar.multiselect("Persona Asignada", options=df['Persona asignada'].dropna().unique(), default=df['Persona asignada'].dropna().unique())

# Aplicar filtros
df_filtrado = df[
    (df['Tipo de Incidencia'].isin(tipo)) &
    (df['Estado'].isin(estado)) &
    (df['Nombre del proyecto'].isin(proyecto)) &
    (df['Persona asignada'].isin(asignado))
]

# Métricas principales
st.markdown("### 📌 Métricas Generales")
col1, col2, col3 = st.columns(3)
col1.metric("Total de Incidencias", len(df_filtrado))
col2.metric("Tipos Distintos", df_filtrado['Tipo de Incidencia'].nunique())
col3.metric("Personas Involucradas", df_filtrado['Persona asignada'].nunique())

# Gráfica: Incidencias por Estado
st.markdown("### 📌 Incidencias por Estado")
estado_chart = (
    alt.Chart(df_filtrado)
    .mark_bar(color='steelblue')
    .encode(
        x=alt.X('count():Q', title='Cantidad'),
        y=alt.Y('Estado:N', sort='-x', title='Estado'),
        tooltip=['Estado', 'count()']
    )
    .properties(height=300)
)
st.altair_chart(estado_chart, use_container_width=True)

# Gráfica: Incidencias por Persona Asignada
st.markdown("### 📌 Incidencias por Persona Asignada")
asignado_chart = (
    alt.Chart(df_filtrado)
    .mark_bar(color='orange')
    .encode(
        x=alt.X('count():Q', title='Cantidad'),
        y=alt.Y('Persona asignada:N', sort='-x', title='Persona Asignada'),
        tooltip=['Persona asignada', 'count()']
    )
    .properties(height=400)
)
st.altair_chart(asignado_chart, use_container_width=True)

# Gráfica: Incidencias por Proyecto
st.markdown("### 📌 Incidencias por Proyecto")
proyecto_chart = (
    alt.Chart(df_filtrado)
    .mark_bar(color='seagreen')
    .encode(
        x=alt.X('count():Q', title='Cantidad'),
        y=alt.Y('Nombre del proyecto:N', sort='-x', title='Proyecto'),
        tooltip=['Nombre del proyecto', 'count()']
    )
    .properties(height=400)
)
st.altair_chart(proyecto_chart, use_container_width=True)

# Tabla final
st.markdown("### 📌 Detalle de Incidencias")
st.dataframe(df_filtrado)
