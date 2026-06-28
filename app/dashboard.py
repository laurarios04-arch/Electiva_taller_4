import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------------
# Configuración de la página
# -------------------------------------------------------

st.set_page_config(
    page_title="Dashboard Turismo Boyacá",
    page_icon="🌎",
    layout="wide"
)

st.title("🌎 Dashboard Analítico - Turismo Boyacá")

st.markdown(
"""
Este dashboard consume información proveniente del Data Lake
utilizando el archivo **turismo.parquet** generado en el proceso ETL.
"""
)

# -------------------------------------------------------
# Lectura del Data Lake
# -------------------------------------------------------

@st.cache_data
def cargar_datos():

    df = pd.read_parquet("outputs/turismo.parquet")

    return df

df = cargar_datos()
print(df.columns)

# -------------------------------------------------------
# Información del dataset
# -------------------------------------------------------

st.sidebar.header("Información")

st.sidebar.write(f"Registros: {df.shape[0]}")
st.sidebar.write(f"Columnas: {df.shape[1]}")

# -------------------------------------------------------
# Filtros
# -------------------------------------------------------

st.sidebar.header("Filtros")

motivos = sorted(df["MOTIVO DEL VIAJE"].dropna().unique())

motivo = st.sidebar.selectbox(
    "Motivo del viaje",
    ["Todos"] + list(motivos)
)

sexo = st.sidebar.selectbox(
    "Sexo",
    ["Todos"] + sorted(df["SEXO"].dropna().unique())
)

pais = st.sidebar.selectbox(
    "País",
    ["Todos"] + sorted(df["PAIS DE PROCEDENCIA"].dropna().unique())
)

# -------------------------------------------------------
# Aplicar filtros
# -------------------------------------------------------

df_filtrado = df.copy()

if motivo != "Todos":

    df_filtrado = df_filtrado[
        df_filtrado["MOTIVO DEL VIAJE"] == motivo
    ]

if sexo != "Todos":

    df_filtrado = df_filtrado[
        df_filtrado["SEXO"] == sexo
    ]

if pais != "Todos":

    df_filtrado = df_filtrado[
        df_filtrado["PAIS DE PROCEDENCIA"] == pais
    ]

# -------------------------------------------------------
# KPIs
# -------------------------------------------------------

st.subheader("Indicadores generales")

total_registros = len(df_filtrado)

total_visitantes = df_filtrado["CANTIDAD DE VIAJEROS"].sum()

promedio_satisfaccion = (
    df_filtrado["RESULTADO SATISFACCIÓN"].mean()
)

promedio_permanencia = (
    df_filtrado["TIEMPO DE PERMANENCIA EN DIAS"].mean()
)

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Registros",
    f"{total_registros:,}"
)

c2.metric(
    "Visitantes",
    f"{int(total_visitantes):,}"
)

c3.metric(
    "Satisfacción",
    round(promedio_satisfaccion,2)
)

c4.metric(
    "Permanencia promedio",
    round(promedio_permanencia,2)
)

st.divider()

# -------------------------------------------------------
# Gráfico 1
# -------------------------------------------------------

col1,col2 = st.columns(2)

with col1:

    destinos = (
        df_filtrado["CIUDAD DE DESTINO 1"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    destinos.columns=[
        "Destino",
        "Visitantes"
    ]

    fig = px.bar(
        destinos,
        x="Destino",
        y="Visitantes",
        color="Visitantes",
        title="Top 10 destinos turísticos"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -------------------------------------------------------
# Gráfico 2
# -------------------------------------------------------

with col2:

    motivos = (
        df_filtrado["MOTIVO DEL VIAJE"]
        .value_counts()
        .reset_index()
    )

    motivos.columns=[
        "Motivo",
        "Cantidad"
    ]

    fig = px.pie(
        motivos,
        names="Motivo",
        values="Cantidad",
        title="Motivo del viaje"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -------------------------------------------------------
# Segunda fila
# -------------------------------------------------------

col3,col4 = st.columns(2)

with col3:

    procedencia = (
        df_filtrado["CIUDAD DE PROCEDENCIA"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    procedencia.columns=[
        "Ciudad",
        "Visitantes"
    ]

    fig = px.bar(
        procedencia,
        y="Ciudad",
        x="Visitantes",
        orientation="h",
        color="Visitantes",
        title="Top ciudades de procedencia"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col4:

    alojamiento = (
        df_filtrado["TIPO ALOJAMIENTO"]
        .value_counts()
        .reset_index()
    )

    alojamiento.columns=[
        "Alojamiento",
        "Cantidad"
    ]

    fig = px.bar(
        alojamiento,
        x="Alojamiento",
        y="Cantidad",
        color="Cantidad",
        title="Tipo de alojamiento"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -------------------------------------------------------
# Tercera fila
# -------------------------------------------------------

st.subheader("Transporte utilizado")

transporte = (
    df_filtrado["TIPO TRANSPORTE"]
    .value_counts()
    .reset_index()
)

transporte.columns=[
    "Transporte",
    "Cantidad"
]

fig = px.bar(
    transporte,
    x="Transporte",
    y="Cantidad",
    color="Cantidad"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------------
# Tabla interactiva
# -------------------------------------------------------

st.subheader("Datos filtrados")

st.dataframe(
    df_filtrado,
    use_container_width=True
)

# -------------------------------------------------------
# Descarga
# -------------------------------------------------------

csv = df_filtrado.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Descargar datos filtrados",
    data=csv,
    file_name="turismo_filtrado.csv",
    mime="text/csv"
)

# -------------------------------------------------------
# Pie de página
# -------------------------------------------------------

st.markdown("---")

st.caption(
"""
Especialización en Analítica Estratégica de Datos

Módulo 3 - Contenedores y Entornos Reproducibles

Dashboard desarrollado con Streamlit y Docker.
"""
)