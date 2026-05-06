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
PASSWORD_APP = "INSERISCI_QUI_LE_TUE_16_LETTERE" 

# CHIAVE IA GEMINI
genai.configure(api_key="AIzaSyCOnJQ9ueY2Bcp9nkibY6P0GpEmQ5-HvK8")

def identifica_attrezzatura(immagine_pil):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = "Identifica l'attrezzatura logistica in questa foto. Rispondi solo con il nome dell'oggetto (es: Muletto, Transpallet, Scaffale)."
        response = model.generate_content([prompt, immagine_pil])
        return response.text.strip()
    except:
        return ""

# 3. DATABASE
NOME_FILE = "dati_magazzino.xlsx"
if os.path.exists(NOME_FILE):
    df = pd.read_excel(NOME_FILE)
else:
    colonne = ["Data", "Cliente", "Stato", "Tipo Macchina", "Tecnico Riferimento", "Luogo", "Marca/Matricola"]
    df = pd.DataFrame(columns=colonne)

# 4. INTERFACCIA PRINCIPALE
st.title("🏗️ Registro Maglamina AI")
st.write("Gestione intelligente delle attrezzature e dei ritiri tecnici.")

col1, col2 = st.columns([1, 1])

tipo_rilevato = ""
with col1:
    st.subheader("📸 Acquisizione")
    foto = st.camera_input("Scatta foto per identificazione automatica")
    if foto:
        img = Image.open(foto)
        with st.spinner("L'IA sta analizzando il mezzo..."):
            tipo_rilevato = identifica_attrezzatura(img)
            st.success(f"IA rileva: {tipo_rilevato}")

with col2:
    st.subheader("📝 Dettagli Registrazione")
    cliente = st.text_input("👤 Cliente / Cantiere")
    
    # Campo Tipo compilato automaticamente dall'IA
    tipo = st.text_input("🚜 Tipo Macchina", value=tipo_rilevato)
    
    # Menu Stato con focus sul Tecnico
    stati = ["In Deposito", "Ritiro Tecnico", "Consegnato al Tecnico", "In Riparazione", "Rientro"]
    stato = st.selectbox("🚦 Stato Attrezzatura", stati)
    
    # Riferimento Tecnico e Luogo
    tecnico = st.text_input("👨‍🔧 Tecnico di Riferimento", placeholder="Chi ritira il mezzo?")
    luogo = st.text_input("📍 Luogo / Posizione", placeholder="Es: Magazzino Nord, Settore B")
    info_extra = st.text_input("🏷️ Marca o Matricola")

    if st.button("✅ SALVA E REGISTRA", use_container_width=True):
        nuovo_dato = {
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Cliente": cliente, 
            "Stato": stato,
            "Tipo Macchina": tipo, 
            "Tecnico Riferimento": tecnico,
            "Luogo": luogo,
            "Marca/Matricola": info_extra
        }
        df = pd.concat([df, pd.DataFrame([nuovo_dato])], ignore_index=True)
        df.to_excel(NOME_FILE, index=False)
        st.balloons()
        st.success(f"Registrato con successo per il tecnico: {tecnico}")
        st.rerun()

# 5. TABELLA REGISTRO
st.write("---")
st.subheader("📊 Registro Storico (Tecnico & Magazzino)")
st.dataframe(df, use_container_width=True)

# 6. FIRMA
st.write("---")
st.markdown("<p style='text-align: center; color: gray;'>Sviluppato da Lamine Kourouma v2.0 - IA Integrata</p>", unsafe_allow_html=True)
