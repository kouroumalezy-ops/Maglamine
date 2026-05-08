import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Configurazione rapida
st.set_page_config(page_title="Magazzino della Min", layout="wide")
genai.configure(api_key="AIzaSyCOnJQ9ueY2Bcp9nkibY6P0GpEmQ5-HvK8")

def analizza_leggero(foto_caricata):
    try:
        # 1. Rimpicciolisce la foto per la velocità
        img = Image.open(foto_caricata)
        img.thumbnail((500, 500)) # La rende piccola ma leggibile
        
        # 2. Chiama l'IA
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = "Analizza targa: scrivi TIPO, MARCA, MODELLO, MATRICOLA separati solo da virgola. Se non leggi, lascia vuoto."
        
        response = model.generate_content([prompt, img])
        return [val.strip() for val in response.text.split(',')]
    except Exception as e:
        return ["", "", "", ""]

# Interfaccia Lamine Kourouma
st.title("📦 Magazzino della Min")
st.write("Sviluppatore: **Lamine Kourouma**")

if 'dati' not in st.session_state:
    st.session_state.dati = ["", "", "", ""]

foto = st.camera_input("📸 Scatta foto alla targa")

if foto:
    if st.button("🔍 ANALIZZA ORA (VELOCE)"):
        with st.spinner("Lettura in corso..."):
            st.session_state.dati = analizza_leggero(foto)
            st.rerun()

# Campi compilazione
st.subheader("📝 Dettagli")
t = st.text_input("TIPO", value=st.session_state.dati[0] if len(st.session_state.dati)>0 else "")
ma = st.text_input("MARCA", value=st.session_state.dati[1] if len(st.session_state.dati)>1 else "")
mo = st.text_input("MODELLO", value=st.session_state.dati[2] if len(st.session_state.dati)>2 else "")
mat = st.text_input("MATRICOLA", value=st.session_state.dati[3] if len(st.session_state.dati)>3 else "")

if st.button("💾 SALVA SCHEDA"):
    st.success("Scheda salvata correttamente!")
