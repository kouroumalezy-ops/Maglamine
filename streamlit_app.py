import streamlit as st
import pandas as pd
import os
from datetime import datetime
import google.generativeai as genai
from PIL import Image
import json

# --- 1. CONFIGURAZIONE E STILE "LAMINE PRO" ---
st.set_page_config(page_title="Lamine AI - Sistema Logistico", page_icon="🏗️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button {
        background: linear-gradient(135deg, #ffcc00, #ff9900);
        color: black !important;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        height: 3em;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px #ffcc00; }
    </style>
    """, unsafe_allow_html=True)

# Configurazione IA
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("Errore configurazione API Key nei Secrets.")

# --- 2. FUNZIONI CORE ---

def analizza_con_ia(immagine_pil, tipo_analisi="mezzo"):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if tipo_analisi == "mezzo":
        prompt = "Analizza questo transpallet. Estrai in JSON: tipo, marca, matricola, consiglio_posizionamento."
    elif tipo_analisi == "bolla":
        prompt = "Analizza questo DDT (Bolla). Estrai in JSON: numero_bolla, matricola_merce, cliente."
    elif tipo_analisi == "targa":
        prompt = "Analizza questa targa tecnica. Estrai in JSON: marca, modello, matricola, anno."
    else:
        prompt = "Analizza questa immagine ed estrai i dati tecnici in JSON."
    
    try:
        response = model.generate_content([prompt, immagine_pil])
        testo_risposta = response.text.strip()
        # Pulizia per estrarre solo il JSON
        if "```json" in testo_risposta:
            testo_risposta = testo_risposta.split("```json")[1].split("```")[0]
        elif "```" in testo_risposta:
            testo_risposta = testo_risposta.split("```")[1].split("```")[0]
        return json.loads(testo_risposta)
    except Exception as e:
        return None

def carica_db(nome_file, colonne):
    if os.path.exists(nome_file):
        try:
            return pd.read_excel(nome_file)
        except:
            return pd.DataFrame(columns=colonne)
    return pd.DataFrame(columns=colonne)

# --- 3. INTERFACCIA A REPARTI (CASELLE) ---
st.title("🏗️ Sistema Gestionale Lamine AI")

tab_rip, tab_torre, tab_nol, tab_dep = st.tabs([
    "🛠️ RIPARAZIONI", "☕ TORREFAZIONE", "🚜 NOLEGGIO", "📦 DEPOSITO"
])

# --- REPARTO RIPARAZIONI ---
with tab_rip:
    st.header("Gestione Riparazioni (Allarme 90gg)")
    df_rip = carica_db("riparazioni.xlsx", ["Data", "Cliente", "Settore", "Macchina", "Tecnico", "Giorni"])
    
    if not df_rip.empty:
        df_rip['Data'] = pd.to_datetime(df_rip['Data'])
        df_rip['Giorni'] = (datetime.now() - df_rip['Data']).dt.days
        # Evidenzia ritardi Settore 1 > 90gg
        def style_ritardo(row):
            if row['Settore'] == "1 (Preventivata)" and row['Giorni'] > 90:
                return ['background-color: #ff4b4b']*len(row)
            return ['']*len(row)
        st.dataframe(df_rip.style.apply(style_ritardo, axis=1), use_container_width=True)
    else:
        st.write("Nessuna riparazione in corso.")

# --- REPARTO TORREFAZIONE ---
with tab_torre:
    st.header("☕ Hub Torrefattori (Lavazza, Bonanni, ecc.)")
    torre_list = ["Lavazza", "Ross caffè", "Bonanni", "La Genovese", "Altro"]
    scelta_torre = st.selectbox("Seleziona Torrefattore", torre_list)
    
    foto_t = st.camera_input("Scansiona targa macchina caffè", key="torre_cam")
    if foto_t:
        dati = analizza_con_ia(Image.open(foto_t), "targa")
        if dati:
            st.success(f"Scheda creata per {scelta_torre}")
            st.json(dati)

# --- REPARTO NOLEGGIO ---
with tab_nol:
    st.header("🚜 Disponibilità Parco Noleggio")
    m1 = st.checkbox("Muletto 1.5t - Disponibile 🟢")
    m2 = st.checkbox("Transpallet Elettrico - Disponibile 🟢")
    if not m1: st.error("Muletto 1.5t in USO 🔴")
    if not m2: st.error("Transpallet Elettrico in USO 🔴")

# --- REPARTO DEPOSITO & IMPORT ---
with tab_dep:
    st.header("📦 Deposito & Caricamento Elenchi")
    file_ex = st.file_uploader("Trascina file Excel Ristorazione", type=['xlsx'])
    if file_ex:
        df_ex = pd.read_excel(file_ex)
        st.write("Anteprima Elenco:")
        st.dataframe(df_ex.head())
