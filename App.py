import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Annales Lab Chimie", layout="wide")

# --- STYLE CSS ---
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@800;900&family=Permanent+Marker&family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    
    <style>
        .credits-compact {
            font-size: 0.85rem; color: #555; text-align: center;
            border-bottom: 1px solid #eee; padding-bottom: 10px;
            margin-bottom: 30px; font-family: 'Roboto', sans-serif;
        }
        .logo-graphic-container {
            text-align: center; margin-bottom: 45px; padding: 25px 40px 15px 40px; 
            background: linear-gradient(165deg, rgba(255, 154, 68, 0.05) 0%, rgba(252, 96, 118, 0.08) 100%);
            border-radius: 50px 15px 70px 20px; display: inline-block;
            position: relative; left: 50%; transform: translateX(-50%);
        }
        .logo-text-base { font-family: 'Poppins', sans-serif !important; font-weight: 900 !important; text-transform: uppercase; letter-spacing: -2px; line-height: 0.85; margin: 0; display: inline-block; }
        .logo-annales { font-size: 4rem !important; color: #2c3e50; position: relative; z-index: 1; }
        .logo-lab-badged {
            font-family: 'Permanent Marker', cursive !important; font-size: 1.7rem !important;
            color: #ffffff; background: linear-gradient(135deg, #ff9a44 0%, #fc6076 100%); 
            padding: 2px 14px; border-radius: 40px; position: absolute;
            top: 48px; right: 25px; transform: rotate(-10deg); z-index: 2;
        }
        .logo-chimie {
            font-size: 3.5rem !important; background: linear-gradient(135deg, #1f77b4 0%, #3498db 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .logo-sub-dynamic { font-family: 'Roboto', sans-serif !important; font-size: 0.9rem !important; color: #95a5a6; text-transform: uppercase; letter-spacing: 5px; margin-top: 8px; }
        
        /* --- NOUVEAU : ANIMATION DU BOUTON SIDEBAR --- */
        [data-testid="stSidebarCollapseIcon"] {
            background-color: #fc6076 !important;
            color: white !important;
            border-radius: 50% !important;
            padding: 5px !important;
            animation: pulse-red 2s infinite;
        }
        @keyframes pulse-red {
            0% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(252, 96, 118, 0.7); }
            70% { transform: scale(1.1); box-shadow: 0 0 0 10px rgba(252, 96, 118, 0); }
            100% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(252, 96, 118, 0); }
        }

        .cpge-warning { font-size: 0.85rem; color: #666; font-style: italic; margin-top: -10px; }
    </style>
    """, unsafe_allow_html=True)

# ... (Le reste des fonctions de chargement reste inchangé) ...

# --- AFFICHAGE ---
st.markdown('<div class="credits-compact"><b>Sylvain Betoule</b> • <b>Ulysse Garnier</b> • <b>Morgane Leite</b></div>', unsafe_allow_html=True)

st.markdown("""
    <div class="logo-graphic-container">
        <span class="logo-text-base logo-annales">Annales</span>
        <span class="logo-lab-badged">Lab</span>
        <span class="logo-text-base logo-chimie">Chimie</span>
        <p class="logo-sub-dynamic">Trouvez le sujet sur mesure</p>
    </div>
    """, unsafe_allow_html=True)

# Bouton d'appel visuel pour les filtres (utile sur mobile)
st.button("⚙️ Configurer les thèmes et difficultés (Barre latérale ⬅️)", use_container_width=True)

with st.expander("👋 Comment utiliser cet outil ?", expanded=True):
    c1, c2, c3 = st.columns(3)
    # ... (Blocs d'aide inchangés) ...
