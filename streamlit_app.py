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

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="Magazzino della Min", page_icon="📦", layout="wide")

# API KEY GEMINI (Verifica che sia corretta)
genai.configure(api_key="AIzaSyCOnJQ9ueY2Bcp9nkibY6P0GpEmQ5-HvK8")

# --- FUNZIONI DI SUPPORTO ---

def analizza_targa_ia(immagine_pil):
    """L'IA legge la targa e restituisce i dati per i campi in automatico"""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = """Analizza la targa tecnica in foto. Estrai con precisione:
        TIPO, MARCA, MODELLO, MATRICOLA.
        Rispondi solo con i valori separati da virgola.
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
        return None

def genera_pdf_professionale(dati):
    """Crea il PDF stampabile personalizzato da Lamine Kourouma"""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4

    # Intestazione Professionale
    c.setStrokeColor(colors.black)
    c.rect(40, height - 85, width - 80, 55, fill=0)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(60, height - 60, "MAGAZZINO DELLA MIN")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, height - 78, "SCHEDA TECNICA E RITIRO")
    
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(width - 250, height - 55, f"Sviluppatore: Lamine Kourouma")
    c.drawString(width - 250, height - 68, f"Tecnologia: Magianina AI")
    c.drawString(width - 250, height - 81, f"Data: {dati['Data']}")

    # Box Dati Macchina (Grigio chiaro di sfondo opzionale)
    c.rect(40, height - 225, width - 80, 125)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(55, height - 125, f"CLIENTE / CANTIERE: {dati['Cliente'].upper()}")
    c.setFont("Helvetica", 11)
    c.drawString(55, height - 150, f"STATO ATTREZZATURA: {dati['Stato']}")
    c.line(55, height - 155, 300, height - 155)
    
    c.drawString(55, height - 175, f"TIPO: {dati['Tipo']}")
    c.drawString(55, height - 195, f"MARCA: {dati['Marca']}")
    c.drawString(250, height - 175, f"MODELLO: {dati['Modello']}")
    c.drawString(250, height - 195, f"MATRICOLA: {dati['Matricola']}")

    # Sezione Checklist (Il Baricotto)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(55, height - 250, "ESITO CONTROLLI:")
    c.rect(40, height - 360, width - 80, 115)
    
    c.setFont("Helvetica", 10)
    check_baricotto = "[X] SI" if dati['Baricotto'] else "[ ] NO"
    c.drawString(60, height - 280, f"Controllo Baricotto / Integrità Strutturale: {check_baricotto}")
    c.drawString(60, height - 305, "[ ] Verifica componenti elettrici")
    c.drawString(60, height - 330, "[ ] Pulizia e sanificazione post-intervento")

    # Note e Lavori
    c.setFont("Helvetica-Bold", 12)
    c.drawString(55, height - 385, "NOTE TECNICHE E LAVORI ESEGUITI:")
    c.rect(40, height - 550, width - 80, 150)
    c.setFont("Helvetica", 10)
    
    text_object = c.beginText(55, height - 410)
    text_object.setFont("Helvetica", 10)
    # Gestione righe lunghe nelle note
    note_testo = dati['Note'] if dati['Note'] else "Nessuna nota aggiuntiva."
    text_object.textLines(note_testo)
    c.drawText(text_object)

    # Area Firme
    c.setFont("Helvetica-Bold", 10)
    c.line(60, 150, 220, 150)
    c.drawString(60, 135, "Firma Tecnico (L. Kourouma)")
    
    c.line(width - 220, 150, width - 60, 150)
    c.drawString(width - 220, 135, "Firma per Accettazione Cliente")

    c.save()
    buf.seek(0)
    return buf

# --- INTERFACCIA UTENTE (STREAMLIT) ---

st.title("📦 Magazzino della Min")
st.markdown(f"**Sviluppato da Lamine Kourouma** | *Powered by Magianina AI*")
st.markdown("---")

# Inizializzazione dati IA per evitare errori di ricaricamento
if 'dati_ia' not in st.session_state:
    st.session_state.dati_ia = {"TIPO": "", "MARCA": "", "MODELLO": "", "MATRICOLA": ""}

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📸 1. Foto Targa")
    foto = st.camera_input("Scatta la foto per compilazione automatica")
    
    if foto:
        img = Image.open(foto)
        # Analizza solo se è una nuova foto
        if 'last_f' not in st.session_state or st.session_state.last_f != foto.name:
            with st.spinner("L'intelligenza artificiale sta leggendo i dati..."):
                risultato = analizza_targa_ia(img)
                if risultato:
                    st.session_state.dati_ia = risultato
                    st.session_state.last_f = foto.name
                    st.rerun()

with col2:
    st.subheader("📝 2. Dettagli Intervento")
    
    with st.container(border=True):
        cliente = st.text_input("👤 Cliente / Cantiere", placeholder="Es: Mario Rossi S.r.l.")
        stato = st.selectbox("🚦 Stato Attrezzatura", 
                            ["Riparazione", "In Deposito", "Ritiro Tecnico", "Muletto in Uso", "Consegnato"])
        
        # Campi popolati automaticamente dall'IA
        c_a, c_b = st.columns(2)
        tipo = c_a.text_input("🚜 Tipo", value=st.session_state.dati_ia["TIPO"])
        marca = c_b.text_input("🏷️ Marca", value=st.session_state.dati_ia["MARCA"])
        modello = c_a.text_input("📦 Modello", value=st.session_state.dati_ia["MODELLO"])
        matricola = c_b.text_input("🔢 Matricola", value=st.session_state.dati_ia["MATRICOLA"])
        
        st.markdown("---")
        baricotto = st.checkbox("✅ Baricotto / Struttura verificata")
        note = st.text_area("🗒️ Note Intervento", placeholder="Descrivi il guasto o i pezzi sostituiti...")

    if st.button("💾 SALVA E GENERA DOCUMENTO PDF", use_container_width=True):
        if not cliente or not matricola:
            st.warning("⚠️ Inserisci almeno il nome del Cliente e la Matricola per procedere.")
        else:
            dati_finali = {
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Cliente": cliente,
                "Stato": stato,
                "Tipo": tipo,
                "Marca": marca,
                "Modello": modello,
                "Matricola": matricola,
                "Baricotto": baricotto,
                "Note": note
            }
            
            # Creazione effettiva del PDF
            pdf_file = genera_pdf_professionale(dati_finali)
            
            st.success("✅ Scheda creata con successo!")
            st.download_button(
                label="📥 SCARICA SCHEDA STAMPABILE (PDF)",
                data=pdf_file,
                file_name=f"Scheda_{matricola}_{datetime.now().strftime('%d%m%y')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

# Storico rapido (Visibile solo se ci sono dati salvati in sessione)
st.markdown("---")
st.caption("Magazzino della Min - Sistema di Gestione Logistica v2.0 | Lamine Kourouma 2026")
