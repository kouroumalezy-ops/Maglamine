
import streamlit as st
import pandas as pd
import os
from datetime import datetime
import json

# --- 1. CONFIGURAZIONE PAGINA ---
# Deve essere la prima istruzione assoluta
st.set_page_config(
    page_title="Lamine AI",
    page_icon="🏗️",
    layout="wide"
)

# Link al tuo logo dorato su GitHub
LOGO_URL = "https://raw.githubusercontent.com/kouroumalezy-ops/Maglamine/main/IMG_0407.png"

# --- 2. STILE GRAFICO (ORO E GRIGIO) ---
st.markdown(f"""
    <head>
        <link rel="apple-touch-icon" href="{LOGO_URL}">
        <link rel="manifest" href="manifest.json">
        <meta name="apple-mobile-web-app-capable" content="yes">
    </head>
    <style>
    /* Sfondo dell'app */
    .stApp {{ 
        background-color: #f4f7f6; 
    }}
    
    /* Titolo Lamine AI in Oro */
    .brand-title {{
        color: #d4af37;
        font-family: 'Arial Black', sans-serif;
        font-size: 40px;
        font-weight: bold;
        margin-bottom: 0;
    }}

    /* Bottoni Dorati Professionali */
    div.stButton > button {{
        background: linear-gradient(135deg, #ffcc00, #d4af37) !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        border: none !important;
        height: 3.5em !important;
        width: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }}

    /* Stile per le Tab dei Reparti */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: white;
        padding: 10px;
        border-radius: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. INTESTAZIONE ---
col_logo, col_text = st.columns([1, 5])
with col_logo:
    try:
        st.image(LOGO_URL, width=100)
    except:
        st.write("🏗️") # Fallback se l'immagine non carica

with col_text:
    st.markdown('<p class="brand-title">LAMINE AI</p>', unsafe_allow_html=True)
    st.caption("Logistica Professionale | Magazzino & Assistenza")

# --- 4. NAVIGAZIONE REPARTI ---
tab_rip, tab_torre, tab_nol, tab_dep = st.tabs([
    "🛠️ ASSISTENZA", "☕ CAFFÈ", "🚜 MEZZI", "📦 DEPOSITO"
])

with tab_rip:
    st.subheader("🛠️ Registro Officina")
    st.info("Monitoraggio macchine presenti oltre 90 giorni.")
    df_rip = pd.DataFrame({
        "Data": ["12/05/2024"],
        "Cliente": ["Esempio Srl"],
        "Macchina": ["Lavastoviglie C50"],
        "Stato": ["In Riparazione"]
    })
    st.dataframe(df_rip, use_container_width=True)

with tab_torre:
    st.subheader("☕ Gestione Macchine Caffè")
    torrefattore = st.selectbox("Seleziona Torrefattore", ["Lavazza", "Ross Caffè", "Bonanni", "Altro"])
    st.camera_input("Scansiona Targa Tecnica", key="cam_torre")
    if st.button("Salva Dati Caffè"):
        st.success(f"Scheda per {torrefattore} creata!")

with tab_nol:
    st.subheader("🚜 Disponibilità Noleggio")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Muletti Diesel", "3 Liberi")
        st.toggle("Disponibile", value=True, key="m1")
    with col2:
        st.metric("Transpallet Elet.", "1 Occupato")
        st.toggle("Disponibile", value=False, key="m2")

with tab_dep:
    st.subheader("📦 Inventario Deposito")
    file_xlsx = st.file_uploader("Carica file Excel merci", type=["xlsx"])
    if st.button("Sincronizza Magazzino"):
        st.balloons()
        st.success("Database aggiornato correttamente!")


