import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("Simulador de Cilindro en Rampa")
st.subheader("Módulo 1: Predicción teórica")

g = 9.81

st.sidebar.header("Parámetros del experimento")

m = st.sidebar.number_input("Masa del cilindro (kg)", min_value=0.01, value=0.20, step=0.01)
R = st.sidebar.number_input("Radio del cilindro (m)", min_value=0.001, value=0.03, step=0.001)
theta_deg = st.sidebar.slider("Ángulo de la rampa (°)", 1, 45, 10)
L = st.sidebar.number_input("Longitud recorrida sobre la rampa (m)", min_value=0.01, value=1.00, step=0.05)

tipo = st.sidebar.selectbox(
    "Tipo de cilindro",
    ["Cilindro macizo", "Aro delgado", "Esfera maciza"]
)

theta = np.radians(theta_deg)

if tipo == "Cilindro macizo":
    k = 1/2
elif tipo == "Aro delgado":
    k = 1
elif tipo == "Esfera maciza":
    k = 2/5

I = k * m * R**2
a = g * np.sin(theta) / (1 + I/(m*R**2))

t_final = np.sqrt(2*L/a)
v_final = a * t_final
omega_final = v_final / R

st.header("Resultados teóricos")

col1, col2, col3 = st.columns(3)

col1.metric("Aceleración", f"{a:.3f} m/s²")
col2.metric("Tiempo de descenso", f"{t_final:.3f} s")
col3.metric("Velocidad final", f"{v_final:.3f} m/s")

st.write(f"Momento de inercia: **{I:.6f} kg·m²**")
st.write(f"Velocidad angular final: **{omega_final:.3f} rad/s**")

st.header("Gráficas de predicción")

t = np.linspace(0, t_final, 200)
s = 0.5 * a * t**2
v = a * t

df = pd.DataFrame({
    "Tiempo (s)": t,
    "Posición sobre la rampa (m)": s,
    "Velocidad (m/s)": v
})

fig1 = px.line(df, x="Tiempo (s)", y="Posición sobre la rampa (m)",
               title="Posición vs tiempo")
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.line(df, x="Tiempo (s)", y="Velocidad (m/s)",
               title="Velocidad vs tiempo")
st.plotly_chart(fig2, use_container_width=True)

st.header("Pregunta de predicción")

respuesta = st.radio(
    "Antes de realizar el experimento, ¿qué esperas observar?",
    [
        "El cilindro aumenta su velocidad de forma uniforme",
        "El cilindro baja con velocidad constante",
        "El cilindro se detiene antes de llegar al final",
        "El movimiento no depende del ángulo"
    ]
)

if st.button("Validar predicción"):
    if respuesta == "El cilindro aumenta su velocidad de forma uniforme":
        st.success("Correcto. Para este modelo ideal, la aceleración es constante.")
    else:
        st.warning("Revisa el modelo teórico: en rodadura sin deslizamiento sobre una rampa ideal, el cilindro tiene aceleración constante.")
