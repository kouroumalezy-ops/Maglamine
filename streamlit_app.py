import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
from datetime import datetime

# CONFIGURAZIONE
st.set_page_config(page_title="Magazzino della Min", layout="wide")
genai.configure(api_key="AIzaSyCOnJQ9ueY2Bcp9nkibY6P0GpEmQ5-HvK8")

def analizza_targa(img):
    try:
        # Modello standard stabilissimo
        model = genai.GenerativeModel('gemini-1.5-flash') 
        prompt = "Analizza targa: scrivi TIPO, MARCA, MODELLO, MATRICOLA separati da virgola."
        response = model.generate_content([prompt, img])
        return response.text.split(',')
    except:
        return ["Riprova", "Riprova", "Riprova", "Riprova"]

# INTERFACCIA LAMINE KOUROUMA
st.title("📦 Magazzino della Min")
st.write("Sviluppato da: **Lamine Kourouma**")

if 'dati' not in st.session_state:
    st.session_state.dati = ["", "", "", ""]

foto = st.camera_input("Scatta foto targa")

if foto:
    img = Image.open(foto)
    if st.button("🔄 CLICCA PER COMPILARE"):
        risultato = analizza_targa(img)
        st.session_state.dati = risultato
        st.rerun()

# CAMPI DA COMPILARE
st.subheader("📝 Dettagli")
tipo = st.text_input("TIPO", value=st.session_state.dati[0])
marca = st.text_input("MARCA", value=st.session_state.dati[1])
modello = st.text_input("MODELLO", value=st.session_state.dati[2])
matricola = st.text_input("MATRICOLA", value=st.session_state.dati[3])
