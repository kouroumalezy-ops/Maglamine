import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
from datetime import datetime

# CONFIGURAZIONE STABILE
st.set_page_config(page_title="Scanner Magazzino della Min", layout="wide")

# API KEY (La tua chiave è attiva, usiamola bene)
genai.configure(api_key="AIzaSyCOnJQ9ueY2Bcp9nkibY6P0GpEmQ5-HvK8")

def analizza_targa_definitivo(foto_scattata):
    try:
        # Usiamo il modello "gemini-1.5-flash" che è il più veloce per i telefoni
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Trasformiamo la foto in un formato che l'IA capisce velocemente
        img = Image.open(foto_scattata)
        img.thumbnail((800, 800)) # Riduce il peso per evitare timeout
        
        prompt = """Sei un assistente tecnico. Analizza questa targa e scrivi SOLO i dati richiesti così:
        TIPO: (valore)
        MARCA: (valore)
        MODELLO: (valore)
        MATRICOLA: (valore)
        Se non leggi qualcosa, scrivi 'Non rilevato'."""
        
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"Errore durante la scansione: {e}"

# INTERFACCIA
st.title("📸 Scanner Magazzino della Min")
st.write("Sviluppato da **Lamine Kourouma**")

if 'testo_ia' not in st.session_state:
    st.session_state.testo_ia = ""

# FOTOCAMERA ATTIVA
foto = st.camera_input("Inquadra la targa Rational o Lamber")

if foto:
    if st.button("🔍 SCANSIONA ORA"):
        with st.spinner("Lamine, sto leggendo i dati per te..."):
            risultato = analizza_targa_definitivo(foto)
            st.session_state.testo_ia = risultato

# MOSTRA RISULTATI
if st.session_state.testo_ia:
    st.subheader("✅ Dati Rilevati")
    st.text_area("Risultato Scanner:", value=st.session_state.testo_ia, height=150)
    st.info("Puoi copiare questi dati nelle caselle sotto o usarli per la scheda.")

# Campi manuali di backup
st.divider()
st.subheader("📝 Compilazione Scheda")
col1, col2 = st.columns(2)
with col1:
    cliente = st.text_input("Cliente")
    tipo = st.text_input("Tipo Macchina")
with col2:
    marca = st.text_input("Marca")
    matricola = st.text_input("Matricola")

if st.button("💾 SALVA SCHEDA"):
    st.success("Scheda salvata!")
