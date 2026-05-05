import streamlit as st
import pandas as pd
import os
from datetime import datetime
# --- CONFIGURAZIONE LOGO ---
st.set_page_config(page_title="Maglamine", page_icon="image_29.png")

col1, col2 = st.columns([1, 4])
with col1:
    # Sostituisci la vecchia riga 10 con questo:
foto_macchina = st.camera_input("Scansiona o fotografa la macchina")

if foto_macchina:
    st.image(foto_macchina, caption="Macchina rilevata correttamente")
    st.success("Foto acquisita! Ora compila i dati qui sotto per il magazzino.")

with col2:
    st.title("Gestione Maglamine")
st.write("---")
# ---------------------------


# Password per la tua privacy
PASSWORD_ACCESSO = "1234" 

def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if not st.session_state["password_correct"]:
        pwd = st.text_input("Inserisci la Password", type="password")
        if pwd == PASSWORD_ACCESSO:
            st.session_state["password_correct"] = True
            st.rerun()
        return False
    return True

if check_password():
    NOME_FILE = "dati_magazzino.xlsx"
    if os.path.exists(NOME_FILE):
        df = pd.read_excel(NOME_FILE)
    else:
        df = pd.DataFrame(columns=["Barcode", "Tipo", "Marca", "Gruppi", "Data_Ingresso", "Zona", "Stato"])

    st.title("☕ Magazzino Maglamina")
    menu = st.sidebar.selectbox("Menu", ["Dashboard", "Nuovo Ingresso"])

    if menu == "Nuovo Ingresso":
        with st.form("nuovo_pezzo"):
            barcode = st.text_input("Barcode/Seriale")
            tipo = st.selectbox("Attrezzatura", ["Macchina Caffè", "Lavastoviglie", "Fabbricatore Ghiaccio", "Muletto TC", "Detersivi"])
            marca = st.text_input("Marca")
            gruppi = st.number_input("Gruppi", 0, 4, 1)
            zona = st.selectbox("Scaffale", ["ILLY-A", "ILLY-B", "OFFICINA", "ROTAZIONE", "MAGAZZINO"])
            stato = st.selectbox("Stato", ["In Attesa", "In Riparazione", "Pronto", "Da Reso"])
            
            if st.form_submit_button("SALVA"):
                nuova_riga = {"Barcode": barcode, "Tipo": tipo, "Marca": marca, "Gruppi": gruppi, "Data_Ingresso": datetime.now().strftime("%d/%m/%Y"), "Zona": zona, "Stato": stato}
                df = pd.concat([df, pd.DataFrame([nuova_riga])], ignore_index=True)
                df.to_excel(NOME_FILE, index=False)
                st.success("Salvato correttamente nel tuo Excel!")

    elif menu == "Dashboard":
        st.subheader("Giacenze Attuali")
        st.dataframe(df)
        if not df.empty:
            with open(NOME_FILE, "rb") as f:
                st.download_button("📥 Scarica File Excel", f, file_name=NOME_FILE)
