
import streamlit as st
import pandas as pd
import os
from datetime import datetime
import google.generativeai as genai
from PIL import Image
import json

# --- 1. CONFIGURAZIONE, ICONA IPHONE E STILE PRO ---
# Deve essere la primissima istruzione Streamlit
st.set_page_config(
    page_title="Lamine AI - Sistema Logistico", 
    page_icon="🏗️", 
    layout="wide"
)

# CSS per stile grafico e collegamento icona Apple
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
        background: linear-gradient(135deg, #ffcc00, #e6b800) !important;
        color: #000000 !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: 1px solid #cca300 !important;
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
        st.warning("⚠️ Nota: Inserisci la chiave API nei Secrets di Streamlit per attivare l'analisi automatica.")
except Exception:
    pass

# --- 3. FUNZIONI DI SUPPORTO ---
def analizza_con_ia(immagine_pil, tipo_analisi="targa"):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompts = {
        "targa": "Analizza questa targa tecnica. Estrai in JSON: marca, modello, matricola, anno.",
        "bolla": "Analizza questo DDT. Estrai in JSON: numero_bolla, matricola_merce, cliente.",
        "mezzo": "Analizza questo transpallet. Estrai in JSON: tipo, marca, matricola."
    }
    prompt = prompts.get(tipo_analisi, prompts["targa"])
    try:
        response = model.generate_content([prompt, immagine_pil])
        testo = response.text.strip()
        if "```json" in testo:
            testo = testo.split("```json")[1].split("```")[0]
        elif "```" in testo:
            testo = testo.split("```")[1].split("```")[0]
        return json.loads(testo)
    except:
        return None

def carica_db(nome_file, colonne):
    if os.path.exists(nome_file):
        try: 
            return pd.read_excel(nome_file)
        except: 
            return pd.DataFrame(columns=colonne)
    return pd.DataFrame(columns=colonne)

# --- 4. INTERFACCIA UTENTE ---
st.title("🏗️ Sistema Gestionale Lamine AI")

tab_rip, tab_torre, tab_nol, tab_dep = st.tabs([
    "🛠️ RIPARAZIONI", "☕ TORREFAZIONE", "🚜 NOLEGGIO", "📦 DEPOSITO"
])

with tab_rip:
    st.subheader("🛠️ Gestione Assistenza Tecnica")
    df_rip = carica_db("riparazioni.xlsx", ["Data", "Cliente", "Settore", "Macchina", "Tecnico", "Giorni"])
    if not df_rip.empty:
        df_rip['Data'] = pd.to_datetime(df_rip['Data'])
        df_rip['Giorni'] = (datetime.now() - df_rip['Data']).dt.days
        st.dataframe(df_rip, use_container_width=True)
    else:
        st.info("Nessuna riparazione registrata.")

with tab_torre:
    st.subheader("☕ Hub Macchine Caffè")
    torrefattori = ["Lavazza", "Ross caffè", "Bonanni", "La Genovese", "Costadoro", "Altro"]
    cliente_scelto = st.selectbox("Seleziona il Cliente", torrefattori)
    foto_caffe = st.camera_input("Scansiona targa macchina caffè", key="cam_torre")
    if foto_caffe:
        with st.spinner("Analisi IA..."):
            dati = analizza_con_ia(Image.open(foto_caffe), "targa")
            if dati:
                st.success(f"Dati estratti per {cliente_scelto}:")
                st.json(dati)
                if st.button("💾 SALVA SCHEDA"):
                    st.toast("Salvato!")

with tab_nol:
    st.subheader("🚜 Stato Parco Mezzi")
    col1, col2 = st.columns(2)
    with col1:
        st.info("**Muletto 1.5t**")
        if st.toggle("Disponibile", value=True, key="nol1"): st.success("LIBERO 🟢")
        else: st.error("IN NOLEGGIO 🔴")
    with col2:
        st.info("**Transpallet Elettrico**")
        if st.toggle("Disponibile", value=True, key="nol2"): st.success("LIBERO 🟢")
        else: st.error("IN NOLEGGIO 🔴")

with tab_dep:
    st.subheader("📦 Deposito Merci")
    file_upload = st.file_uploader("Carica file .xlsx", type=["xlsx"])
    if file_upload:
        df_caricato = pd.read_excel(file_upload)
        st.dataframe(df_caricato.head(), use_container_width=True)
        if st.button("📥 UNISCI AL MAGAZZINO"):
            st.success("Importazione completata!")

```
