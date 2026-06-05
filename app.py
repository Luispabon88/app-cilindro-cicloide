import streamlit as st

st.title("Simulador de Cilindro en Rampa")

angulo = st.slider(
    "Ángulo de la rampa (°)",
    0,
    45,
    15
)

st.write("Ángulo seleccionado:", angulo)
