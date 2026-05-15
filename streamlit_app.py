
import streamlit as st
import pandas as pd

# 1. Configurazione Pagina - DEVE ESSERE LA PRIMA RIGA
st.set_page_config(
    page_title="Lamine AI",
    page_icon="🏗️",
    layout="wide"
)

# URL LOGO
LOGO_URL = "https://raw.githubusercontent.com/kouroumalezy-ops/Maglamine/main/IMG_0407.png"

# 2. Iniezione CSS e Meta Tags per iPhone (Corretto per non mostrare scritte)
st.markdown(f"""
    <style>
        /* Nasconde scritte residue e imposta lo sfondo */
        .stApp {{
            background-color: #f4f7f6;
        }}
        .brand-title {{
            color: #d4af37;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            font-size: 32px;
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
    </style>
    
    <!-- Istruzioni segrete per iPhone -->
    <link rel="apple-touch-icon" href="{LOGO_URL}">
    <meta name="apple-mobile-web-app-title" content="Lamine AI">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    """, unsafe_allow_html=True)

# 3. Intestazione
col_logo, col_text = st.columns([1, 4])
with col_logo:
    # Metodo sicuro per mostrare il logo senza errori MediaFile
    st.markdown(f'<img src="{LOGO_URL}" width="85" style="border-radius:15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
with col_text:
    st.markdown('<p class="brand-title">LAMINE AI</p>', unsafe_allow_html=True)
    st.caption("Logistica Integrata | Magazzino & Assistenza")

# 4. Menu Reparti
tab_ass, tab_caff, tab_mez, tab_dep = st.tabs([
    "🛠️ ASSISTENZA", "☕ CAFFÈ", "🚜 MEZZI", "📦 DEPOSITO"
])

with tab_ass:
    st.subheader("🛠️ Registro Officina")
    st.info("Monitoraggio macchine presenti oltre 90 giorni.")
    df_ass = pd.DataFrame({
        "Ingresso": ["12/05/2024"],
        "Cliente": ["Hotel Roma"],
        "Macchina": ["Lavastoviglie C50"],
        "Tecnico": ["Lamine"]
    })
    st.dataframe(df_ass, use_container_width=True)

with tab_caff:
    st.subheader("☕ Gestione Reparto Caffè")
    cliente = st.selectbox("Seleziona il Torrefattore", [
        "Lavazza", "Ross Caffè", "Bonanni", "La Genovese", "Costadoro", "Altro"
    ])
    st.text_input("Modello Macchina")
    st.camera_input("Scansiona Targa Tecnica", key="cam_caff")
    if st.button("Salva Scheda Caffè"):
        st.success(f"Dati per {cliente} salvati!")

with tab_mez:
    st.subheader("🚜 Stato Parco Mezzi")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Muletti Liberi", "3")
    with c2:
        st.metric("In Noleggio", "1")
    st.button("Aggiorna Stato Mezzi")

with tab_dep:
    st.subheader("📦 Gestione Deposito")
    st.file_uploader("Carica Excel Inventario", type=["xlsx"])
    if st.button("Sincronizza Magazzino"):
        st.balloons()
        st.success("Database sincronizzato!")

