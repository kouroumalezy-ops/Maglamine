import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
from PIL import Image
from datetime import datetime, timedelta

# --- 1. SICUREZZA E AI ---
# Assicurati di aggiungere GOOGLE_API_KEY nei 'Secrets' di Streamlit Cloud
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("⚠️ Chiave API non trovata! Configurala nei Secrets di Streamlit.")

# --- 2. CONFIGURAZIONE ESTETICA (ROSSO/BLU) ---
st.set_page_config(page_title="Lamine Kourouma Magazzino", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #f4f7f9; }
    h1 { color: #1d3557; border-bottom: 3px solid #e63946; }
    .stButton>button { background-color: #e63946; color: white; border-radius: 10px; border: none; height: 50px; font-weight: bold;}
    .stButton>button:hover { background-color: #1d3557; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FUNZIONI LOGICHE ---
def analizza_targa(foto):
    model = genai.GenerativeModel('gemini-1.5-flash')
    img = Image.open(foto)
    prompt = "Analizza questa etichetta tecnica. Estrai: Marca, Modello, S/N. Rispondi in modo schematico."
    response = model.generate_content([prompt, img])
    return response.text

def crea_scheda_pdf(dati):
    pdf = FPDF()
    pdf.add_page()
    # Intestazione Blu
    pdf.set_fill_color(29, 53, 87)
    pdf.rect(0, 0, 210, 35, 'F')
    pdf.set_font("Arial", 'B', 18)
    pdf.set_text_color(255, 255, 255)
    pdf.text(15, 22, "LAMINE KOUROUMA - SCHEDA TECNICA")
    
    # Contenuto
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 12)
    pdf.ln(40)
    pdf.cell(0, 10, f"DATA: {dati['data']}", ln=True)
    pdf.cell(0, 10, f"REPARTO: {dati['reparto']}", ln=True)
    pdf.cell(0, 10, f"SCADENZA PREVISTA: {dati['scadenza']}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"MACCHINARIO: {dati['modello']}", ln=True)
    pdf.cell(0, 10, f"MATRICOLA: {dati['sn']}", ln=True)
    pdf.cell(0, 10, f"CLIENTE: {dati['cliente']}", ln=True)
    pdf.ln(10)
    pdf.cell(0, 10, "NOTE INTERVENTO:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 10, dati['note'], border=1)
    return pdf.output(dest='S').encode('latin-1')

# --- 4. INTERFACCIA APP ---
st.title("📦 Magazzino Lamine Kourouma")

# Fotocamera
foto_input = st.camera_input("Scansiona Targa Macchinario")

if foto_input:
    with st.spinner("L'AI sta leggendo i dati..."):
        testo_ai = analizza_targa(foto_input)
        st.success("Dati rilevati correttamente!")
        st.text_area("Dati AI:", testo_ai)

st.divider()

# Form di registrazione
with st.form("magazzino_form"):
    col1, col2 = st.columns(2)
    with col1:
        modello = st.text_input("Modello Macchina")
        cliente = st.text_input("Cliente")
    with col2:
        reparto = st.selectbox("Destinazione", ["Deposito", "Riparazione", "Noleggio"])
        seriale = st.text_input("S/N o Matricola")
    
    note = st.text_area("Descrizione Guasto / Note")
    
    inviato = st.form_submit_button("REGISTRA E GENERA PDF")

    if inviato:
        data_oggi = datetime.now()
        data_scadenza = data_oggi + timedelta(days=90)
        
        dati_scheda = {
            "data": data_oggi.strftime("%d/%m/%Y"),
            "scadenza": data_scadenza.strftime("%d/%m/%Y"),
            "modello": modello,
            "cliente": cliente,
            "reparto": reparto,
            "sn": seriale,
            "note": note
        }
        
        pdf_bytes = crea_scheda_pdf(dati_scheda)
        st.download_button("📥 Scarica Scheda Riparazione", pdf_bytes, f"Scheda_{seriale}.pdf", "application/pdf")
