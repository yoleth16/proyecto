# -*- coding: utf-8 -*-
"""codigo proyec

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ndOIGFGF8HqN5IW_tEaDht2TSiqxHh7d
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from Bio import SeqIO
from Bio.SeqUtils import GC

st.set_page_config(page_title="Análisis de Secuencias con Biopython", layout="wide")
st.title("🔬 Análisis de Secuencias con Biopython")
st.markdown("""
Este dashboard permite analizar y visualizar datos relacionados con secuencias biológicas.
Utiliza las herramientas disponibles para interactuar con tus datos.
""")

def process_fasta_biopython(file):
    try:
        sequences = list(SeqIO.parse(file, "fasta"))
        if not sequences:
            st.sidebar.error("El archivo FASTA no contiene secuencias válidas.")
            return None
        st.sidebar.success(f"Archivo FASTA cargado correctamente: {len(sequences)} secuencias.")
        return sequences
    except Exception as e:
        st.sidebar.error("Error al procesar el archivo FASTA.")
        return None

def process_csv(file):
    try:
        data = pd.read_csv(file)
        st.sidebar.success("Archivo CSV procesado correctamente.")
        return data
    except Exception as e:
        st.sidebar.error("Error al procesar el archivo CSV.")
        return None

def calculate_gc_content(sequences):
    gc_contents = [GC(record.seq) for record in sequences]
    return gc_contents

def find_motifs(sequences, motifs):
    motif_counts = {motif: 0 for motif in motifs}
    for record in sequences:
        seq = str(record.seq).upper()
        for motif in motifs:
            motif_counts[motif] += seq.count(motif)
    return motif_counts

st.sidebar.title("📂 Carga de Datos y Configuración")
uploaded_file = st.sidebar.file_uploader("Sube tu archivo FASTA o CSV", type=["fasta", "csv"])

data = None
sequences = None

if uploaded_file:
    if uploaded_file.name.endswith(".fasta"):
        sequences = process_fasta_biopython(uploaded_file)
    elif uploaded_file.name.endswith(".csv"):
        data = process_csv(uploaded_file)

if sequences:
    st.write(f"### Número de secuencias cargadas: {len(sequences)}")
    st.text("Ejemplo de secuencia:")
    st.code(f"> {sequences[0].id}\n{str(sequences[0].seq)}")

    st.header("Análisis del Contenido GC")
    gc_contents = calculate_gc_content(sequences)
    st.write("### Distribución del contenido de GC en las secuencias")
    fig = px.histogram(gc_contents, nbins=20, labels={'value': "Contenido GC (%)", 'count': "Frecuencia"},
                       title="Distribución de Contenido GC", color_discrete_sequence=['lightblue'])
    st.plotly_chart(fig)

    st.header("Búsqueda de Motivos")
    st.markdown("Busca motivos comunes en las secuencias (ej. ATG, TATA, CCGG).")
    user_motifs = st.text_input("Introduce los motivos separados por comas (ej. ATG, TATA):", value="ATG, TATA, CCGG")
    if user_motifs:
        motifs = [motif.strip() for motif in user_motifs.split(",")]
        motif_counts = find_motifs(sequences, motifs)
        st.write("### Frecuencia de los motivos")
        st.table(pd.DataFrame(list(motif_counts.items()), columns=["Motivo", "Frecuencia"]))

if data is not None:
    st.write("### Vista previa de los datos")
    st.dataframe(data)
    st.write("### Estadísticas descriptivas")
    st.dataframe(data.describe())

st.header("Herramientas Interactivas")
selected_tool = st.radio("Elige una herramienta para analizar tus secuencias:",
                         options=["Alineación", "Predicción de estructuras", "Análisis estadístico"])

if selected_tool == "Alineación":
    st.subheader("Alineación de Secuencia")
    st.text("Ejemplo: Resultado del algoritmo Needleman-Wunsch (placeholder).")
    st.code("""
    Seq1: AGCTAGC
    Seq2: AGCTG-C
    Puntuación de alineación: 92
    """)
elif selected_tool == "Predicción de estructuras":
    st.subheader("Predicción de Estructuras Proteicas")
    st.text("Estructura 3D prevista (Placeholder):")
    st.image("https://via.placeholder.com/300", caption="Estructura 3D prevista")
elif selected_tool == "Análisis estadístico":
    st.subheader("Análisis de Correlación Estadística")
    example_data = {"Contenido": ["Contenido GC", "Contenido AT", "Longitud de la secuencia"],
                    "Correlación con el objetivo": [0.87, -0.56, 0.45]}
    st.table(pd.DataFrame(example_data))

if data is not None:
    st.sidebar.markdown("---")
    st.sidebar.write("📥 Descarga de Resultados")
    csv = data.to_csv(index=False)
    st.sidebar.download_button(label="Descargar resultados", data=csv, file_name="resultados.csv", mime="text/csv")

st.sidebar.markdown("---")
st.sidebar.write("💻 Desarrollado por [Yoleth Barrios y Lucero Ramos]")