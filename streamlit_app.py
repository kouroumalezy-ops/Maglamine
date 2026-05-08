import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 1. SETUP - Cambiamo la versione dell'API internamente
st.set_page_config(page_title="Magazzino della Min", layout="wide")
genai.configure(api_key="AIzaSyCOnJQ9ueY2Bcp9nkibY6P0GpEmQ5-HvK8")

# Inizializzazione sicura dei dati
if 'risultato_ia' not in st.session_state:
    st.session_state.risultato_ia = ["", "", "", ""]

def analizza_targa_stabile(foto):
    try:
        img = Image.open(foto)
        img.thumbnail((500, 500))
        
        # PROVIAMO IL MODELLO PIÙ COMPATIBILE IN ASSOLUTO
        model = genai.GenerativeModel('gemini-pro-vision')
        
        prompt = "Analizza targa: scrivi TIPO, MARCA, MODELLO, MATRICOLA separati da virgola."
        
        response = model.generate_content([prompt, img])
        
        # Pulizia della risposta per evitare errori di formattazione
        testo = response.text.strip()
        dati = [v.strip() for v in testo.split(',')]
        
        while len(dati) < 4:
            dati.append("")
        return dati
    except Exception as e:
        # Se il modello pro-vision non è disponibile, forziamo l'ultimo tentativo col flash standard
        try:
            model_flash = genai.GenerativeModel('gemini-1.5-flash')
            response = model_flash.generate_content(["Estrai TIPO, MARCA, MODELLO, MATRICOLA da questa targa, separati da virgola", img])
            return [v.strip() for v in response.text.split(',')]
        except:
            st.error("Errore di connessione ai server Google. Riprova tra un istante.")
            return ["", "", "", ""]

# 2. INTERFACCIA
st.title("📦 Magazzino della Min")
st.write("Sviluppatore: **Lamine Kourouma**")

foto_input = st.camera_input("📸 Scatta la foto alla targa")

if foto_input:
    if st.button("🔍 AVVIA LETTURA DATI"):
        with st.spinner("Lettura in corso..."):
            dati_letti = analizza_targa_stabile(foto_input)
            st.session_state.risultato_ia = dati_letti
            st.rerun() # Forza l'aggiornamento immediato delle caselle

st.divider()

# 3. CASSETTE DI TESTO
dati = st.session_state.risultato_ia
st.text_input("TIPO", value=dati[0])
st.text_input("MARCA", value=dati[1])
st.text_input("MODELLO", value=dati[2])
st.text_input("MATRICOLA", value=dati[3])
