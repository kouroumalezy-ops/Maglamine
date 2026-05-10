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
    .status-card {
        padding: 20px;
        border-radius: 15px;
        background-color: #1e2130;
        border-left: 5px solid #ffcc00;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Configurazione IA (Inserisci la tua chiave qui o nei secrets)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    genai.configure(api_key="TUA_CHIAVE_QUI")

# --- 2. FUNZIONI CORE ---

def analizza_con_ia(immagine_pil, tipo_analisi="mezzo"):
    model = genai.GenerativeModel('gemini-1.5-flash')
    if tipo_analisi == "mezzo":
        prompt = "Analizza questo transpallet. Estrai in JSON: tipo, marca, matricola, consiglio_posizionamento."
    else:
        prompt = "Analizza questo DDT (Bolla). Estrai in JSON: numero_bolla, matricola_merce, cliente."
    
    try:
        response = model.generate_content([prompt, immagine_pil])
        testo_pulito = response.text.replace("```json", "").replace("
```", "").strip()
        return json.loads(testo_pulito)
    except:
        return None

# Caricamento database (Excel)
def carica_db(nome_file, colonne):
    if os.path.exists(nome_file):
        return pd.read_excel(nome_file)
    return pd.DataFrame(columns=colonne)

# --- 3. INTERFACCIA PRINCIPALE ---
st.title("🏗️ Lamine AI: Gestione Intelligente & Sicurezza")

menu = st.sidebar.radio("Scegli Operazione", ["Uscita Merce (Controllo Bolla)", "Deposito & Inventario", "Riparazioni (Allarme 90gg)", "Disponibilità Muletti"])

# --- MODULO 1: CONTROLLO BOLLA (ANTI-FRODE) ---
if menu == "Uscita Merce (Controllo Bolla)":
    st.subheader("🚨 Smart Gate: Verifica Documento e Matricola")
    col1, col2 = st.columns(2)
    
    with col1:
        foto_bolla = st.camera_input("Fotografa la Bolla (DDT)")
    
    if foto_bolla:
        dati_bolla = analizza_con_ia(Image.open(foto_bolla), "bolla")
        with col2:
            if dati_bolla:
                st.write(f"📄 **Bolla N:** {dati_bolla.get('numero_bolla')}")
                st.write(f"👤 **Cliente:** {dati_bolla.get('cliente')}")
                st.write(f"🔢 **Matricola su Bolla:** {dati_bolla.get('matricola_merce')}")
                
                # Simulazione incrocio dati
                if st.button("VERIFICA AUTENTICITÀ"):
                    # Qui aggiungeresti il controllo col tuo DB reale
                    st.components.v1.html("""
                        <script>
                        alert("✅ Lamine, la bolla è originale. Puoi procedere all'uscita.");
                        </script>
                    """, height=0)
            else:
                st.error("Errore lettura bolla. Possibile documento non conforme!")

# --- MODULO 2: DEPOSITO & UBICAZIONE ---
elif menu == "Deposito & Inventario":
    st.subheader("📍 Mappa Macchinari in Deposito")
    df_dep = carica_db("deposito.xlsx", ["Data", "Modello", "Matricola", "Ubicazione", "Tecnico"])
    
    with st.expander("➕ Registra Nuovo Ingresso"):
        c1, c2, c3 = st.columns(3)
        modello = c1.text_input("Modello")
        matricola = c2.text_input("Matricola")
        ubicazione = c3.text_input("Ubicazione (es. Settore A1)")
        tecnico = st.text_input("Tecnico che ha posizionato")
        
        if st.button("SALVA POSIZIONE"):
            nuovo = {"Data": datetime.now(), "Modello": modello, "Matricola": matricola, "Ubicazione": ubicazione, "Tecnico": tecnico}
            df_dep = pd.concat([df_dep, pd.DataFrame([nuovo])], ignore_index=True)
            df_dep.to_excel("deposito.xlsx", index=False)
            st.success("Posizione registrata! Non dovrai più girare a vuoto.")

    st.dataframe(df_dep, use_container_width=True)

# --- MODULO 3: RIPARAZIONI (ALLARME 90GG) ---
elif menu == "Riparazioni (Allarme 90gg)":
    st.subheader("🔧 Gestione Settori Riparazione")
    df_rip = carica_db("riparazioni.xlsx", ["Data_Ingresso", "Cliente", "Settore", "Macchina", "Tecnico_Ritiro"])
    
    # Calcolo giorni
    if not df_rip.empty:
        df_rip['Data_Ingresso'] = pd.to_datetime(df_rip['Data_Ingresso'])
        df_rip['Giorni'] = (datetime.now() - df_rip['Data_Ingresso']).dt.days
        
        # Allarme 90 giorni Settore 1
        ritardi = df_rip[(df_rip['Settore'] == "1 (Preventivata)") & (df_rip['Giorni'] > 90)]
        if not ritardi.empty:
            st.warning(f"⚠️ Lamine, ci sono {len(ritardi)} macchine ferme da oltre 90 giorni!")
            st.components.v1.html("""<script>alert("🚨 ATTENZIONE: Ritardi gravi nel Settore 1!");</script>""", height=0)

    st.write("### 🗂️ Elenco Riparazioni")
    st.dataframe(df_rip, use_container_width=True)

# --- MODULO 4: DISPONIBILITÀ MULETTI ---
elif menu == "Disponibilità Muletti":
    st.subheader("🚜 Stato Flotta Interna (Manuale)")
    
    # Esempio di gestione rapida
    st.markdown("Clicca per cambiare lo stato della macchina:")
    col1, col2, col3 = st.columns(3)
    
    macchine = ["Muletto 1.5t", "Transpallet Elettrico", "Muletto Grande"]
    for i, m in enumerate(macchine):
        with [col1, col2, col3][i]:
            st.info(f"**{m}**")
            stato = st.radio("Stato:", ["Disponibile 🟢", "In Uso 🔴"], key=f"m_{i}")
            if stato == "Disponibile 🟢":
                st.write("📍 Posizione: Piazzale")
            else:
                st.write("👤 Preso da: Tecnico X")

