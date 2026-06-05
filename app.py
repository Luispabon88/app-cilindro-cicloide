import streamlit as st
import sys
import subprocess

st.title("Diagnóstico de librerías")

st.write("Python:", sys.version)

try:
    import numpy
    st.success("NumPy instalado")
except Exception as e:
    st.error(f"NumPy error: {e}")

try:
    import pandas
    st.success("Pandas instalado")
except Exception as e:
    st.error(f"Pandas error: {e}")

try:
    import plotly
    st.success(f"Plotly instalado: {plotly.__version__}")
except Exception as e:
    st.error(f"Plotly error: {e}")
