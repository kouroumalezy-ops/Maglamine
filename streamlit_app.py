```python
import streamlit as st
import pandas as pd
import os
from datetime import datetime
import google.generativeai as genai
from PIL import Image
import json

# --- 1. CONFIGURAZIONE E FORZATURA LOGO ---
# Usiamo un link che cambia ogni volta per ingannare la memoria del telefono
LOGO_URL = "https://raw.githubusercontent.com/kouroumalezy-ops/Maglamine/main/IMG_0407.png"
BORN_TIME = datetime.now().strftime("%H%M%S")

st.set_page_config(
    page_title="Lamine AI", 
    page_icon=LOGO_URL,
    layout="wide"
)

# HTML/CSS Speciale per forzare l'icona iPhone (Apple Touch Icon)
st.markdown(f"""
    <head>
        <link rel="apple-touch-icon" href="{LOGO_URL}?v={BORN_TIME}">
        <link rel="apple-touch-icon-precomposed" href="{LOGO_URL}?v={BORN_TIME}">
        <link rel="icon" href="{LOGO_URL}?v={BORN_TIME}">
    </head>
    <style>
    /* Sfondo e stile generale */
    .stApp {{ 
        background-color: #f5f7f9; 
    }}
    
    /* Titolo Lamine AI in Oro */
    .title-gold {{
        color: #d4af37;
        font-family: 'Impact', sans-serif;
        font-size: 45px;
        letter-spacing: 2px;
        margin: 0;
    }}

    /* Bottoni stile Lamine (Oro) */
    div.stButton > button {{
        background: linear-gradient(135deg, #ffcc00, #d4af37) !important;
        color: black !important;
        border: none !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        height: 3.5em !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }}

    /* Tabs bianche professionali */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: white;
        border-radius: 15px;
        padding: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER CON LOGO ---
col_icon, col_txt = st.columns([1, 5])
with col_icon:
    st.image(LOGO_URL, width=100)
with col_txt:
    st.markdown('<p class="title-gold">LAMINE AI</p>', unsafe_allow_html=True)
    st.caption("Logistica Professionale & Assistenza")

# --- 2. IA ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    pass

# --- 3. REPARTI ---
tabs = st.tabs(["🛠️ ASSISTENZA", "☕ CAFFÈ", "🚜 MEZZI", "📦 DEPOSITO"])

with tabs[0]:
    st.subheader("Riparazioni Attive")
    st.info("Sistema di monitoraggio scadenze 90 giorni.")
    st.dataframe(pd.DataFrame({"Data": ["12/05/2024"], "Cliente": ["Test"], "Stato": ["In corso"]}), use_container_width=True)

with tabs[1]:
    st.subheader("Gestione Torrefazione")
    st.selectbox("Scegli Cliente", ["Lavazza", "Ross Caffè", "Bonanni", "Altro"])
    st.camera_input("Foto Targa")

with tabs[2]:
    st.subheader("Stato Noleggio")
    c1, c2 = st.columns(2)
    c1.metric("Muletti", "3 Liberi")
    c2.metric("Transpallet", "1 In Noleggio")
    st.toggle("Aggiorna Stato Mezzi")

with tabs[3]:
    st.subheader("Inventario Magazzino")
    st.file_uploader("Carica File Excel", type=["xlsx"])
    if st.button("Sincronizza Dati"):
        st.success("Database Aggiornato!")

```
