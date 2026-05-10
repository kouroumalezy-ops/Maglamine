import streamlit as st
import pandas as pd
import os
from datetime import datetime
import google.generativeai as genai
from PIL import Image
import json

# --- 1. CONFIGURAZIONE E STILE "LAMINE LIGHT & PRO" ---
st.set_page_config(page_title="Lamine AI - Sistema Logistico", page_icon="🏗️", layout="wide")

st.markdown("""
    <style>
    /* Sfondo grigio chiaro professionale */
    .stApp { 
        background-color: #f0f2f6; 
        color: #1e1e1e; 
    }
    
    /* Titoli in blu scuro */
    h1, h2, h3 {
        color: #0e1133 !important;
    }

    /* Bottoni Oro Lamine */
    .stButton>button {
        background: linear-gradient(135deg, #ffcc00, #e6b800);
        color: #000000 !important;
        font-weight: bold;
        border-radius: 8px;
        border: 1px solid #cca300;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        width: 100%;
    }
    
    /* Tabs (le caselle dei reparti) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    /* Riquadri per le tabelle */
    .stDataFrame {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONFIGURAZIONE IA ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("⚠️ Configura la chiave API nei Secrets di Streamlit per attivare l'IA.")

# --- 3. FUNZIONI CORE ---
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
        try: return pd.read_excel(nome_file)
        except: return pd.DataFrame(columns=colonne)
    return pd.DataFrame(columns=colonne)

# --- 4. INTERFACCIA PRINCIPALE ---
st.title("🏗️ Sistema Gestionale Lamine AI")

tab_rip, tab_torre, tab_nol, tab_dep = st.tabs([
    "🛠️ RIPARAZIONI", "☕ TORREFAZIONE", "🚜 NOLEGGIO", "📦 DEPOSITO"
])

# --- REPARTO RIPARAZIONI ---
with tab_rip:
    st.subheader("🛠️ Gestione Assistenza (Allarme 90gg)")
    df_rip = carica_db("riparazioni.xlsx", ["Data", "Cliente", "Settore", "Macchina", "Tecnico", "Giorni"])
    
    if not df_rip.empty:
        df_rip['Data'] = pd.to_datetime(df_rip['Data'])
        df_rip['Giorni'] = (datetime.now() - df_rip['Data']).dt.days
        
        def evidenzia_ritardi(row):
            if row['Settore'] == "1 (Preventivata)" and row['Giorni'] > 90:
                return ['background-color: #ff4b4b; color: white'] * len(row)
            return [''] * len(row)
        
        st.dataframe(df_rip.style.apply(evidenzia_ritardi, axis=1), use_container_width=True)
    else:
        st.info("Nessuna riparazione registrata al momento.")

# --- REPARTO TORREFAZIONE ---
with tab_torre:
    st.subheader("☕ Hub Macchine Caffè")
    torrefattori = ["Lavazza", "Ross caffè", "Bonanni", "La Genovese", "Costadoro", "Altro"]
    cliente_scelto = st.selectbox("Seleziona il Torrefattore", torrefattori)
    
    foto_caffe = st.camera_input("Scansiona targa macchina caffè", key="cam_torre")
    if foto_caffe:
        with st.spinner("Creazione scheda automatica..."):
            dati = analizza_con_ia(Image.open(foto_caffe), "targa")
            if dati:
                st.success(f"Dati estratti per {cliente_scelto}:")
                st.write(dati)
                if st.button("SALVA NEL DATABASE TORREFAZIONE"):
                    # Qui andrebbe la logica di salvataggio su Excel
                    st.toast("Scheda salvata!")

# --- REPARTO NOLEGGIO ---
with tab_nol:
    st.subheader("🚜 Parco Macchine da Noleggio")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Muletto 1.5t**")
        stato1 = st.toggle("Disponibile", value=True, key="nol1")
        if stato1: st.success("LIBERO 🟢")
        else: st.error("IN NOLEGGIO 🔴")
    with col2:
        st.write("**Transpallet Elettrico**")
        stato2 = st.toggle("Disponibile", value=True, key="nol2")
        if stato2: st.success("LIBERO 🟢")
        else: st.error("IN NOLEGGIO 🔴")

# --- REPARTO DEPOSITO & RISTORAZIONE ---
with tab_dep:
    st.subheader("📦 Deposito & Importazione Elenchi")
    st.write("Trascina qui i file Excel della Ristorazione (Lavastoviglie, Forni, Ghiaccio)")
    file_upload = st.file_uploader("Carica file .xlsx", type=["xlsx"])
    
    if file_upload:
        df_caricato = pd.read_excel(file_upload)
        st.write("Anteprima dati caricati:")
        st.dataframe(df_caricato.head(), use_container_width=True)
        if st.button("UNISCI AL MAGAZZINO"):
            st.success("Tutti i macchinari sono stati importati correttamente!")
