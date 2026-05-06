import streamlit as st
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="Maglamine AI & Tech", page_icon="🤖", layout="wide")

# 2. CREDENZIALI
MIA_EMAIL = "kurumalesi@gmail.com" 
PASSWORD_APP = "METTI_QUI_LE_TUE_16_LETTERE" 

# CHIAVE IA
genai.configure(api_key="AIzaSyCOnJQ9ueY2Bcp9nkibY6P0GpEmQ5-HvK8")

def identifica_attrezzatura(immagine_pil):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = "Identifica l'attrezzatura logistica in foto. Rispondi solo con il nome dell'oggetto (max 2 parole)."
        response = model.generate_content([prompt, immagine_pil])
        return response.text.strip()
    except:
        return ""

# 3. DATABASE (Aggiornato con Tecnico e Luogo)
NOME_FILE = "dati_magazzino.xlsx"
if os.path.exists(NOME_FILE):
    df = pd.read_excel(NOME_FILE)
else:
    df = pd.DataFrame(columns=["Data", "Cliente", "Stato", "Tipo", "Marca", "Tecnico", "Luogo"])

# 4. INTERFACCIA
st.title("🤖 Maglamina: Gestione Tecnica AI")

col1, col2 = st.columns([1, 1])

tipo_rilevato = ""
with col1:
    foto = st.camera_input("📸 Foto per il Tecnico")
    if foto:
        img = Image.open(foto)
        with st.spinner("L'IA sta identificando il mezzo..."):
            tipo_rilevato = identifica_attrezzatura(img)

with col2:
    cliente = st.text_input("👤 Cliente")
    tipo = st.text_input("🚜 Tipo Macchina", value=tipo_rilevato)
    
    # MODIFICA: Menu Stato con "Ritiro Tecnico"
    stati_possibili = ["In Deposito", "Ritiro Tecnico", "In Riparazione", "Muletto da prestare", "Rientro"]
    stato = st.selectbox("🚦 Stato Attrezzatura", stati_possibili)
    
    # AGGIUNTA: Riferimento Tecnico
    tecnico = st.text_input("👨‍🔧 Nome Tecnico (Ritira/Consegna)")
    
    luogo = st.text_input("📍 Luogo di giacenza")

    if st.button("✅ REGISTRA E AVVISA", use_container_width=True):
        nuovo = {
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Cliente": cliente, 
            "Stato": stato,
            "Tipo": tipo, 
            "Tecnico": tecnico,
            "Luogo": luogo
        }
        df = pd.concat([df, pd.DataFrame([nuovo])], ignore_index=True)
        df.to_excel(NOME_FILE, index=False)
        st.success(f"Registrato! Stato: {stato} - Tecnico: {tecnico}")
        st.rerun()

st.write("---")
st.subheader("📊 Registro Interventi e Ritiri")
st.dataframe(df, use_container_width=True)
