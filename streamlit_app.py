import streamlit as st
import pandas as pd
import os
from datetime import datetime
import google.generativeai as genai
from PIL import Image
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# 1. CONFIGURAZIONE
st.set_page_config(page_title="Magazzino della Min", page_icon="📦", layout="wide")

# API KEY (Assicurati che non ci siano spazi vuoti attorno alla chiave)
genai.configure(api_key="AIzaSyCOnJQ9ueY2Bcp9nkibY6P0GpEmQ5-HvK8")

def analizza_targa_veloce(immagine_pil):
    """Lettura semplificata per compilazione automatica"""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = """Analizza la foto. Trova TIPO, MARCA, MODELLO e MATRICOLA. 
        Rispondi SOLO con i valori separati da un trattino.
        Esempio: Lavastoviglie - Lamber - L21 - 20169611"""
        
        response = model.generate_content([prompt, immagine_pil])
        testo = response.text.strip()
        
        # Dividiamo per il trattino
        parti = [p.strip() for p in testo.split('-')]
        
        return {
            "TIPO": parti[0] if len(parti) > 0 else "Non rilevato",
            "MARCA": parti[1] if len(parti) > 1 else "Non rilevato",
            "MODELLO": parti[2] if len(parti) > 2 else "Non rilevato",
            "MATRICOLA": parti[3] if len(parti) > 3 else "Non rilevato"
        }
    except Exception as e:
        st.error(f"Errore tecnico IA: {e}")
        return None

# --- LOGICA DI STATO ---
if 'dati_macchina' not in st.session_state:
    st.session_state.dati_macchina = {"TIPO": "", "MARCA": "", "MODELLO": "", "MATRICOLA": ""}

# --- INTERFACCIA ---
st.title("📦 Magazzino della Min")
st.markdown("**Sviluppato da Lamine Kourouma** | *Powered by Magianina AI*")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📸 Scatto Targa")
    foto = st.camera_input("Inquadra la targa Rational o Lamber")
    
    if foto:
        img = Image.open(foto)
        # Se la foto è nuova, analizza subito
        if 'last_pic' not in st.session_state or st.session_state.last_pic != foto.name:
            with st.spinner("Lamine, sto leggendo la targa per te..."):
                risultato = analizza_targa_veloce(img)
                if risultato:
                    st.session_state.dati_macchina = risultato
                    st.session_state.last_pic = foto.name
                    st.rerun() # FORZA IL REFRESH DEI CAMPI

with col2:
    st.subheader("📝 Dettagli Registrazione")
    
    with st.container(border=True):
        cliente = st.text_input("👤 Cliente", placeholder="Inserisci nome cliente")
        stato = st.selectbox("🚦 Stato", ["Riparazione", "In Deposito", "Ritiro Tecnico", "Muletto in Uso"])
        
        # CAMPI CHE SI COMPILANO DA SOLI
        tipo = st.text_input("🚜 Tipo Macchina", value=st.session_state.dati_macchina["TIPO"])
        marca = st.text_input("🏷️ Marca", value=st.session_state.dati_macchina["MARCA"])
        modello = st.text_input("📦 Modello", value=st.session_state.dati_macchina["MODELLO"])
        matricola = st.text_input("🔢 Matricola", value=st.session_state.dati_macchina["MATRICOLA"])
        
        st.markdown("---")
        baricotto = st.checkbox("✅ Controllo Baricotto effettuato")
        note = st.text_area("🗒️ Note Lavori")

    if st.button("💾 SALVA E GENERA PDF", use_container_width=True):
        if not matricola or matricola == "Non rilevato":
            st.warning("Attenzione: La matricola non è valida. Controlla la foto.")
        else:
            st.success(f"Scheda creata per {cliente}!")
            # Qui andrebbe la funzione PDF già vista
