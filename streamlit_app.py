import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Maglamine", page_icon="📦")

# --- GESTIONE DATI ---
NOME_FILE = "dati_magazzino.xlsx"
if os.path.exists(NOME_FILE):
    df = pd.read_excel(NOME_FILE)
else:
    df = pd.DataFrame(columns=["Barcode", "Tipo", "Marca", "Data"])

# --- INTERFACCIA APP ---
st.title("📦 Gestione Magazzino Maglamina")

col1, col2 = st.columns([1, 2])

with col1:
    foto = st.camera_input("Scatta foto macchina")

with col2:
    tipo = st.text_input("Tipo Macchina")
    marca = st.text_input("Marca")
    barcode = st.text_input("Codice / Barcode")
    
    if st.button("💾 Salva nel Magazzino"):
        nuova_riga = {
            "Barcode": barcode, 
            "Tipo": tipo, 
            "Marca": marca, 
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        df = pd.concat([df, pd.DataFrame([nuova_riga])], ignore_index=True)
        df.to_excel(NOME_FILE, index=False)
        st.success("Dato salvato con successo!")
        st.rerun()

st.write("---")
st.write("### 📊 Registro Macchine")
st.dataframe(df, use_container_width=True)
