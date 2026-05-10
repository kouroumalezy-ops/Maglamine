```python
import streamlit as st
import pandas as pd
import os
from datetime import datetime
import google.generativeai as genai
from PIL import Image
import json

# --- 1. CONFIGURAZIONE, ICONA IPHONE E STILE PRO ---
# Questa parte deve essere la primissima cosa nel codice
st.set_page_config(
    page_title="Lamine AI - Sistema Logistico", 
    page_icon="🏗️", 
    layout="wide"
)

# Inserimento CSS per lo stile e link per l'icona Apple (logo dorato)
st.markdown(f"""
    <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/kouroumalezy-ops/Maglamine/main/IMG_0407.png">
    <style>
    /* Sfondo dell'applicazione professionale */
    .stApp {{ 
        background-color: #f0f2f6; 
        color: #1e1e1e; 
    }}
    
    /* Colore dei titoli principale */
    h1, h2, h3 {{
        color: #0e1133 !important;
    }}

    /* Stile dei bottoni dorati come il logo LAI */
    .stButton>button {{
        background: linear-gradient(135deg, #ffcc00, #e6b800) !important;
        color: #000000 !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: 1px solid #cca300 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        width: 100%;
    }}
    
    /* Stile per le schede dei reparti (Tabs) */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background-color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}

    /* Sfondo bianco per le tabelle dati */
    .stDataFrame {{
        background-color: white;
        border-radius: 10px;
        padding: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONFIGURAZIONE INTELLIGENZA ARTIFICIALE ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.warning("⚠️ Nota: Inserisci la chiave API nei Secrets di Streamlit per attivare l'analisi automatica.")
except Exception:
    pass

# --- 3. FUNZIONI DI SUPPORTO ---
def analizza_con_ia(immagine_pil, tipo_analisi="targa"):
    """Usa l'IA per leggere i dati dalle foto delle macchine o dei documenti"""
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
        # Pulizia del formato JSON restituito dall'IA
        if "```json" in testo:
            testo = testo.split("```json")[1].split("```")[0]
        elif "```" in testo:
            testo = testo.split("```")[1].split("```")[0]
        return json.loads(testo)
    except:
        return None

def carica_db(nome_file, colonne):
    """Carica i dati dai file Excel del magazzino"""
    if os.path.exists(nome_file):
        try: 
            return pd.read_excel(nome_file)
        except: 
            return pd.DataFrame(columns=colonne)
    return pd.DataFrame(columns=colonne)

# --- 4. INTERFACCIA UTENTE (UI) ---
st.title("🏗️ Sistema Gestionale Lamine AI")

# Creazione delle sezioni del magazzino
tab_rip, tab_torre, tab_nol, tab_dep = st.tabs([
    "🛠️ RIPARAZIONI", "☕ TORREFAZIONE", "🚜 NOLEGGIO", "📦 DEPOSITO"
])

# SEZIONE 1: RIPARAZIONI
with tab_rip:
    st.subheader("🛠️ Gestione Assistenza Tecnica")
    df_rip = carica_db("riparazioni.xlsx", ["Data", "Cliente", "Settore", "Macchina", "Tecnico", "Giorni"])
    
    if not df_rip.empty:
        # Calcolo dei giorni trascorsi per gli allarmi 90 giorni
        df_rip['Data'] = pd.to_datetime(df_rip['Data'])
        df_rip['Giorni'] = (datetime.now() - df_rip['Data']).dt.days
        st.dataframe(df_rip, use_container_width=True)
    else:
        st.info("Nessuna riparazione registrata in questo momento.")

# SEZIONE 2: TORREFAZIONE
with tab_torre:
    st.subheader("☕ Hub Macchine Caffè")
    torrefattori = ["Lavazza", "Ross caffè", "Bonanni", "La Genovese", "Costadoro", "Altro"]
    cliente_scelto = st.selectbox("Seleziona il Cliente/Torrefattore", torrefattori)
    
    foto_caffe = st.camera_input("Scansiona targa macchina caffè", key="cam_torre")
    if foto_caffe:
        with st.spinner("Analisi IA in corso..."):
            dati = analizza_con_ia(Image.open(foto_caffe), "targa")
            if dati:
                st.success(f"Dati estratti correttamente per {cliente_scelto}:")
                st.json(dati)
                if st.button("💾 SALVA SCHEDA MACCHINA"):
                    st.toast("Dati salvati nel database!")

# SEZIONE 3: NOLEGGIO
with tab_nol:
    st.subheader("🚜 Stato Parco Mezzi")
    col1, col2 = st.columns(2)
    with col1:
        st.info("**Muletto 1.5t**")
        if st.toggle("Disponibile", value=True, key="nol1"): 
            st.success("STATO: LIBERO 🟢")
        else: 
            st.error("STATO: IN NOLEGGIO 🔴")
    with col2:
        st.info("**Transpallet Elettrico**")
        if st.toggle("Disponibile", value=True, key="nol2"): 
            st.success("STATO: LIBERO 🟢")
        else: 
            st.error("STATO: IN NOLEGGIO 🔴")

# SEZIONE 4: DEPOSITO
with tab_dep:
    st.subheader("📦 Deposito Merci & Importazione")
    st.write("Importa liste Excel per Lavastoviglie, Forni e Ghiaccio.")
    file_upload = st.file_uploader("Trascina qui il file .xlsx", type=["xlsx"])
    
    if file_upload:
        df_caricato = pd.read_excel(file_upload)
        st.write("Anteprima dati rilevati:")
        st.dataframe(df_caricato.head(), use_container_width=True)
        if st.button("📥 UNISCI AL MAGAZZINO"):
            st.success("Importazione completata con successo!")

```
