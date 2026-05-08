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

# API KEY
genai.configure(api_key="AIzaSyCOnJQ9ueY2Bcp9nkibY6P0GpEmQ5-HvK8")

def analizza_targa_ia(immagine_pil):
    try:
        # Usiamo il modello più recente e compatibile
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        prompt = """Analizza la targa tecnica in foto. Estrai: TIPO, MARCA, MODELLO, MATRICOLA.
        Rispondi solo con i valori separati da una virgola.
        Esempio: Forno, Rational, SCC 61, E11SG120324"""
        
        response = model.generate_content([prompt, immagine_pil])
        testo = response.text.strip()
        valori = [v.strip() for v in testo.split(',')]
        
        return {
            "TIPO": valori[0] if len(valori) > 0 else "",
            "MARCA": valori[1] if len(valori) > 1 else "",
            "MODELLO": valori[2] if len(valori) > 2 else "",
            "MATRICOLA": valori[3] if len(valori) > 3 else ""
        }
    except Exception as e:
        st.error(f"Errore IA: {e}")
        return None

# --- LOGICA PDF (Lamine Kourouma) ---
def genera_pdf(dati):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(60, 800, "MAGAZZINO DELLA MIN - SCHEDA TECNICA")
    c.setFont("Helvetica", 10)
    c.drawString(60, 780, f"Sviluppatore: Lamine Kourouma | Data: {dati['Data']}")
    c.rect(50, 650, 500, 100)
    c.drawString(60, 730, f"CLIENTE: {dati['Cliente']}")
    c.drawString(60, 710, f"MACCHINA: {dati['Tipo']} {dati['Marca']}")
    c.drawString(60, 690, f"MODELLO: {dati['Modello']} | MATRICOLA: {dati['Matricola']}")
    c.drawString(60, 600, "NOTE:")
    c.drawString(60, 580, dati['Note'])
    c.save()
    buf.seek(0)
    return buf

# --- INTERFACCIA ---
st.title("📦 Magazzino della Min")
st.markdown("Sviluppato da **Lamine Kourouma**")

if 'dati_ia' not in st.session_state:
    st.session_state.dati_ia = {"TIPO": "", "MARCA": "", "MODELLO": "", "MATRICOLA": ""}

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📸 Foto Targa")
    foto = st.camera_input("Inquadra la targa")
    if foto:
        img = Image.open(foto)
        if 'last_f' not in st.session_state or st.session_state.last_f != foto.name:
            with st.spinner("Analisi in corso..."):
                res = analizza_targa_ia(img)
                if res:
                    st.session_state.dati_ia = res
                    st.session_state.last_f = foto.name
                    st.rerun()

with col2:
    st.subheader("📝 Dettagli")
    cliente = st.text_input("Cliente", placeholder="Nome cliente")
    stato = st.selectbox("Stato", ["Riparazione", "Deposito", "Ritiro", "Muletto"])
    
    tipo = st.text_input("Tipo", value=st.session_state.dati_ia["TIPO"])
    marca = st.text_input("Marca", value=st.session_state.dati_ia["MARCA"])
    modello = st.text_input("Modello", value=st.session_state.dati_ia["MODELLO"])
    matricola = st.text_input("Matricola", value=st.session_state.dati_ia["MATRICOLA"])
    
    baricotto = st.checkbox("Controllo Baricotto OK")
    note = st.text_area("Note")

    if st.button("💾 SALVA E GENERA PDF"):
        dati = {"Data": datetime.now().strftime("%d/%m/%Y"), "Cliente": cliente, "Stato": stato, 
                "Tipo": tipo, "Marca": marca, "Modello": modello, "Matricola": matricola, "Note": note}
        pdf = genera_pdf(dati)
        st.success("Scheda Pronta!")
        st.download_button("📥 Scarica PDF", data=pdf, file_name=f"Scheda_{matricola}.pdf")
