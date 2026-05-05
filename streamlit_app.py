import streamlit as st
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

st.set_page_config(page_title="Maglamine Pro", page_icon="🏗️", layout="wide")

# --- CONFIGURAZIONE EMAIL ---
# Sostituisci qui con la tua gmail e la password a 16 lettere di Google
MIA_EMAIL = "LA_TUA_EMAIL@gmail.com" 
PASSWORD_APP = "IL_TUO_CODICE_16_LETTERE" 

def invia_email_allarme(cliente, giorni, marca):
    corpo = f"⚠️ ALLARME MAGLAMINA\n\nIl muletto di {cliente} (Marca: {marca}) è fuori da {giorni} giorni e non è ancora rientrato."
    msg = MIMEText(corpo)
    msg['Subject'] = f"🚨 RITARDO MULETTO: {cliente}"
    msg['From'] = MIA_EMAIL
    msg['To'] = MIA_EMAIL
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(MIA_EMAIL, PASSWORD_APP)
            server.send_message(msg)
        return True
    except:
        return False

# --- GESTIONE DATABASE ---
NOME_FILE = "dati_magazzino.xlsx"
if os.path.exists(NOME_FILE):
    df = pd.read_excel(NOME_FILE)
else:
    colonne = ["Data", "Cliente", "Fornitore/Fattore", "Provenienza", "Stato", "Tipo Macchina", "Marca", "Matricola/Barcode"]
    df = pd.DataFrame(columns=colonne)

# --- SEZIONE ALLARMI (In cima all'app) ---
st.subheader("🚨 Controllo Scadenze Muletti (>10 giorni)")
oggi = datetime.now()
ritardi_trovati = False

for index, riga in df.iterrows():
    if riga['Stato'] == "Muletto da prestare":
        try:
            data_uscita = datetime.strptime(riga['Data'], "%d/%m/%Y %H:%M")
            giorni_passati = (oggi - data_uscita).days
            
            if giorni_passati >= 10:
                ritardi_trovati = True
                col_a, col_b = st.columns([3, 1])
                col_a.error(f"⚠️ {riga['Cliente']} - Fuori da {giorni_passati} giorni")
                if col_b.button(f"📧 Avvisami via Mail", key=f"mail_{index}"):
                    if invia_email_allarme(riga['Cliente'], giorni_passati, riga['Marca']):
                        st.success("Notifica inviata alla tua email!")
                    else:
                        st.error("Configura la Password App per le mail")
        except:
            continue
if not ritardi_trovati:
    st.success("✅ Nessun muletto in ritardo al momento.")

st.write("---")

# --- INTERFACCIA DI INSERIMENTO ---
st.title("🏗️ Gestione Magazzino Maglamina")
c1, c2 = st.columns([1, 2])

with c1:
    foto = st.camera_input("Foto Macchina")

with c2:
    cliente = st.text_input("👤 Nome del Cliente")
    fornitore = st.text_input("🏢 Fornitore / Fattore")
    provenienza = st.text_input("📍 Luogo di Provenienza")
    stato = st.selectbox("🚦 Stato", ["In Deposito", "In Riparazione", "Muletto da prestare", "Macchina da noleggiare", "Rientro"])
    tipo = st.text_input("🚜 Tipo Macchina")
    marca = st.text_input("🏷️ Marca")
    barcode = st.text_input("🔢 Matricola / Barcode")

    if st.button("✅ SALVA NEL REGISTRO", use_container_width=True):
        nuova_riga = {
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Cliente": cliente, "Fornitore/Fattore": fornitore, "Provenienza": provenienza,
            "Stato": stato, "Tipo Macchina": tipo, "Marca": marca, "Matricola/Barcode": barcode
        }
        df = pd.concat([df, pd.DataFrame([nuova_riga])], ignore_index=True)
        df.to_excel(NOME_FILE, index=False)
        st.success("Dati salvati!")
        st.rerun()

st.write("---")
st.subheader("📊 Registro Storico")
st.dataframe(df, use_container_width=True)


