import os
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime

# ------------------- CONFIGURACIÓN INICIAL -------------------

# Nombre del archivo principal y carpeta de historial
archivo_csv = "historias_sprint.csv"
carpeta_historial = "historial"

# Crear carpeta de historial si no existe
if not os.path.exists(carpeta_historial):
    os.makedirs(carpeta_historial)

# Crear archivo CSV inicial si no existe
if not os.path.exists(archivo_csv):
    datos_ejemplo = {
        "id": [1, 2, 3, 4],
        "titulo": ["Login de usuario", "Registro de usuario", "Restablecer contraseña", "Perfil de usuario"],
        "estado": ["Done", "In Progress", "To Do", "Done"],
        "puntos": [5, 8, 3, 5],
        "avance_manual": [100, 50, 0, 100]
    }
    df_ejemplo = pd.DataFrame(datos_ejemplo)
    df_ejemplo.to_csv(archivo_csv, index=False)
    st.success("Archivo 'historias_sprint.csv' creado con datos de ejemplo.")

# ------------------- CARGA DE DATOS -------------------

# Cargar datos desde CSV principal
data = pd.read_csv(archivo_csv)

# Asegurar columna 'avance_manual'
if 'avance_manual' not in data.columns:
    data['avance_manual'] = 0

# ------------------- DASHBOARD -------------------

st.title("📊 Dashboard de Historias del Sprint")

# Edición del avance manual
st.subheader("✏️ Editar porcentaje de avance por historia")
data_editada = st.data_editor(
    data,
    use_container_width=True,
    num_rows="dynamic",
    column_order=["id", "titulo", "estado", "puntos", "avance_manual"],
    key="editor"
)

# Cálculo automático de avance restante
data_editada["avance_restante"] = 100 - data_editada["avance_manual"]

# Mostrar tabla con avance restante
st.subheader("📉 Avance restante por historia")
st.dataframe(data_editada[["id", "titulo", "estado", "puntos", "avance_manual", "avance_restante"]],
             use_container_width=True)

# ------------------- MÉTRICAS -------------------

# Avance automático basado en estado "Done"
total_puntos = data_editada["puntos"].sum()
puntos_done = data_editada[data_editada["estado"] == "Done"]["puntos"].sum()
avance_real = (puntos_done / total_puntos) * 100 if total_puntos > 0 else 0

# Avance manual promedio ponderado
avance_manual_total = (data_editada["avance_manual"] * data_editada["puntos"]).sum()
avance_manual = avance_manual_total / total_puntos if total_puntos > 0 else 0

# Mostrar métricas
col1, col2 = st.columns(2)
col1.metric("Avance por estado (automático)", f"{avance_real:.2f}%")
col2.metric("Avance manual promedio", f"{avance_manual:.2f}%")

# ------------------- VISUALIZACIÓN ACTUAL -------------------

st.subheader("📌 Puntos por Estado")
fig = px.bar(data_editada.groupby("estado")["puntos"].sum().reset_index(),
             x="estado", y="puntos", color="estado", title="Distribución de Puntos")
st.plotly_chart(fig)

# ------------------- GUARDAR CAMBIOS -------------------

if st.button("💾 Guardar cambios en CSV"):
    # Guardar archivo principal
    data_editada.to_csv(archivo_csv, index=False)

    # Guardar archivo histórico diario
    fecha = datetime.now().strftime("%Y-%m-%d")
    archivo_diario = os.path.join(carpeta_historial, f"avance_sprint_{fecha}.csv")
    data_editada.to_csv(archivo_diario, index=False)

    st.success(f"¡Datos guardados en '{archivo_csv}' y '{archivo_diario}'!")

# ------------------- GRÁFICO HISTÓRICO -------------------

st.subheader("📆 Evolución del avance manual (histórico diario)")

# Leer archivos del historial
historial_files = sorted([
    f for f in os.listdir(carpeta_historial)
    if f.startswith("avance_sprint_") and f.endswith(".csv")
])

historial_data = []

for archivo in historial_files:
    ruta = os.path.join(carpeta_historial, archivo)
    try:
        df_hist = pd.read_csv(ruta)
        fecha = archivo.replace("avance_sprint_", "").replace(".csv", "")
        total_puntos_hist = df_hist["puntos"].sum()
        avance_hist = (df_hist["avance_manual"] * df_hist["puntos"]).sum()
        promedio = avance_hist / total_puntos_hist if total_puntos_hist > 0 else 0
        historial_data.append({"fecha": fecha, "avance_manual": promedio})
    except Exception as e:
        st.warning(f"No se pudo leer {archivo}: {e}")

# Mostrar gráfico si hay datos
if historial_data:
    df_historial = pd.DataFrame(historial_data)
    df_historial["fecha"] = pd.to_datetime(df_historial["fecha"])
    df_historial = df_historial.sort_values("fecha")

    fig_linea = px.line(df_historial, x="fecha", y="avance_manual",
                        title="📈 Evolución del Avance Manual del Sprint",
                        markers=True,
                        labels={"avance_manual": "% Avance"})
    st.plotly_chart(fig_linea)
else:
    st.info("No hay datos históricos aún. Guarda al menos un día para comenzar.")
