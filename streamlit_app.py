import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. SETUP - Usiamo la configurazione più semplice
st.set_page_config(page_title="Magazzino della Min")
genai.configure(api_key="AIzaSyCOnJQ9ueY2Bcp9nkibY6P0GpEmQ5-HvK8")

# Inizializziamo i dati nella memoria dell'app
if 'dati_letti' not in st.session_state:
    st.session_state.dati_letti = ["", "", "", ""]

def leggi_targa(immagine):
    try:
        # Usiamo il modello 'gemini-1.5-flash' ma senza beta nel codice
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Chiediamo solo i testi separati da virgola
        prompt = "Estrai dalla targa i valori: TIPO, MARCA, MODELLO, MATRICOLA. Scrivili separati solo da una virgola, senza altro testo."
        
        img = Image.open(immagine)
        img.thumbnail((600, 600)) # Rimpiccioliamo per velocità
        
        response = model.generate_content([prompt, img])
        testo = response.text.strip()
        
        # Dividiamo la risposta in 4 parti
        risultato = [x.strip() for x in testo.split(',')]
        while len(risultato) < 4: risultato.append("")
        return risultato
    except Exception as e:
        st.error(f"Errore: {e}")
        return ["", "", "", ""]

# 2. INTERFACCIA
st.title("📦 Magazzino della Min")
st.write("Sviluppatore: **Lamine Kourouma**")

foto = st.camera_input("Inquadra la targa")

if foto:
    if st.button("🔍 CLICCA QUI PER COMPILARE"):
        with st.spinner("Analisi in corso..."):
            dati = leggi_targa(foto)
            st.session_state.dati_letti = dati
            st.rerun()

st.divider()

# 3. CAMPI CHE SI RIEMPIONO
st.subheader("Dettagli Macchina")
# Assegniamo i valori letti alle caselle
tipo = st.text_input("TIPO", value=st.session_state.dati_letti[0])
marca = st.text_input("MARCA", value=st.session_state.dati_letti[1])
modello = st.text_input("MODELLO", value=st.session_state.dati_letti[2])
matricola = st.text_input("MATRICOLA", value=st.session_state.dati_letti[3])

if st.button("💾 SALVA SCHEDA"):
    st.success("Dati salvati!")
