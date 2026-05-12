
import streamlit as st
import pandas as pd
import os
from datetime import datetime
import google.generativeai as genai
from PIL import Image
import json

# --- CONFIGURAZIONE ---
LOGO_URL = "[https://raw.githubusercontent.com/kouroumalezy-ops/Maglamine/main/IMG_0407.png](https://raw.githubusercontent.com/kouroumalezy-ops/Maglamine/main/IMG_0407.png)"

st.set_page_config(
    page_title="Lamine AI", 
    page_icon=LOGO_URL,
    layout="wide"
)

# Istruzioni per iPhone
st.markdown(f"""
    <head>
        <link rel="manifest" href="manifest.json">
        <link rel="apple-touch-icon" href="{LOGO_URL}">
        <meta name="apple-mobile-web-app-capable" content="yes">
    </head>
    <style>
    .stApp {{ background-color: #f5f7f9; }}
    .title-gold {{
        color: #d4af37;
        font-size: 40px;
        font-weight: bold;
    }}
    div.stButton > button {{
        background: linear-gradient(135deg, #ffcc00, #d4af37) !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        border: none !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
c1, c2 = st.columns([1, 5])
with c1:
    st.image(LOGO_URL, width=90)
with c2:
    st.markdown('<p class="title-gold">LAMINE AI</p>', unsafe_allow_html=True)

# --- REPARTI ---
tabs = st.tabs(["🛠️ ASSISTENZA", "☕ CAFFÈ", "🚜 MEZZI", "📦 DEPOSITO"])

with tabs[0]:
    st.subheader("Assistenza Officina")
    st.dataframe(pd.DataFrame({"Ingresso": ["12/05/2024"], "Cliente": ["Hotel Roma"], "Stato": ["In corso"]}), use_container_width=True)

with tabs[1]:
    st.subheader("Settore Caffè")
    st.selectbox("Torrefattore", ["Lavazza", "Ross Caffè", "Altro"])
    st.camera_input("Foto Targa")

with tabs[2]:
    st.subheader("Mezzi")
    st.toggle("Muletto Disponibile", value=True)

with tabs[3]:
    st.subheader("Magazzino")
    st.file_uploader("Carica Excel", type=["xlsx"])

