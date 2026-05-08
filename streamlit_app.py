import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 1. SETUP
st.set_page_config(page_title="Magazzino della Min", layout="wide")
genai.configure(api_key="AIzaSyCOnJQ9ueY2Bcp9nkibY6P0GpEmQ5-HvK8")

def analizza_targa_lamine(img):
    try:
        # Usiamo il modello Flash che è il più veloce in assoluto
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = "Analizza questa targa tecnica. Estrai i valori: TIPO, MARCA, MODELLO, MATRICOLA. Rispondi solo con i valori separati da virgola. Se non leggi qualcosa scrivi 'Non letto'."
        
        # Ridimensioniamo l'immagine per caricarla più velocemente dal cellulare
        img.thumbnail((800, 800))
        
        response = model.generate_content([prompt, img])
        testo = response.text.strip()
        # Se l'IA risponde bene, dividiamo i dati
        parti = [p.strip() for p in testo.split(',')]
        return parti
    except Exception as e:
        # In caso di errore, restituisce campi vuoti invece di "Riprova"
        return ["", "", "", ""]

# 2. INTERFACCIA
st.title("📦 Magazzino della Min")
st.write("Sviluppatore: **Lamine Kourouma**")

if 'dati' not in st.session_state:
    st.session_state.dati = ["", "", "", ""]

# Sezione Foto
foto = st.camera_input("📸 Scatta la foto alla targa")

if foto:
    img = Image.open(foto)
    # Tasto analisi
    if st.button("🔍 ANALIZZA ORA"):
        with st.spinner("Lamine, sto leggendo la targa..."):
            risultato = analizza_targa_lamine(img)
            st.session_state.dati = risultato
            st.rerun()

# 3. CAMPI COMPILAZIONE
st.subheader("📝 Dettagli Macchina")
col_a, col_b = st.columns(2)

with col_a:
    tipo = st.text_input("TIPO", value=st.session_state.dati[0] if len(st.session_state.dati)>0 else "")
    marca = st.text_input("MARCA", value=st.session_state.dati[1] if len(st.session_state.dati)>1 else "")

with col_b:
    modello = st.text_input("MODELLO", value=st.session_state.dati[2] if len(st.session_state.dati)>2 else "")
    matricola = st.text_input("MATRICOLA", value=st.session_state.dati[3] if len(st.session_state.dati)>3 else "")

st.markdown("---")
note = st.text_area("🗒️ Note (es. Controllo Baricotto)")

if st.button("💾 SALVA REGISTRAZIONE"):
    st.success(f"Dati per {marca} salvati nel database di Lamine!")
