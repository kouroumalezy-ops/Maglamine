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
st.set_page_config(page_title="MaglaScan Pro - Schede Riparazione", page_icon="📋", layout="wide")

# API KEY (Assicurati che sia valida)
genai.configure(api_key="TUA_API_KEY_QUI") # Sostituisci con la tua chiave

# --- FUNZIONI LOGICHE ---

def analizza_foto_ia(immagine_pil):
    """L'IA legge la targa e restituisce dati strutturati"""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = """Analizza questa targa tecnica. Estrai con precisione:
        - TIPO DI MACCHINA (es. Forno, Lavastoviglie)
        - MARCA
        - MATRICOLA (S/N)
        - MODELLO
        Rispondi ESATTAMENTE in questo formato:
        TIPO: [dato], MARCA: [dato], MATRICOLA: [dato], MODELLO: [dato]"""
        
        response = model.generate_content([prompt, immagine_pil])
        testo = response.text
        # Parsing semplice dei risultati
        dati = {}
        for riga in testo.split(','):
            chiave, valore = riga.split(':')
            dati[chiave.strip()] = valore.strip()
        return dati
    except:
        return None

def genera_pdf(dati):
    """Crea un file PDF simile alla foto della scheda riparazione"""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4

    # Header - Simile a Tecno Clinic
    c.setLineWidth(1)
    c.rect(40, height - 100, width - 80, 60) # Box intestazione
    c.setFont("Helvetica-Bold", 16)
    c.drawString(60, height - 75, "SCHEDA RIPARAZIONE")
    c.setFont("Helvetica", 12)
    c.drawString(width - 200, height - 75, f"DATA: {dati['Data']}")

    # Box Cliente e Macchina
    c.rect(40, height - 250, width - 80, 140)
    c.drawString(50, height - 130, f"CLIENTE: {dati['Cliente']}")
    c.drawString(50, height - 150, f"ATTREZZATURA: {dati['Tipo']} - {dati['Marca']}")
    c.drawString(50, height - 170, f"MODELLO: {dati['Modello']}")
    c.drawString(50, height - 190, f"MATRICOLA: {dati['Matricola']}")

    # Tabella Componenti (Il "Baricotto" e altri)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 280, "VERIFICA COMPONENTI E BARICOTTO:")
    c.rect(40, height - 450, width - 80, 150)
    
    y = height - 310
    c.setFont("Helvetica", 10)
    componenti = ["Struttura/Baricotto", "Termostati", "Resistenze", "Pompa Lavaggio", "Pulizia Generale"]
    for comp in componenti:
        c.drawString(60, y, f"[  ] {comp}")
        y -= 25

    # Note Lavori
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 480, "LAVORI ESEGUITI / NOTE:")
    c.rect(40, height - 600, width - 80, 100)
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 510, dati.get('Note', 'Controllo tecnico generale.'))

    # Firme
    c.drawString(60, 100, "Firma Tecnico: ___________________")
    c.drawString(width - 250, 100, "Firma Cliente: ___________________")

    c.save()
    buf.seek(0)
    return buf

# --- INTERFACCIA STREAMLIT ---

st.title("🛠️ Magianina AI - Gestione Schede Professionali")

# Database locale
if os.path.exists("database_tecnico.xlsx"):
    df = pd.read_excel("database_tecnico.xlsx")
else:
    df = pd.DataFrame(columns=["Data", "Cliente", "Tipo", "Marca", "Matricola", "Stato"])

col1, col2 = st.columns([1, 1])

# Inizializzazione stati
if 'dati_ia' not in st.session_state:
    st.session_state.dati_ia = {"TIPO": "", "MARCA": "", "MATRICOLA": "", "MODELLO": ""}

with col1:
    st.subheader("📸 1. Acquisizione Targa")
    foto = st.camera_input("Inquadra la targa del macchinario")
    
    if foto:
        img = Image.open(foto)
        if st.button("🔍 ANALIZZA CON AI"):
            with st.spinner("Lettura targa in corso..."):
                risultato = analizza_foto_ia(img)
                if risultato:
                    st.session_state.dati_ia = risultato
                    st.success("Dati estratti correttamente!")

with col2:
    st.subheader("📝 2. Compilazione Scheda")
    cliente = st.text_input("👤 Nome Cliente / Cantiere")
    
    # Campi pre-compilati dall'IA ma modificabili
    tipo = st.text_input("🚜 Tipo Macchina", value=st.session_state.dati_ia.get("TIPO", ""))
    marca = st.text_input("🏷️ Marca", value=st.session_state.dati_ia.get("MARCA", ""))
    modello = st.text_input("📦 Modello", value=st.session_state.dati_ia.get("MODELLO", ""))
    matricola = st.text_input("🔢 Matricola / SN", value=st.session_state.dati_ia.get("MATRICOLA", ""))
    
    st.markdown("---")
    st.subheader("📋 Verifica Componenti")
    # Qui inseriamo i componenti che volevi (il "baricotto")
    col_a, col_b = st.columns(2)
    with col_a:
        c1 = st.checkbox("Controllo Baricotto/Vasca")
        c2 = st.checkbox("Resistenze")
    with col_b:
        c3 = st.checkbox("Termostati")
        c4 = st.checkbox("Test Funzionamento")
    
    note = st.text_area("🗒️ Note Intervento")

    if st.button("💾 SALVA E GENERA SCHEDA PDF", use_container_width=True):
        dati_finali = {
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Cliente": cliente,
            "Tipo": tipo,
            "Marca": marca,
            "Modello": modello,
            "Matricola": matricola,
            "Note": note
        }
        
        # 1. Salva nel Database
        nuovo_df = pd.DataFrame([dati_finali])
        df = pd.concat([df, nuovo_df], ignore_index=True)
        df.to_excel("database_tecnico.xlsx", index=False)
        
        # 2. Genera il PDF
        pdf_file = genera_pdf(dati_finali)
        
        st.success("✅ Scheda salvata!")
        st.download_button(
            label="📥 Scarica Scheda PDF per Stampa",
            data=pdf_file,
            file_name=f"Scheda_{matricola}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

# Storico in fondo
st.markdown("---")
st.subheader("📊 Ultime schede create")
st.dataframe(df.tail(5), use_container_width=True)
