# -*- coding: utf-8 -*-
"""
Created on Thu Aug 28 15:54:53 2025

@author: jahop
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import os
from pathlib import Path

st.set_page_config(page_title="Capital Humano - Evaluación y Talento", page_icon="💼", layout="wide")

# --- Función para cargar archivo automáticamente ---
def cargar_archivo_automatico(nombre_archivo, key_suffix):
    # Intentar varias ubicaciones posibles
    posibles_rutas = [
        nombre_archivo,  # Directorio actual
        Path(nombre_archivo),  # Usando pathlib
        Path(__file__).parent / nombre_archivo,  # Directorio del script
    ]
    
    for ruta in posibles_rutas:
        try:
            if os.path.exists(ruta):
                df = pd.read_excel(ruta)
                st.success(f"✅ Archivo '{ruta}' cargado automáticamente")
                return df
        except Exception as e:
            continue
    
    # Si no se encuentra en ninguna ruta, mostrar uploader
    st.info(f"📋 No se encontró el archivo '{nombre_archivo}'. Por favor, súbelo manualmente.")
    uploaded_file = st.file_uploader(f"📎 Sube archivo {nombre_archivo} (xlsx)", 
                                   type=["xlsx"], 
                                   key=f"upload_{key_suffix}")
    if uploaded_file:
        try:
            return pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
    
    return None

# --- Mostrar directorio actual para debugging ---
st.sidebar.write(f"Directorio actual: {os.getcwd()}")
st.sidebar.write(f"Archivos disponibles: {[f for f in os.listdir('.') if f.endswith('.xlsx')]}")

# --- Menú lateral ---
st.sidebar.title("Menú")
menu = st.sidebar.radio("Ir a:", ["Evaluación de Desempeño y Clima", "Gestión del Cambio", "Análisis del Talento"])

# --- 1. Evaluación de desempeño y clima laboral ---
if menu == "Evaluación de Desempeño y Clima":
    st.header("📊 Evaluación de Desempeño y Clima Laboral")
    st.write("Resultados de encuestas aplicadas al personal")

    df = cargar_archivo_automatico("evaluaciones.xlsx", "eval")
    
    if df is not None:
        st.dataframe(df, use_container_width=True)

        # Distribución de satisfacción
        if "Satisfacción" in df.columns:
            fig = px.histogram(df, x="Satisfacción", title="Distribución de Satisfacción")
            st.plotly_chart(fig, use_container_width=True)

        # Promedio de desempeño
        if "Desempeño" in df.columns:
            avg = df["Desempeño"].mean()
            st.metric("Promedio de Desempeño", f"{avg:.2f}")

# --- 2. Estrategias de gestión del cambio ---
elif menu == "Gestión del Cambio":
    st.header("🔄 Estrategias de Gestión del Cambio")
    st.write("Monitoreo de indicadores clave durante procesos de cambio organizacional.")

    df = cargar_archivo_automatico("indicadores.xlsx", "change")
    
    if df is not None:
        st.dataframe(df, use_container_width=True)

        if "Resistencia" in df.columns and "Comunicación" in df.columns:
            fig = px.scatter(df, x="Comunicación", y="Resistencia", color="Liderazgo", size="Avance",
                             title="Relación Comunicación vs Resistencia al Cambio")
            st.plotly_chart(fig, use_container_width=True)

# --- 3. Herramientas de análisis del talento ---
elif menu == "Análisis del Talento":
    st.header("🌟 Herramientas de Análisis del Talento")
    st.write("Identificación de alto potencial y necesidades de desarrollo.")

    # Carga automática del archivo talento.xlsx
    df = cargar_archivo_automatico("talento.xlsx", "talento")
    
    if df is not None:
        st.dataframe(df, use_container_width=True)

        if "Desempeño" in df.columns and "Potencial" in df.columns:
            fig = px.scatter(df, x="Desempeño", y="Potencial", color="Departamento",
                             title="Matriz 9-Box (Potencial vs Desempeño)")
            st.plotly_chart(fig, use_container_width=True)

        # Ranking de talento
        if "Desempeño" in df.columns and "Potencial" in df.columns:
            df["Score Talento"] = df["Desempeño"]*0.6 + df["Potencial"]*0.4
            df = df.sort_values("Score Talento", ascending=False)
            st.subheader("🏆 Ranking de Talento")
            st.dataframe(df[["Nombre", "Departamento", "Desempeño", "Potencial", "Score Talento"]])

# --- Instrucciones para el usuario ---
st.sidebar.markdown("---")
st.sidebar.info("""
**📋 Instrucciones:**
1. Coloca los archivos Excel en la misma carpeta que esta aplicación
2. Nombres requeridos:
   - `talento.xlsx`
   - `evaluaciones.xlsx`
   - `indicadores.xlsx`
3. La aplicación los cargará automáticamente
""")
