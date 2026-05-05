import streamlit as st
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# 1. CONFIGURAZIONE ICONA E TITOLO
st.set_page_config(
    page_title="Maglamine Transpallet", 
    page_icon="🛒", 
    layout="wide"
)

# 2. CONFIGURAZIONE EMAIL
MIA_EMAIL = "LA_TUA_EMAIL@gmail.com" 
PASSWORD_APP = "IL_TUO_CODICE_16_LETTERE" 

def invia_email_allarme(cliente, giorni, marca):
    corpo = f"⚠️ ALLARME MAGLAMINA\n\nIl mezzo di {cliente} (Marca: {marca}) è fuori da {giorni} giorni."
    msg = MIMEText(corpo)
    msg['Subject'] = f"🚨 RITARDO: {cliente}"
    msg['From'] = MIA_EMAIL
    msg['To'] = MIA_EMAIL
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(MIA_EMAIL, PASSWORD_APP)
            server.send_message(msg)
        return True
    except:
        return False

# 3. GESTIONE DATABASE
NOME_FILE = "dati_magazzino.xlsx"
if os.path.exists(NOME_FILE):
    df = pd.read_excel(NOME_FILE)
else:
    colonne = ["Data", "Cliente", "Fornitore/Fattore", "Provenienza", "Stato", "Tipo Macchina", "Marca", "Matricola/Barcode"]
    df = pd.DataFrame(columns=colonne)

# 4. SEZIONE ALLARMI
st.subheader("🚨 Controllo Scadenze (>10 giorni)")
oggi = datetime.now()
ritardi_trovati = False

for index, riga in df.iterrows():
    if riga['Stato'] == "Muletto da prestare":
        try:
            data_uscita = datetime.strptime(riga['Data'], "%d/%m/%Y %H:%M")
            giorni_passati = (oggi - data_uscita).days
            if giorni_passati >= 10:
                ritardi_trovati = True
                c_a, c_b = st.columns([3, 1])
                c_a.error(f"⚠️ {riga['Cliente']} - Fuori da {giorni_passati} giorni")
                if c_b.button(f"📧 Avvisami via Mail", key=f"m_{index}"):
                    if invia_email_allarme(riga['Cliente'], giorni_passati, riga['Marca']):
                        st.success("Mail inviata!")
                    else:
                        st.error("Errore Mail: controlla Password App")
        except:
            continue
if not ritardi_trovati:
    st.success("✅ Nessun mezzo in ritardo.")

st.write("---")

# 5. INTERFACCIA DI REGISTRAZIONE
st.title("🏗️ Registro Maglamina")
col1, col2 = st.columns([1, 2])

with col1:
    foto = st.camera_input("Foto Mezzo")

with col2:
    cliente = st.text_input("👤 Cliente")
    fornitore = st.text_input("🏢 Fornitore")
    provenienza = st.text_input("📍 Provenienza")
    stati = ["In Deposito", "In Riparazione", "Muletto da prestare", "Noleggio", "Rientro"]
    stato = st.selectbox("🚦 Stato", stati)
    tipo = st.text_input("🚜 Tipo (es. Transpallet)")
    marca = st.text_input("🏷️ Marca")
    barcode = st.text_input("🔢 Matricola / Barcode")

    if st.button("✅ SALVA REGISTRAZIONE", use_container_width=True):
        nuovo_dato = {
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Cliente": cliente, "Fornitore/Fattore": fornitore, "Provenienza": provenienza,
            "Stato": stato, "Tipo Macchina": tipo, "Marca": marca, "Matricola/Barcode": barcode
        }
        df = pd.concat([df, pd.DataFrame([nuovo_dato])], ignore_index=True)
        df.to_excel(NOME_FILE, index=False)
        st.success("Salvato correttamente!")
        st.rerun()

st.write("---")
st.subheader("📊 Registro Completo")
st.dataframe(df, use_container_width=True)

# 6. FIRMA FINALE
st.write("---")
st.markdown(
    """
    <div style='text-align: center;'>
        <p style='color: #555; font-size: 0.9em;'>
            📦 <b>Sistema Gestione Transpallet Maglamina</b><br>
            Sviluppato con orgoglio da <b>Lamine Kourouma</b> v1.0
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)
