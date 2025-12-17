# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st
import numpy as np

st.set_page_config(
    page_title="Mi Landing con Streamlit",
    page_icon="🚀",
    layout="wide"
)

# ---------- CSS GLOBAL ----------
st.markdown("""
<style>
/* Ajustes generales */
.block-container { padding-top: 2.5rem; max-width: 1200px; }
h1, h2, h3 { letter-spacing: -0.5px; }

/* Hero */
.hero {
  padding: 28px;
  border-radius: 18px;
  background: linear-gradient(135deg, rgba(255,122,0,0.18), rgba(255,255,255,0.02));
  border: 1px solid rgba(255,255,255,0.08);
  margin-bottom: 18px;
}
.hero-title { font-size: 42px; font-weight: 800; margin: 0; }
.hero-sub { margin-top: 8px; opacity: 0.85; font-size: 16px; line-height: 1.4; }
.hero-cta {
  display: inline-block;
  margin-top: 14px;
  padding: 10px 14px;
  border-radius: 12px;
  background: rgba(255,122,0,0.95);
  color: #111 !important;
  font-weight: 700;
  text-decoration: none;
}

/* Cards */
.card {
  padding: 16px;
  border-radius: 16px;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  height: 100%;
}
.card h3 { margin: 0 0 6px 0; font-size: 18px; }
.card p { margin: 0; opacity: 0.8; }

/* Secciones */
.section {
  margin-top: 18px;
  padding: 18px;
  border-radius: 18px;
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(255,255,255,0.08);
}
.section-title { margin: 0 0 10px 0; font-size: 20px; }

/* Tabla HTML bonita */
.table-wrap {
  overflow-x: auto;
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}
thead th {
  text-align: left;
  padding: 10px;
  background: rgba(255,122,0,0.12);
  border-bottom: 1px solid rgba(255,255,255,0.10);
}
tbody td {
  padding: 10px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}
tbody tr:hover {
  background: rgba(255,255,255,0.03);
}
</style>
""", unsafe_allow_html=True)

# ---------- HERO (HTML) ----------
st.markdown("""
<div class="hero">
  <div class="hero-title">Welcome to Streamlit, pero con estilo</div>
  <div class="hero-sub">
    Esto es una “landing” montada con HTML/CSS alrededor, pero el gráfico sigue siendo 100% nativo de Streamlit.
  </div>
  <a class="hero-cta" href="#dashboard">Ver dashboard</a>
</div>
""", unsafe_allow_html=True)

# ---------- CARDS (layout Streamlit + contenido HTML) ----------
c1, c2, c3 = st.columns(3, gap="large")

with c1:
    st.markdown("""
    <div class="card">
      <h3>Rápido</h3>
      <p>Layout con columnas + CSS inyectado.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
      <h3>Nativo</h3>
      <p>El chart es el de Streamlit (no un iframe).</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="card">
      <h3>Flexible</h3>
      <p>Metes secciones, cards, tablas, lo que quieras.</p>
    </div>
    """, unsafe_allow_html=True)

# ---------- DATA ----------
st.markdown('<div id="dashboard"></div>', unsafe_allow_html=True)

chart_data = pd.DataFrame(
    np.random.randn(10, 2),
    columns=[f"Col{i+1}" for i in range(2)]
)

# ---------- SECCIÓN CHART + TEXTO ----------
left, right = st.columns([2, 1], gap="large")

with left:
    st.markdown("""
    <div class="section">
      <div class="section-title">📈 Chart (nativo de Streamlit)</div>
    """, unsafe_allow_html=True)

    st.line_chart(chart_data, height=320)

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="section">
      <div class="section-title">Resumen</div>
    </div>
    """, unsafe_allow_html=True)
    st.metric("Filas", len(chart_data))
    st.metric("Columnas", chart_data.shape[1])

# ---------- TABLA HTML (con tu df.to_html) ----------
chart_data_html = chart_data.to_html(index=False)

st.markdown("""
<div class="section">
  <div class="section-title">Tabla renderizada en HTML</div>
  <div class="table-wrap">
""", unsafe_allow_html=True)

st.markdown(chart_data_html, unsafe_allow_html=True)

st.markdown("""
  </div>
</div>
""", unsafe_allow_html=True)