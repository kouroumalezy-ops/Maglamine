import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd # Per gestire i dati come una tabella

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="Magazzino Lamine", page_icon="📦", layout="centered")

# Inizializzazione della "Memoria" (Session State)
if 'storico' not in st.session_state:
    st.session_state.storico = []

# 2. COLORI PERSONALIZZATI
st.markdown("""
    <style>
    header[data-testid="stHeader"] { background-color: #0000FF !important; }
    h1 { color: #0000FF !important; }
    .stButton>button { background-color: #FF0000 !important; color: white !important; border-radius: 20px !important; width: 100% !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. CONFIGURAZIONE AI
API_KEY = "LA_TUA_API_KEY_QUI" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. INTERFACCIA UTENTE
st.title("📦 Magazzino Lamine Kourouma")

# --- NUOVO: SELEZIONE LUOGO ---
st.subheader("📍 Localizzazione")
luogo = st.selectbox("Seleziona il luogo attuale:", ["Magazzino Centrale", "Cantiere Nord", "Deposito Esterno", "Altro..."])

st.write("---")

# Scansione
st.subheader("📸 Registra Nuovo Pezzo")
foto_input = st.camera_input("Scatta una foto alla targa")

if foto_input is not None:
    with st.spinner("Analisi e registrazione in corso..."):
        try:
            img = Image.open(foto_input)
            response = model.generate_content(["Estrai modello e seriale da questa targa in modo sintetico.", img])
            dati_analizzati = response.text
            
            # Salvataggio nella memoria della sessione
            nuova_registrazione = {
                "Data": pd.Timestamp.now().strftime("%d/%m/%Y %H:%M"),
                "Luogo": luogo,
                "Dettagli": dati_analizzati
            }
            st.session_state.storico.append(nuova_registrazione)
            st.success(f"Registrato con successo in: {luogo}")
        except Exception as e:
            st.error(f"Errore: {e}")

# --- NUOVO: VISUALIZZAZIONE CAMPI REGISTRATI ---
st.write("---")
st.subheader("📂 Registro Scansioni Recenti")

if st.session_state.storico:
    df = pd.DataFrame(st.session_state.storico)
    st.table(df) # Mostra la tabella con i tuoi campi salvati
    
    if st.button("Svuota Registro"):
        st.session_state.storico = []
        st.rerun()
else:
    st.info("Nessun dato registrato in questa sessione.")

st.caption("App creata per la gestione magazzino personalizzata.")
