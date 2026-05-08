import streamlit as st
import pandas as pd
import os
from datetime import datetime
import google.generativeai as genai
from PIL import Image
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# 1. CONFIGURAZIONE
st.set_page_config(page_title="Magianina AI Pro", page_icon="🛠️", layout="wide")

# API KEY
genai.configure(api_key="AIzaSyCOnJQ9ueY2Bcp9nkibY6P0GpEmQ5-HvK8")

def analizza_foto_ia(immagine_pil):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Prompt migliorato per estrarre tutto subito
        prompt = """Analizza questa targa tecnica. Estrai:
        TIPO: (es. Forno, Lavastoviglie, Muletto), 
        MARCA: (es. Rational, Lamber), 
        MATRICOLA: (S/N), 
        MODELLO: (Mod)
        Rispondi ESATTAMENTE così: TIPO: [dato], MARCA: [dato], MATRICOLA: [dato], MODELLO: [dato]"""
        
        response = model.generate_content([prompt, immagine_pil])
        testo = response.text
        dati = {}
        for riga in testo.split(','):
            chiave, valore = riga.split(':')
            dati[chiave.strip()] = valore.strip()
        return dati
    except:
        return None

# Funzione PDF (identica alla precedente)
def genera_pdf(dati):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(60, 800, "SCHEDA TECNICA DI RIPARAZIONE / DEPOSITO")
    c.setFont("Helvetica", 12)
    c.drawString(60, 770, f"Data: {dati['Data']}")
    c.drawString(60, 750, f"Cliente: {dati['Cliente']}")
    c.drawString(60, 730, f"Stato Mezzo: {dati['Stato']}")
    c.rect(50, 600, 500, 100)
    c.drawString(60, 680, f"Attrezzatura: {dati['Tipo']} {dati['Marca']}")
    c.drawString(60, 660, f"Modello: {dati['Modello']}")
    c.drawString(60, 640, f"Matricola: {dati['Matricola']}")
    c.drawString(60, 550, "Note Tecniche:")
    c.drawString(60, 530, dati.get('Note', '-'))
    c.save()
    buf.seek(0)
    return buf

# --- INTERFACCIA ---
st.title("🛠️ Magianina AI - Gestione Professionale")

if 'dati_ia' not in st.session_state:
    st.session_state.dati_ia = {"TIPO": "", "MARCA": "", "MATRICOLA": "", "MODELLO": ""}

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📸 1. Acquisizione")
    foto = st.camera_input("Inquadra la targa")
    
    if foto:
        img = Image.open(foto)
        # --- AUTOMAZIONE: Analizza subito senza tasti ---
        if 'ultima_foto' not in st.session_state or st.session_state.ultima_foto != foto.name:
            with st.spinner("L'intelligenza artificiale sta lavorando..."):
                risultato = analizza_foto_ia(img)
                if risultato:
                    st.session_state.dati_ia = risultato
                    st.session_state.ultima_foto = foto.name
                    st.rerun() # Ricarica per mostrare i dati nei campi

with col2:
    st.subheader("📝 2. Dettagli e Stato")
    cliente = st.text_input("👤 Cliente / Cantiere")
    
    # AGGIUNTE LE TUE CASELLE MANCANTI
    stato = st.selectbox("🚦 Stato Attrezzatura", ["Riparazione", "In Deposito", "Ritiro Tecnico", "Muletto in Uso"])
    
    tipo = st.text_input("🚜 Tipo", value=st.session_state.dati_ia.get("TIPO", ""))
    marca = st.text_input("🏷️ Marca", value=st.session_state.dati_ia.get("MARCA", ""))
    modello = st.text_input("📦 Modello", value=st.session_state.dati_ia.get("MODELLO", ""))
    matricola = st.text_input("🔢 Matricola / SN", value=st.session_state.dati_ia.get("MATRICOLA", ""))
    
    st.markdown("---")
    st.subheader("📋 Verifica Componenti")
    baricotto = st.checkbox("Controllo Baricotto / Struttura")
    note = st.text_area("🗒️ Note Intervento")

    if st.button("💾 SALVA E CREA SCHEDA", use_container_width=True):
        dati_finali = {
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Cliente": cliente,
            "Stato": stato,
            "Tipo": tipo,
            "Marca": marca,
            "Modello": modello,
            "Matricola": matricola,
            "Note": note
        }
        pdf = genera_pdf(dati_finali)
        st.success(f"✅ Registrato in {stato}!")
        st.download_button("📥 Scarica PDF", data=pdf, file_name=f"Scheda_{matricola}.pdf", mime="application/pdf")
