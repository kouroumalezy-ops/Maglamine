import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURAZIONE PAGINA (Titolo che apparirà sulla Home del telefono)
st.set_page_config(
    page_title="Magazzino Lamine",
    page_icon="📦",
    layout="centered"
)

# 2. COLORI PERSONALIZZATI (Rosso e Blu)
st.markdown("""
    <style>
    /* Sfondo della barra superiore (Blu) */
    header[data-testid="stHeader"] {
        background-color: #0000FF !important;
    }
    /* Titolo principale (Blu) */
    h1 {
        color: #0000FF !important;
        font-family: 'Arial', sans-serif;
    }
    /* Pulsanti (Rosso) */
    .stButton>button {
        background-color: #FF0000 !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        height: 3em !important;
        width: 100% !important;
    }
    /* Messaggi di errore o istruzioni */
    .stAlert {
        border-left-color: #FF0000 !important;
    }
    </style>
    """, unsafe_allow_this_html=True)

# 3. CONFIGURAZIONE AI (Sostituisci con la tua chiave!)
API_KEY = "LA_TUA_API_KEY_QUI" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. FUNZIONE LOGICA
def analizza_targa(foto):
    try:
        img = Image.open(foto)
        prompt = "Analizza questa immagine di un macchinario o targa e descrivi il contenuto."
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"Errore durante l'analisi: {e}"

# 5. INTERFACCIA UTENTE
st.title("📦 Magazzino Lamine Kourouma")
st.write("Scansiona la targa del macchinario per registrarlo.")

# Input fotocamera
foto_input = st.camera_input("Scatta una foto alla targa")

if foto_input is not None:
    st.info("Analisi in corso... attendi un istante.")
    risultato = analizza_targa(foto_input)
    
    st.subheader("Risultato Scansione:")
    st.success(risultato)

# Messaggio a fondo pagina
st.write("---")
st.caption("App creata per la gestione magazzino personalizzata.")
