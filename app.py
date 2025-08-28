# -*- coding: utf-8 -*-
"""
Created on Thu Aug 28 15:54:53 2025

@author: jahop
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Capital Humano - Evaluación y Talento", page_icon="💼", layout="wide")

# --- Menú lateral ---
st.sidebar.title("Menú")
menu = st.sidebar.radio("Ir a:", ["Evaluación de Desempeño y Clima", "Gestión del Cambio", "Análisis del Talento"])

# --- Función para cargar Excel automáticamente ---
def cargar_excel(uploaded_file, default_file):
    if uploaded_file is not None:
        return pd.read_excel(uploaded_file)
    elif os.path.exists(default_file):
        return pd.read_excel(default_file)
    else:
        st.warning("⚠️ No se encontró archivo por defecto.")
        return None

# --- 1. Evaluación de desempeño y clima laboral ---
if menu == "Evaluación de Desempeño y Clima":
    st.header("📊 Evaluación de Desempeño y Clima Laboral")
    st.write("Resultados de encuestas aplicadas al personal")

    uploaded_file = st.file_uploader("📎 Sube archivo con evaluaciones (xlsx)", type=["xlsx"], key="eval")
    df = cargar_excel(uploaded_file, "evaluacion.xlsx")

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

    uploaded_file = st.file_uploader("📎 Sube archivo con indicadores (xlsx)", type=["xlsx"], key="change")
    df = cargar_excel(uploaded_file, "cambio.xlsx")

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

    uploaded_file = st.file_uploader("📎 Sube base de empleados (xlsx)", type=["xlsx"], key="talento")
    df = cargar_excel(uploaded_file, "talento.xlsx")

    if df is not None:
        st.dataframe(df, use_container_width=True)

        # 📊 Matriz 9-Box
        if "Desempeño" in df.columns and "Potencial" in df.columns:
            fig = px.scatter(df, x="Desempeño", y="Potencial", color="Departamento",
                             title="Matriz 9-Box (Potencial vs Desempeño)")
            st.plotly_chart(fig, use_container_width=True)

        # 🏆 Ranking de talento
        if "Habilidades" in df.columns:
            df["Score Talento"] = df["Desempeño"]*0.6 + df["Potencial"]*0.4
            df = df.sort_values("Score Talento", ascending=False)
            st.subheader("🏆 Ranking de Talento")
            st.dataframe(df[["Nombre", "Departamento", "Desempeño", "Potencial", "Score Talento"]])

        # --- 📊 Dashboard dinámico ---
        st.subheader("📈 Dashboard del Talento")

        col1, col2 = st.columns(2)

        # Distribución por departamento
        with col1:
            fig1 = px.histogram(df, x="Departamento", title="Distribución por Departamento")
            st.plotly_chart(fig1, use_container_width=True)

        # Promedio de desempeño y potencial
        with col2:
            resumen = df.groupby("Departamento")[["Desempeño", "Potencial"]].mean().reset_index()
            fig2 = px.bar(resumen, x="Departamento", y=["Desempeño", "Potencial"],
                          barmode="group", title="Promedios por Departamento")
            st.plotly_chart(fig2, use_container_width=True)

        # Estadísticos generales
        st.subheader("📌 Estadísticos Generales")
        st.write(df[["Desempeño", "Potencial", "Score Talento"]].describe())
