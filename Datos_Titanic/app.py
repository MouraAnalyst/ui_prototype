import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.title("Titanic")

DATE_COLUMN = "date/time"
DATA_URL = "./titanic.csv"


@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    # Eliminar valores nulos de la columna 'age'
    if "age" in data.columns:
        data.dropna(subset=["age"], inplace=True)
    data["age"] = data["age"].astype(int)  # Convertir la edad a enteros
    return data


# Create a text element and let the reader know the data is loading.
data_load_state = st.text("Loading data...")
# Load 10,000 rows of data into the dataframe.
data = load_data(1000)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache_data)")

st.subheader("Raw data")
st.write(data)

st.subheader("Número de Supervivientes (o no)")

# Transformamos los datos para asignar etiquetas "No" y "Sí" a la columna 'survived'
data["survived_label"] = data["survived"].replace({0: "No", 1: "Sí"})

# Agrupamos los datos por edad y estado de supervivencia
grouped_data = data.groupby(["age", "survived_label"]).size().reset_index(name="count")

# Creamos el gráfico
chart = (
    alt.Chart(grouped_data)
    .mark_bar()
    .encode(
        x=alt.X("age:O", title="Edad"),  # Edad en el eje X
        y=alt.Y("count:Q", title="Total de Pasajeros"),  # Conteo en el eje Y
        color=alt.Color(
            "survived_label:N",
            title="Supervivencia",
            scale=alt.Scale(domain=["No", "Sí"], range=["red", "blue"]),
        ),
        tooltip=["age:O", "count:Q", "survived_label:N"],  # Información en el tooltip
    )
    .properties(
        width=800,
        height=400,
        title="Total de pasajeros por edad y estado de supervivencia",
    )
)

st.altair_chart(chart, use_container_width=True)
