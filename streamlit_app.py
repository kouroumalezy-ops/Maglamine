import streamlit as st
import pandas as pd
import os
from datetime import datetime
import google.generativeai as genai
from PIL import Image
import json

# --- 1. CONFIGURAZIONE, ICONA IPHONE E STILE PRO ---
st.set_page_config(page_title="Lamine AI - Sistema Logistico", page_icon="🏗️", layout="wide")

# Questo blocco nasconde il testo e applica i colori giusti
st.markdown(f"""
    <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/kouroumalezy-ops/Maglamine/main/IMG_0407.png">
    <style>
    .stApp {{ 
        background-color: #f0f2f6; 
        color: #1e1e1e; 
    }}
    h1, h2, h3 {{
        color: #0e1133 !important;
    }}
    .stButton>button {{
        background: linear-gradient(135deg, #ffcc00, #e6b800);
        color: #000000 !important;
        font-weight: bold;
        border-radius: 8px;
        border: 1px solid #cca300;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        width: 100%;
    }}
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background-color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}
    .stDataFrame {{
        background-color: white;
        border-radius: 10px;
        padding: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONFIGURAZIONE IA ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.warning("⚠️ Inserisci la chiave API nei Secrets per usare l'IA.")
except Exception:
    pass

# --- 3. FUNZIONI CORE ---
def analizza_con_ia(immagine_pil, tipo_analisi="targa"):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompts = {{
        "targa": "Analizza questa targa tecnica. Estrai in JSON: marca, modello, matricola, anno.",
        "bolla": "Analizza questo DDT. Estrai in JSON: numero_bolla, matricola_merce, cliente.",
        "mezzo": "Analizza questo transpallet. Estrai in JSON: tipo, marca, matricola."
    }}
    prompt = prompts.get(tipo_analisi, prompts["targa"])
    try:
        response = model.generate_content([prompt, immagine_pil])
        testo = response.text.strip()
        if "
http://googleusercontent.com/immersive_entry_chip/0

### Cosa cambierà ora:
1.  **Niente scritte brutte:** Quel testo tecnico in alto sparirà e l'app sarà pulita.
2.  **Colori OK:** Lo sfondo diventerà grigio e i titoli blu scuro.
3.  **Icona iPhone:** Puntando a `IMG_0407.png`, quando aggiungerai l'app alla Home, vedrai il tuo logo dorato **LAI**.

**Un'ultima cosa:** Nello screenshot vedo il triangolino giallo "Configura la chiave API". Per farlo sparire e far funzionare l'IA (OCR delle targhe), devi andare nelle impostazioni di Streamlit (Manage App -> Settings -> Secrets) e incollare la tua chiave Gemini.

Incolla questo codice ora e l'app sarà pronta per il lavoro!
