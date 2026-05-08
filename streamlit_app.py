import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 1. SETUP API E PAGINA
st.set_page_config(page_title="Magazzino della Min", layout="wide")
genai.configure(api_key="AIzaSyCOnJQ9ueY2Bcp9nkibY6P0GpEmQ5-HvK8")

# Inizializzazione dati se non esistono
if 'risultato_ia' not in st.session_state:
    st.session_state.risultato_ia = ["", "", "", ""]

def analizza_targa(foto):
    try:
        # Carica e ottimizza immagine
        img = Image.open(foto)
        img.thumbnail((500, 500))
        
        # Configura modello
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Prompt super diretto
        prompt = "Analizza questa targa. Scrivi solo i valori di TIPO, MARCA, MODELLO, MATRICOLA separati da una virgola. Non aggiungere altro testo."
        
        response = model.generate_content([prompt, img])
        
        # Pulizia risposta
        dati = response.text.replace('\n', '').split(',')
        # Assicuriamoci di avere 4 elementi
        while len(dati) < 4:
            dati.append("")
        return dati
    except Exception as e:
        st.error(f"Errore durante l'analisi: {e}")
        return ["Errore", "Errore", "Errore", "Errore"]

# 2. INTERFACCIA UTENTE
st.title("📦 Magazzino della Min")
st.write("Sviluppatore: **Lamine Kourouma**")

# Caricamento Foto
foto_input = st.camera_input("📸 Scatta la foto alla targa")

if foto_input:
    # Se clicchi il tasto, esegue l'analisi e salva subito nello stato della pagina
    if st.button("🔍 AVVIA LETTURA DATI"):
        with st.spinner("Sto leggendo la targa..."):
            dati_letti = analizza_targa(foto_input)
            st.session_state.risultato_ia = dati_letti
            st.success("Lettura completata!")

st.divider()

# 3. CAMPI DI TESTO (Prendono i dati dallo stato della sessione)
st.subheader("📝 Dettagli Macchinario")

# Usiamo variabili per i campi per facilitare la lettura
dati = st.session_state.risultato_ia

tipo = st.text_input("TIPO", value=dati[0])
marca = st.text_input("MARCA", value=dati[1])
modello = st.text_input("MODELLO", value=dati[2])
matricola = st.text_input("MATRICOLA", value=dati[3])

st.divider()

if st.button("💾 CONFERMA E SALVA"):
    st.balloons()
    st.success(f"Scheda per {marca} {modello} registrata con successo!")
