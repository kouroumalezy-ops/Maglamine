
import streamlit as st
import pandas as pd
import os
from datetime import datetime
import google.generativeai as genai
from PIL import Image
import json

# --- 1. CONFIGURAZIONE E LINK ICONA DEFINITIVI ---
# Questo URL deve puntare alla tua immagine su GitHub
LOGO_URL = "https://raw.githubusercontent.com/kouroumalezy-ops/Maglamine/main/IMG_0407.png"

st.set_page_config(
    page_title="Lamine AI", 
    page_icon=LOGO_URL,
    layout="wide"
)

# Metadati per forzare l'icona dorata su iPhone
st.markdown(f"""
    <head>
        <link rel="manifest" href="manifest.json">
        <link rel="apple-touch-icon" sizes="180x180" href="{LOGO_URL}">
        <link rel="apple-touch-icon" href="{LOGO_URL}">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    </head>
    <style>
    /* Sfondo generale grigio professionale */
    .stApp {{ background-color: #f5f7f9; }}
    
    /* Stile per il titolo dorato LAMINE AI */
    .title-gold {{
        color: #d4af37;
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 42px;
        font-weight: 900;
        margin-bottom: 0px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }}

    /* Bottoni stile Lamine (Oro/Giallo) */
    div.stButton > button {{
        background: linear-gradient(135deg, #ffcc00, #d4af37) !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        height: 3.5em !important;
        border: none !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        width: 100%;
    }}
    
    /* Stile per le schede dei reparti */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: white;
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER APP CON LOGO ---
col_logo, col_text = st.columns([1, 4])
with col_logo:
    st.image(LOGO_URL, width=100)
with col_text:
    st.markdown('<p class="title-gold">LAMINE AI</p>', unsafe_allow_html=True)
    st.caption("Sistema Logistico Integrato - Gestione Magazzino")

# --- 2. LOGICA IA (OPZIONALE) ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    pass

# --- 3. REPARTI OPERATIVI ---
t_assistenza, t_caffe, t_mezzi, t_deposito = st.tabs([
    "🛠️ ASSISTENZA", "☕ CAFFÈ", "🚜 MEZZI", "📦 DEPOSITO"
])

with t_assistenza:
    st.subheader("🛠️ Registro Assistenza Officina")
    st.info("Monitoraggio allarmi per macchine presenti da oltre 90 giorni.")
    # Dati di esempio
    df_rip = pd.DataFrame({
        "Ingresso": ["12/05/2024"],
        "Cliente": ["Hotel Roma"],
        "Macchina": ["Lavastoviglie c50"],
        "Tecnico": ["Lamine"]
    })
    st.dataframe(df_rip, use_container_width=True)

with t_caffe:
    st.subheader("☕ Gestione Torrefattori")
    cliente = st.selectbox("Seleziona Torrefattore", ["Lavazza", "Ross Caffè", "Bonanni", "Altro"])
    st.camera_input("Inquadra targa tecnica", key="cam_caffe")
    if st.button("Salva Scheda Caffè"):
        st.success(f"Dati per {cliente} salvati nel database.")

with t_mezzi:
    st.subheader("🚜 Stato Noleggio Mezzi")
    c1, c2 = st.columns(2)
    with c1:
        st.info("**Muletto Diesel**")
        st.toggle("Disponibile", value=True, key="m1")
    with c2:
        st.info("**Transpallet Elettrico**")
        st.toggle("Disponibile", value=False, key="m2")

with t_deposito:
    st.subheader("📦 Carico/Scarico Deposito")
    file_xlsx = st.file_uploader("Importa file Excel Merci", type=["xlsx"])
    if file_xlsx:
        st.success("File caricato con successo.")
    if st.button("Aggiorna Inventario Globale"):
        st.balloons()
        st.toast("Inventario sincronizzato!")
