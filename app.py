import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("Módulo 1: Predicción del movimiento del cilindro")

st.markdown("""
Este módulo predice si el cilindro **sube o baja la rampa** al variar la masa colgante,
el número de barras y la posición radial de las barras.
""")

# -----------------------------
# Entradas del sistema
# -----------------------------

st.sidebar.header("Parámetros del cilindro")

M = st.sidebar.number_input("Masa del cilindro M (kg)", min_value=0.001, value=0.500, step=0.010)
R = st.sidebar.number_input("Radio externo del cilindro R (m)", min_value=0.001, value=0.050, step=0.001)

st.sidebar.header("Parámetros de las barras")

N = st.sidebar.number_input("Número de barras N", min_value=0, value=4, step=1)
mn = st.sidebar.number_input("Masa promedio de cada barra mn (kg)", min_value=0.0, value=0.020, step=0.001)
Rx = st.sidebar.number_input("Radio de colocación de barras Rx (m)", min_value=0.0, value=0.030, step=0.001)

st.sidebar.header("Sistema en la rampa")

mc = st.sidebar.number_input("Masa colgante mc (kg)", min_value=0.0, value=0.100, step=0.001)
theta_deg = st.sidebar.number_input("Ángulo de la rampa θ (grados)", min_value=0.0, max_value=90.0, value=10.0, step=0.5)
g = st.sidebar.number_input("Gravedad g (m/s²)", min_value=0.0, value=9.81, step=0.01)

st.sidebar.header("Simulación temporal")

t_max = st.sidebar.number_input("Tiempo de simulación (s)", min_value=0.1, value=5.0, step=0.1)
x0 = st.sidebar.number_input("Posición inicial sobre la rampa x₀ (m)", value=0.0, step=0.01)
v0 = st.sidebar.number_input("Velocidad inicial v₀ (m/s)", value=0.0, step=0.01)

# -----------------------------
# Cálculo físico
# -----------------------------

theta = np.radians(theta_deg)

numerador = g * ((M + N * mn) * np.sin(theta) - mc)

denominador = (3/2) * M + N * mn * (1 + (Rx**2 / R**2)) + mc

a = numerador / denominador

# -----------------------------
# Predicción del sentido
# -----------------------------

tolerancia = 1e-3

if a > tolerancia:
    estado = "El cilindro baja la rampa"
elif a < -tolerancia:
    estado = "El cilindro sube la rampa"
else:
    estado = "El sistema está casi en equilibrio"

# -----------------------------
# Resultados principales
# -----------------------------

st.subheader("Resultado de la predicción")

st.metric("Aceleración del cilindro", f"{a:.4f} m/s²")
st.success(estado)

st.write("Masa total del cilindro con barras:")

masa_total = M + N * mn
st.metric("Masa total", f"{masa_total:.4f} kg")

I_total = 0.5 * M * R**2 + N * mn * Rx**2
st.metric("Momento de inercia total", f"{I_total:.6f} kg·m²")

# -----------------------------
# Movimiento
# -----------------------------

t = np.linspace(0, t_max, 300)

x = x0 + v0 * t + 0.5 * a * t**2
v = v0 + a * t

df = pd.DataFrame({
    "t (s)": t,
    "x (m)": x,
    "v (m/s)": v
})

st.subheader("Tabla de datos simulados")
st.dataframe(df)

# -----------------------------
# Gráfica posición-tiempo
# -----------------------------

st.subheader("Posición del cilindro en función del tiempo")

fig1, ax1 = plt.subplots()
ax1.plot(t, x)
ax1.set_xlabel("Tiempo (s)")
ax1.set_ylabel("Posición sobre la rampa (m)")
ax1.grid(True)

st.pyplot(fig1)

# -----------------------------
# Gráfica velocidad-tiempo
# -----------------------------

st.subheader("Velocidad del cilindro en función del tiempo")

fig2, ax2 = plt.subplots()
ax2.plot(t, v)
ax2.set_xlabel("Tiempo (s)")
ax2.set_ylabel("Velocidad (m/s)")
ax2.grid(True)

st.pyplot(fig2)

# -----------------------------
# Explicación física
# -----------------------------

st.subheader("Interpretación física")

st.markdown(f"""
La aceleración calculada fue:

**a = {a:.4f} m/s²**

El término que decide el sentido del movimiento es:

\[
(M+Nm_n)\sin(\\theta)-m_c
\]

Para este caso:

\[
({M:.3f}+{N}({mn:.3f}))\sin({theta_deg:.2f}^\circ)-{mc:.3f}
\]

Si este valor es positivo, el peso del cilindro sobre la rampa domina y el cilindro baja.  
Si es negativo, la masa colgante domina y el cilindro sube.
""")
