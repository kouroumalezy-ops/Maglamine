import streamlit as st
import pandas as pd
import os
from datetime import datetime
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURAZIONE
st.set_page_config(page_title="Maglamine AI PRO", page_icon="🏷️", layout="wide")

# Cartella per salvare le foto
CARTELLA_FOTO = "foto_mezzi"
if not os.path.exists(CARTELLA_FOTO):
    os.makedirs(CARTELLA_FOTO)

# CREDENZIALI
genai.configure(api_key="AIzaSyCOnJQ9ueY2Bcp9nkibY6P0GpEmQ5-HvK8")

def analizza_foto_completa(immagine_pil):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = """Analizza questa foto di un mezzo logistico. 
        Estrai: TIPO, MARCA, BARCODE. 
        Formato: TIPO: [nome], MARCA: [nome], BARCODE: [codice]"""
        response = model.generate_content([prompt, immagine_pil])
        return response.text.strip()
    except:
        return "TIPO: Errore, MARCA: Errore, BARCODE: Non trovato"

# 2. DATABASE
NOME_FILE = "dati_magazzino.xlsx"
if os.path.exists(NOME_FILE):
    df = pd.read_excel(NOME_FILE)
else:
    df = pd.DataFrame(columns=["Data", "Cliente", "Stato", "Tipo", "Marca", "Barcode/Matricola", "Tecnico", "Luogo", "Nome_Foto"])

# 3. INTERFACCIA
st.title("🏗️ Registro Maglamina AI + Salvataggio Foto")

col1, col2 = st.columns([1, 1])

tipo_ia, marca_ia, barcode_ia = "", "", ""
nome_file_foto = ""

with col1:
    foto = st.camera_input("📸 Scatta foto al mezzo")
    if foto:
        img = Image.open(foto)
        st.image(img, caption="Anteprima scatto", use_container_width=True)
        
        # Generiamo un nome unico per la foto basato sull'orario
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_file_foto = f"mezzo_{timestamp}.png"
        percorso_foto = os.path.join(CARTELLA_FOTO, nome_file_foto)
        
        # SALVIAMO LA FOTO FISICAMENTE
        img.save(percorso_foto)
        st.info(f"Foto salvata come: {nome_file_foto}")
        
        with st.spinner("L'IA sta leggendo i dati..."):
            risultato = analizza_foto_completa(img)
            try:
                parti = risultato.split(",")
                tipo_ia = parti[0].split("TIPO:")[1].strip()
                marca_ia = parti[1].split("MARCA:")[1].strip()
                barcode_ia = parti[2].split("BARCODE:")[1].strip()
            except:
                st.warning("IA: Rilevamento parziale.")

with col2:
    st.subheader("📋 Compila Scheda")
    cliente = st.text_input("👤 Cliente")
    tipo = st.text_input("🚜 Tipo Mezzo", value=tipo_ia)
    marca = st.text_input("🏷️ Marca", value=marca_ia)
    barcode = st.text_input("🔢 Barcode / Matricola", value=barcode_ia)
    stato = st.selectbox("🚦 Stato", ["Ritiro Tecnico", "In Deposito", "In Riparazione", "Rientro"])
    tecnico = st.text_input("👨‍🔧 Tecnico")
    luogo = st.text_input("📍 Luogo")

    if st.button("💾 SALVA TUTTO", use_container_width=True):
        nuovo = {
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Cliente": cliente, "Stato": stato, "Tipo": tipo, 
            "Marca": marca, "Barcode/Matricola": barcode, 
            "Tecnico": tecnico, "Luogo": luogo,
            "Nome_Foto": nome_file_foto # Salviamo il nome della foto nel database
        }
        df = pd.concat([df, pd.DataFrame([nuovo])], ignore_index=True)
        df.to_excel(NOME_FILE, index=False)
        st.success("Dati e Foto registrati!")
        st.rerun()

# 4. TABELLA
st.write("---")
st.subheader("📊 Archivio con riferimenti Foto")
st.dataframe(df, use_container_width=True)

# Visualizzatore foto salvate
if not df.empty:
    st.write("### 🖼️ Visualizza Foto Salvate")
    foto_da_vedere = st.selectbox("Seleziona una foto dal database:", df["Nome_Foto"].unique())
    if foto_da_vedere:
        percorso_rilettura = os.path.join(CARTELLA_FOTO, foto_da_vedere)
        if os.path.exists(percorso_rilettura):
            st.image(percorso_rilettura, width=400)
        else:
            st.error("File immagine non trovato (potrebbe essere stato resettato dal server).")
