import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configurazione Pagina (Deve essere la prima riga)
st.set_page_config(
    page_title="Lamine AI",
    page_icon="🏗️",
    layout="wide"
)

# Link al logo ufficiale
LOGO_URL = "https://raw.githubusercontent.com/kouroumalezy-ops/Maglamine/main/IMG_0407.png"

# 2. Stile Grafico e Icona iPhone (Senza scritte residue)
st.markdown(f"""
    <head>
        <link rel="apple-touch-icon" href="{LOGO_URL}">
        <link rel="manifest" href="manifest.json">
        <meta name="apple-mobile-web-app-capable" content="yes">
    </head>
    <style>
    .stApp {{ background-color: #f4f7f6; }}
    .brand-title {{
        color: #d4af37;
        font-family: sans-serif;
        font-size: 38px;
        font-weight: bold;
        margin: 0;
    }}
    /* Bottoni Dorati */
    div.stButton > button {{
        background: linear-gradient(135deg, #ffcc00, #d4af37) !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        border: none !important;
        height: 3.5em !important;
        width: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    /* Tab Menu */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: white;
        padding: 10px;
        border-radius: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. Intestazione con Logo
col_logo, col_text = st.columns([1, 4])
with col_logo:
    st.markdown(f'<img src="{LOGO_URL}" width="95">', unsafe_allow_html=True)
with col_text:
    st.markdown('<p class="brand-title">LAMINE AI</p>', unsafe_allow_html=True)
    st.caption("Sistema Logistico Integrato | Magazzino & Assistenza")

# 4. Menu Reparti (Tutte le voci ripristinate)
tab_ass, tab_caff, tab_mez, tab_dep = st.tabs([
    "🛠️ ASSISTENZA", "☕ CAFFÈ", "🚜 MEZZI", "📦 DEPOSITO"
])

with tab_ass:
    st.subheader("🛠️ Registro Assistenza Officina")
    st.info("Monitoraggio macchine in giacenza oltre 90 giorni.")
    df_ass = pd.DataFrame({
        "Ingresso": ["12/05/2024"],
        "Cliente": ["Hotel Roma"],
        "Macchina": ["Lavastoviglie C50"],
        "Tecnico": ["Lamine"]
    })
    st.dataframe(df_ass, use_container_width=True)

with tab_caff:
    st.subheader("☕ Gestione Reparto Caffè")
    # Qui trovi di nuovo le caselle e la selezione
    cliente = st.selectbox("Seleziona il Torrefattore", [
        "Lavazza", "Ross Caffè", "Bonanni", "La Genovese", "Costadoro", "Altro"
    ])
    st.text_input("Modello Macchina")
    st.camera_input("Scansiona Targa Tecnica", key="caff_cam")
    if st.button("Salva Scheda Caffè"):
        st.success(f"Dati per {cliente} salvati correttamente!")

with tab_mez:
    st.subheader("🚜 Stato Parco Mezzi")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Muletti Disponibili", "3")
        st.toggle("Muletto 1.5t Libero", value=True)
    with c2:
        st.metric("In Noleggio", "1")
        st.toggle("Transpallet Libero", value=False)
    st.button("Aggiorna Disponibilità")

with tab_dep:
    st.subheader("📦 Gestione Deposito")
    st.write("Carica i documenti per Forni, Lavastoviglie e Ghiaccio.")
    up = st.file_uploader("Carica Excel Inventario", type=["xlsx"])
    if st.button("Sincronizza Database"):
        st.balloons()
        st.toast("Magazzino aggiornato!")
