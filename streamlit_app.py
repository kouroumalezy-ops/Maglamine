
import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configurazione della pagina (Deve essere la prima riga di codice)
st.set_page_config(
    page_title="Lamine AI",
    page_icon="🏗️",
    layout="wide"
)

# Link al logo
LOGO_URL = "https://raw.githubusercontent.com/kouroumalezy-ops/Maglamine/main/IMG_0407.png"

# 2. Stile Grafico - Corretto per non mostrare scritte in alto
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .brand-title {
        color: #d4af37;
        font-family: sans-serif;
        font-size: 38px;
        font-weight: bold;
        margin: 0;
    }
    /* Stile Bottoni Dorati */
    div.stButton > button {
        background: linear-gradient(135deg, #ffcc00, #d4af37) !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        border: none !important;
        height: 3em !important;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Intestazione
col_logo, col_text = st.columns([1, 4])
with col_logo:
    # Usiamo un metodo più sicuro per caricare l'immagine ed evitare l'errore MediaFile
    st.markdown(f'<img src="{LOGO_URL}" width="90">', unsafe_allow_html=True)

with col_text:
    st.markdown('<p class="brand-title">LAMINE AI</p>', unsafe_allow_html=True)
    st.caption("Logistica e Assistenza Professionale")

# 4. Contenuto App
tab1, tab2, tab3 = st.tabs(["🛠️ ASSISTENZA", "🚜 MEZZI", "📦 DEPOSITO"])

with tab1:
    st.subheader("Registro Officina")
    st.info("Monitoraggio giacenze oltre 90 giorni.")
    df = pd.DataFrame({
        "Data": ["12/05/2024"],
        "Cliente": ["Esempio Srl"],
        "Stato": ["In Lavorazione"]
    })
    st.dataframe(df, use_container_width=True)

with tab2:
    st.subheader("Gestione Mezzi")
    st.metric("Muletti Disponibili", "3")
    st.button("Aggiorna Stato Parco Mezzi")

with tab3:
    st.subheader("Magazzino")
    st.file_uploader("Carica file inventario", type=["xlsx"])
    if st.button("Sincronizza Dati"):
        st.success("Database aggiornato!")


