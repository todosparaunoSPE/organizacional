# -*- coding: utf-8 -*-
"""
Created on Thu Aug 28 15:54:53 2025

@author: jahop
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Capital Humano - Evaluación y Talento", page_icon="💼", layout="wide")

# --- Información personal ---
st.sidebar.markdown("---")
st.sidebar.subheader("👤 Información de Contacto")
st.sidebar.write("**Javier Horacio Pérez Ricárdez**")
st.sidebar.write(f"📅 {datetime.now().strftime('%d/%m/%Y')}")
st.sidebar.write("📱 +52 56 1056 4095")
st.sidebar.write("📧 jhperez@email.com")
st.sidebar.markdown("---")

# --- Datos de ejemplo integrados ---
@st.cache_data
def generar_datos_evaluacion():
    np.random.seed(42)
    data = {
        'Empleado': [f'EMP{i:03d}' for i in range(1, 51)],
        'Departamento': np.random.choice(['Ventas', 'TI', 'RH', 'Finanzas', 'Operaciones'], 50),
        'Satisfacción': np.random.randint(1, 11, 50),
        'Desempeño': np.random.randint(60, 101, 50),
        'Comunicación': np.random.randint(1, 11, 50),
        'Liderazgo': np.random.randint(1, 11, 50)
    }
    return pd.DataFrame(data)

@st.cache_data
def generar_datos_gestion_cambio():
    np.random.seed(42)
    data = {
        'Proyecto': [f'Proyecto {i}' for i in range(1, 21)],
        'Comunicación': np.random.randint(5, 11, 20),
        'Resistencia': np.random.randint(1, 8, 20),
        'Liderazgo': np.random.randint(6, 11, 20),
        'Avance': np.random.randint(30, 101, 20),
        'Éxito': np.random.choice(['Alto', 'Medio', 'Bajo'], 20, p=[0.4, 0.4, 0.2])
    }
    return pd.DataFrame(data)

@st.cache_data
def generar_datos_talento():
    np.random.seed(42)
    data = {
        'Nombre': [f'Empleado {i}' for i in range(1, 31)],
        'Departamento': np.random.choice(['Ventas', 'TI', 'RH', 'Finanzas', 'Operaciones'], 30),
        'Desempeño': np.random.randint(70, 101, 30),
        'Potencial': np.random.randint(60, 101, 30),
        'Habilidades': np.random.randint(1, 11, 30),
        'Experiencia': np.random.randint(1, 16, 30),
        'Salario': np.random.randint(30000, 100001, 30)
    }
    return pd.DataFrame(data)

# --- Menú lateral ---
st.sidebar.title("Menú")
menu = st.sidebar.radio("Ir a:", ["Evaluación de Desempeño y Clima", "Gestión del Cambio", "Análisis del Talento"])

# --- Header principal con información ---
col1, col2 = st.columns([3, 1])
with col1:
    st.title("💼 Dashboard de Capital Humano")
    st.write("Sistema integral de gestión del talento humano")
with col2:
    st.write(f"**Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    st.write("**Desarrollado por:** Javier H. Pérez R.")

# --- 1. Evaluación de desempeño y clima laboral ---
if menu == "Evaluación de Desempeño y Clima":
    st.header("📊 Evaluación de Desempeño y Clima Laboral")
    st.write("Resultados de encuestas aplicadas al personal")
    
    # Cargar datos de ejemplo
    df = generar_datos_evaluacion()
    
    st.success("✅ Datos de evaluación cargados automáticamente")
    st.dataframe(df, use_container_width=True)

    # Distribución de satisfacción
    if "Satisfacción" in df.columns:
        fig = px.histogram(df, x="Satisfacción", title="Distribución de Satisfacción", 
                          nbins=10, color_discrete_sequence=['#FF6B6B'])
        fig.update_layout(xaxis_title="Nivel de Satisfacción", yaxis_title="Cantidad de Empleados")
        st.plotly_chart(fig, use_container_width=True)

    # Promedio de desempeño
    if "Desempeño" in df.columns:
        col1, col2, col3 = st.columns(3)
        with col1:
            avg_desempeño = df["Desempeño"].mean()
            st.metric("📈 Promedio de Desempeño", f"{avg_desempeño:.1f}")
        with col2:
            avg_satisfaccion = df["Satisfacción"].mean()
            st.metric("😊 Satisfacción Promedio", f"{avg_satisfaccion:.1f}/10")
        with col3:
            avg_comunicacion = df["Comunicación"].mean()
            st.metric("💬 Comunicación Promedio", f"{avg_comunicacion:.1f}/10")

    # Análisis por departamento
    st.subheader("📋 Análisis por Departamento")
    dept_stats = df.groupby('Departamento').agg({
        'Desempeño': 'mean',
        'Satisfacción': 'mean',
        'Comunicación': 'mean'
    }).round(1)
    
    st.dataframe(dept_stats, use_container_width=True)

# --- 2. Estrategias de gestión del cambio ---
elif menu == "Gestión del Cambio":
    st.header("🔄 Estrategias de Gestión del Cambio")
    st.write("Monitoreo de indicadores clave durante procesos de cambio organizacional.")
    
    # Cargar datos de ejemplo
    df = generar_datos_gestion_cambio()
    
    st.success("✅ Datos de gestión del cambio cargados automáticamente")
    st.dataframe(df, use_container_width=True)

    # Gráfico de dispersión
    if "Resistencia" in df.columns and "Comunicación" in df.columns:
        fig = px.scatter(df, x="Comunicación", y="Resistencia", color="Liderazgo", 
                        size="Avance", hover_name="Proyecto", title="Relación Comunicación vs Resistencia al Cambio",
                        color_continuous_scale='Viridis')
        fig.update_layout(xaxis_title="Nivel de Comunicación", yaxis_title="Nivel de Resistencia")
        st.plotly_chart(fig, use_container_width=True)

    # Métricas clave
    st.subheader("📊 Métricas de Gestión del Cambio")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Comunicación Promedio", f"{df['Comunicación'].mean():.1f}/10")
    with col2:
        st.metric("Resistencia Promedio", f"{df['Resistencia'].mean():.1f}/10")
    with col3:
        st.metric("Liderazgo Promedio", f"{df['Liderazgo'].mean():.1f}/10")
    with col4:
        st.metric("Avance Promedio", f"{df['Avance'].mean():.1f}%")

# --- 3. Herramientas de análisis del talento ---
elif menu == "Análisis del Talento":
    st.header("🌟 Herramientas de Análisis del Talento")
    st.write("Identificación de alto potencial y necesidades de desarrollo.")
    
    # Cargar datos de ejemplo
    df = generar_datos_talento()
    
    st.success("✅ Datos de talento cargados automáticamente")
    st.dataframe(df, use_container_width=True)

    # Matriz 9-Box
    if "Desempeño" in df.columns and "Potencial" in df.columns:
        fig = px.scatter(df, x="Desempeño", y="Potencial", color="Departamento",
                         title="Matriz 9-Box (Potencial vs Desempeño)",
                         hover_name="Nombre", size="Experiencia",
                         color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_layout(xaxis_title="Desempeño (%)", yaxis_title="Potencial (%)")
        st.plotly_chart(fig, use_container_width=True)

    # Ranking de talento
    if "Desempeño" in df.columns and "Potencial" in df.columns:
        df["Score Talento"] = df["Desempeño"] * 0.6 + df["Potencial"] * 0.4
        df = df.sort_values("Score Talento", ascending=False)
        
        st.subheader("🏆 Ranking de Talento")
        
        # Top 5 talentos
        st.write("**Top 5 Talentos:**")
        top_5 = df.head(5)[["Nombre", "Departamento", "Desempeño", "Potencial", "Score Talento"]]
        st.dataframe(top_5, use_container_width=True)
        
        # Ranking completo
        st.write("**Ranking Completo:**")
        ranking_completo = df[["Nombre", "Departamento", "Desempeño", "Potencial", "Score Talento", "Habilidades", "Experiencia"]]
        st.dataframe(ranking_completo, use_container_width=True)

    # Análisis por departamento
    st.subheader("📊 Estadísticas por Departamento")
    dept_stats = df.groupby('Departamento').agg({
        'Desempeño': 'mean',
        'Potencial': 'mean',
        'Habilidades': 'mean',
        'Experiencia': 'mean',
        'Score Talento': 'mean'
    }).round(1)
    
    st.dataframe(dept_stats, use_container_width=True)

# --- Información adicional ---
st.sidebar.markdown("---")
st.sidebar.info("""
**ℹ️ Información:**
- Todos los datos son de ejemplo generados automáticamente
- No es necesario subir archivos Excel
- Los datos se resetearán al recargar la página
""")

# --- Agregar botones de acción ---
st.sidebar.markdown("---")
st.sidebar.subheader("🔧 Acciones")
if st.sidebar.button("🔄 Actualizar Datos"):
    st.cache_data.clear()
    st.rerun()

if st.sidebar.button("📊 Ver Estadísticas Generales"):
    st.sidebar.write("**Estadísticas Globales:**")
    st.sidebar.write(f"- Total empleados: 50")
    st.sidebar.write(f"- Total proyectos: 20")
    st.sidebar.write(f"- Departamentos: 5")

# --- Footer con información de contacto ---
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)
with footer_col1:
    st.write("**Desarrollado por:**")
    st.write("Javier Horacio Pérez Ricárdez")
with footer_col2:
    st.write("**Contacto:**")
    st.write("📱 +52 56 1056 4095")
with footer_col3:
    st.write("**Fecha:**")
    st.write(datetime.now().strftime("%d/%m/%Y %H:%M"))
