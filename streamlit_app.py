 import streamlit as st
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

st.set_page_config(page_title="Maglamine Transpallet", page_icon="🛒", layout="wide")

MIA_EMAIL = "LA_TUA_EMAIL@gmail.com" 
PASSWORD_APP = "IL_TUO_CODICE_16_LETTERE" 
def invia_email_allarme(cliente, giorni, marca):
    corpo = f"⚠️ ALLARME: {cliente} fuori da {giorni} giorni."
    msg = MIMEText(corpo)
    msg['Subject'] = f"🚨 RITARDO: {cliente}"
    msg['From'] = MIA_EMAIL
    msg['To'] = MIA_EMAIL
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(MIA_EMAIL, PASSWORD_APP)
            server.send_message(msg)
        return True
    except: return False

NOME_FILE = "dati_magazzino.xlsx"
if os.path.exists(NOME_FILE):
    df = pd.read_excel(NOME_FILE)
else:
    df = pd.DataFrame(columns=["Data", "Cliente", "Fornitore/Fattore", "Provenienza", "Stato", "Tipo Macchina", "Marca", "Matricola/Barcode"])

st.subheader("🚨 Controllo Scadenze (>10 giorni)")
oggi = datetime.now()
for index, riga in df.iterrows():
    if riga['Stato'] == "Muletto da prestare":
        try:
            data_uscita = datetime.strptime(riga['Data'], "%d/%m/%Y %H:%M")
            g = (oggi - data_uscita).days
            if g >= 10:
                st.error(f"⚠️ {riga['Cliente']} - {g} giorni")
                if st.button(f"📧 Mail", key=f"m_{index}"):
                    invia_email_allarme(riga['Cliente'], g, riga['Marca'])
        except: continue

st.title("🏗️ Registro Maglamina")
foto = st.camera_input("Foto Mezzo")
cliente = st.text_input("👤 Cliente")
stato = st.selectbox("🚦 Stato", ["In Deposito", "In Riparazione", "Muletto da prestare", "Noleggio", "Rientro"])
tipo = st.text_input("🚜 Tipo")
marca = st.text_input("🏷️ Marca")
barcode = st.text_input("🔢 Matricola")

if st.button("✅ SALVA"):
    nuovo = {"Data": datetime.now().strftime("%d/%m/%Y %H:%M"), "Cliente": cliente, "Stato": stato, "Tipo Macchina": tipo, "Marca": marca, "Matricola/Barcode": barcode}
    df = pd.concat([df, pd.DataFrame([nuovo])], ignore_index=True)
    df.to_excel(NOME_FILE, index=False)
    st.success("Salvato!")
    st.rerun()

st.dataframe(df, use_container_width=True)
st.markdown(f"--- \n <div style='text-align: center;'>Sviluppato da **Lamine Kourouma**</div>", unsafe_allow_html=True)
