import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Annales Lab Chimie", layout="wide")

# --- STYLE CSS (NETTOYÉ ET SÉCURISÉ) ---
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@800;900&family=Permanent+Marker&family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    
    <style>
        /* On NE masque PLUS le header ici pour éviter les bugs d'affichage de la sidebar */

        /* Style de l'expander */
        .stExpander summary p {
            font-size: 0.95rem !important;
            color: #2c3e50;
        }

        /* Espacement du contenu principal */
        .block-container {
            padding-top: 2rem !important;
        }

        /* Credits & Logo */
        .credits-compact {
            font-size: 0.85rem; color: #555; text-align: center;
            border-bottom: 1px solid #eee; padding-bottom: 10px;
            margin-bottom: 30px; font-family: 'Roboto', sans-serif; line-height: 1.5;
        }
        .logo-graphic-container {
            text-align: center; margin-bottom: 45px; padding: 25px 40px 5px 40px; 
            background: linear-gradient(165deg, rgba(255, 154, 68, 0.05) 0%, rgba(252, 96, 118, 0.08) 100%);
            border-radius: 50px 15px 70px 20px; display: inline-block;
            position: relative; left: 50%; transform: translateX(-50%);
            box-shadow: 0 10px 30px rgba(0,0,0,0.02);
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
            background-clip: text; text-fill-color: transparent; margin-top: -5px; display: block;
        }
        .logo-sub-dynamic { font-family: 'Roboto', sans-serif !important; font-size: 0.9rem !important; color: #95a5a6; text-transform: uppercase; letter-spacing: 5px; margin-top: 8px; font-weight: 400; }
        
        /* Animation du bouton Sidebar */
        [data-testid="stSidebarCollapseIcon"] {
            background-color: #fc6076 !important; color: white !important; border-radius: 50% !important; padding: 5px !important; 
            animation: pulse-red 2s infinite;
        }
        
        @keyframes pulse-red {
            0% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(252, 96, 118, 0.7); }
            70% { transform: scale(1.1); box-shadow: 0 0 0 10px rgba(252, 96, 118, 0); }
            100% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(252, 96, 118, 0); }
        }

        /* Sliders personnalisés */
        .stSlider [data-baseweb="slider"] div[role="presentation"] div { background-color: #fc6076 !important; }
        .stSlider [data-baseweb="slider"] div[role="slider"] { background-color: #fc6076 !important; border: 2px solid white !important; }
        div[data-testid="stThumbValue"] { color: #fc6076 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURATION DONNÉES ---
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTsADsmsMnYgQXIUlU25_FlKrtTffM5XOL69taw9Pco8AHV4suIUtT0tg384XBtBAo28qGKGbtSJtIy/pub?gid=0&single=true&output=csv"
URL_THEMES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTsADsmsMnYgQXIUlU25_FlKrtTffM5XOL69taw9Pco8AHV4suIUtT0tg384XBtBAo28qGKGbtSJtIy/pub?gid=1733310474&single=true&output=csv"
URL_NIVEAUX = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTsADsmsMnYgQXIUlU25_FlKrtTffM5XOL69taw9Pco8AHV4suIUtT0tg384XBtBAo28qGKGbtSJtIy/pub?gid=1879771001&single=true&output=csv"

@st.cache_data(ttl=60)
def recuperer_listes(url_themes, url_niveaux):
    try:
        df_t = pd.read_csv(url_themes, header=None)
        themes = df_t.iloc[0].dropna().astype(str).tolist()
        df_n = pd.read_csv(url_niveaux, header=None)
        niveaux = df_n.iloc[0].dropna().astype(str).tolist()
        return themes, niveaux
    except: return ["Erreur chargement"], ["facile", "moyen", "difficile"]

THEMES_LISTE, NIVEAUX_ORDRE = recuperer_listes(URL_THEMES, URL_NIVEAUX)

if 'resultats_recherche' not in st.session_state: st.session_state.resultats_recherche = None
if 'nb_filtres' not in st.session_state: st.session_state.nb_filtres = 1

@st.cache_data(ttl=30)
def charger_donnees(url):
    try:
        df = pd.read_csv(url, header=None, low_memory=False)
        sujets = []
        for i in range(1, df.shape[1], 4):
            nom_sujet = df.iloc[1, i]
            if pd.isna(nom_sujet) or str(nom_sujet).strip() == "": continue
            annee = df.iloc[2, i]
            questions = df.iloc[4:, i : i+4].copy()
            questions.columns = ['Numéro', 'Thème', 'Difficulté', 'Remarque']
            questions = questions.dropna(subset=['Thème'])
            sujets.append({"nom": str(nom_sujet).strip(), "annee": str(annee).strip(), "questions": questions})
        return sujets
    except: return []

# --- AFFICHAGE HEADER PAGE ---
st.markdown("""
<div class="credits-compact">
    <b>Sylvain Betoule</b> • <b>Ulysse Garnier</b> • <b>Morgane Leite</b>
</div>
<div class="logo-graphic-container">
    <span class="logo-text-base logo-annales">Annales</span>
    <span class="logo-lab-badged">Lab</span>
    <span class="logo-text-base logo-chimie">Chimie</span>
    <p class="logo-sub-dynamic">Trouvez le sujet sur mesure</p>
</div>
""", unsafe_allow_html=True)

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.header("⚙️ Filtres")
    criteres = []
    
    for n in range(st.session_state.nb_filtres):
        if n > 0: st.divider()
        t = st.selectbox(f"Thème {n+1}", THEMES_LISTE, key=f"t_{n}")
        d_range = st.select_slider(f"Difficulté {n+1}", options=NIVEAUX_ORDRE, value=(NIVEAUX_ORDRE[0], NIVEAUX_ORDRE[-1]), key=f"d_{n}")
        m = st.number_input(f"Qté min. {n+1}", min_value=1, value=1, key=f"m_{n}")
        criteres.append({"theme": t, "diff_range": d_range, "min": m})

    col1, col2 = st.columns(2)
    if col1.button("➕ Ajouter"): st.session_state.nb_filtres += 1; st.rerun()
    if col2.button("🗑️ Effacer") and st.session_state.nb_filtres > 1: st.session_state.nb_filtres -= 1; st.rerun()

# --- RECHERCHE ---
if st.button("🔎 Lancer la recherche d'annales", type="primary", use_container_width=True):
    data = charger_donnees(URL_CSV)
    trouves = []
    for s in data:
        valid = True
        stats = []
        q = s['questions']
        for c in criteres:
            mask_theme = q['Thème'].astype(str).str.contains(c['theme'], case=False, na=False)
            # Logique simplifiée pour le test
            count = len(q[mask_theme])
            stats.append(f"{c['theme']} ({count})")
            if count < c['min']:
                valid = False
                break
        if valid:
            s['stats'] = " | ".join(stats)
            trouves.append(s)
    st.session_state.resultats_recherche = sorted(trouves, key=lambda x: x['annee'], reverse=True)

# --- RÉSULTATS ---
if st.session_state.resultats_recherche:
    for r in st.session_state.resultats_recherche:
        with st.expander(f"📄 {r['nom']} ({r['annee']}) | {r['stats']}"):
            st.dataframe(r['questions'], use_container_width=True, hide_index=True)
elif st.session_state.resultats_recherche == []:
    st.warning("Aucun résultat.")
