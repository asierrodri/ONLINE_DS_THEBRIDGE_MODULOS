import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Landing",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={  # esto controla el menú de los 3 puntos
        "Get Help": None,
        "Report a bug": None,
        "About": None,
    },
)

# 1) OCULTAR HEADER/DEPLOY/FOOTER (CSS)
st.markdown("""
<style>
/* Quita la barra superior */
header[data-testid="stHeader"] { display: none; }

/* Quita el menú (hamburguesa / toolbar) y el footer */
div[data-testid="stToolbar"] { display: none; }
footer { display: none; }

/* Quita espacios extra que deja el header */
.block-container { padding-top: 1.5rem; }

/* NAVBAR */
.navbar {
  position: sticky;
  top: 0;
  z-index: 999;
  padding: 14px 18px;
  border-radius: 16px;
  background: rgba(15, 23, 42, 0.75);
  border: 1px solid rgba(255,255,255,0.10);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}
.brand { font-weight: 800; letter-spacing: -0.3px; }
.links a {
  margin-left: 14px;
  text-decoration: none;
  opacity: 0.85;
}
.links a:hover { opacity: 1; }
.cta {
  margin-left: 14px;
  padding: 8px 12px;
  border-radius: 12px;
  background: rgba(255,122,0,0.95);
  color: #111 !important;
  font-weight: 700;
}
.section {
  padding: 18px;
  border-radius: 18px;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)

# 2) TU NAVBAR (HTML)
st.markdown("""
<div class="navbar">
  <div class="brand">Mi App</div>
  <div class="links">
    <a href="#inicio">Inicio</a>
    <a href="#dashboard">Dashboard</a>
    <a href="#tabla">Tabla</a>
    <a class="cta" href="#contacto">Contactar</a>
  </div>
</div>
""", unsafe_allow_html=True)

# Secciones con anclas
st.markdown('<div id="inicio"></div>', unsafe_allow_html=True)
st.markdown('<div class="section"><h2>Inicio</h2><p>Hero / texto de landing…</p></div>', unsafe_allow_html=True)

st.markdown('<div id="dashboard"></div>', unsafe_allow_html=True)
chart_data = pd.DataFrame(np.random.randn(10, 2), columns=["Col1", "Col2"])
st.markdown('<div class="section"><h2>Dashboard</h2></div>', unsafe_allow_html=True)
st.line_chart(chart_data)

st.markdown('<div id="tabla"></div>', unsafe_allow_html=True)
st.markdown('<div class="section"><h2>Tabla</h2></div>', unsafe_allow_html=True)
st.markdown(chart_data.to_html(index=False), unsafe_allow_html=True)

st.markdown('<div id="contacto"></div>', unsafe_allow_html=True)
st.markdown('<div class="section"><h2>Contacto</h2><p>CTA final…</p></div>', unsafe_allow_html=True)
