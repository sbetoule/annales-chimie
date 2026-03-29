import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Annales Lab Chimie", layout="wide")

# --- STYLE CSS (LOGO, CRÉDITS, EXPANDERS) ---
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@800;900&family=Permanent+Marker&family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    
    <style>
        /* Masquer la barre d'outils Streamlit */
        header[data-testid="stHeader"] { display: none !important; }

        /* --- STYLE DES RÉSULTATS (EXPANDER) --- */
        
        /* Titre principal (Nom du sujet) */
        .stExpander summary p {
            font-size: 1rem !important;
            color: #2c3e50 !important;
            font-weight: 700 !important;
        }

        /* Thèmes injectés via span */
        .sujet-themes {
            color: #888 !important;
            font-weight: 400 !important;
            font-size: 0.85rem !important;
            margin-left: 8px;
            display: inline-block;
        }

        .stExpander {
            border: none !important;
            border-bottom: 1px solid #f0f0f0 !important;
        }
        
        .stExpander:focus, .stExpander:active {
            outline: none !important;
            box-shadow: none !important;
        }

        /* --- INTERFACE ET LOGO --- */
        .block-container { padding-top: 1.5rem !important; }
        
        .credits-compact {
            font-size: 0.85rem; color: #555; text-align: center;
            border-bottom: 1px solid #eee; padding-bottom: 10px;
            margin-bottom: 30px; font-family: 'Roboto', sans-serif;
        }
        
        .logo-graphic-container {
            text-align: center; margin-bottom: 45px; padding: 25px 40px 5px 40px; 
            background: linear-gradient(165deg, rgba(255, 154, 68, 0.05) 0%, rgba(252, 96, 118, 0.08) 100%);
            border-radius: 50px 15px 70px 20px; display: inline-block;
            position: relative; left: 50%; transform: translateX(-50%);
        }
        
        .logo-text-base { font-family: 'Poppins', sans-serif !important; font-weight: 900 !important; text-transform: uppercase; letter-spacing: -2px; line-height: 0.85; margin: 0; display: inline-block; }
        .logo-annales { font-size: 4rem !important; color: #2c3e50; }
        .logo-lab-badged {
            font-family: 'Permanent Marker', cursive !important; font-size: 1.7rem !important;
            color: #ffffff; background: linear-gradient(135deg, #ff9a44 0%, #fc6076 100%); 
            padding: 2px 14px; border-radius: 40px; position: absolute;
            top: 48px; right: 25px; transform: rotate(-10deg);
        }
        .logo-chimie {
            font-size: 3.5rem !important; background: linear-gradient(135deg, #1f77b4 0%, #3498db 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; display: block;
        }
        .logo-sub-dynamic { font-family: 'Roboto', sans-serif !important; font-size: 0.9rem !important; color: #95a5a6; text-transform: uppercase; letter-spacing: 5px; margin-top: 8px; }
        
        [data-testid="stSidebarCollapseIcon"] { background-color: #fc6076 !important; color: white !important; border-radius: 50% !important; animation: pulse-red 2s infinite; }
        
        @keyframes pulse-red {
            0% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(252, 96, 118, 0.7); }
            70% { transform: scale(1.1); box-shadow: 0 0 0 10px rgba(252, 96, 118, 0); }
            100% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(252, 96, 118, 0); }
        }
        
        .stSlider [data-baseweb="slider"] div[role="presentation"] div { background-color: #fc6076 !important; }
        .stSlider [data-baseweb="slider"] div[role="slider"] { background-color: #fc6076 !important; border: 2px solid white !important; }
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
    except: return ["Erreur"], ["facile", "moyen", "difficile"]

with st.spinner("Initialisation des thématiques..."):
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
            questions = questions[questions['Thème'].astype(str).str.lower() != "thème"]
            sujets.append({"nom": str(nom_sujet).strip(), "annee": str(annee).strip(), "questions": questions})
        return sujets
    except: return []

# --- AFFICHAGE HEADER ---
st.markdown("""
<div class="credits-compact">
    <span class="credits-qsn">Qui sommes-nous ?</span>
    <b>Sylvain Betoule</b> (Doctorant, Sorbonne Univ.) • 
    <b>Ulysse Garnier</b> (Doctorant, Sorbonne Univ.) • 
    <b>Morgane Leite</b> (Resp. prépa agrégation de chimie, ENS)
</div>
<div class="logo-graphic-container">
    <span class="logo-text-base logo-annales">Annales</span>
    <span class="logo-lab-badged">Lab</span>
    <span class="logo-text-base logo-chimie">Chimie</span>
    <p class="logo-sub-dynamic">Trouvez le sujet sur mesure</p>
</div>
""", unsafe_allow_html=True)

with st.expander("👋 Comment utiliser cet outil ?", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown("**1. Filtres**"); st.info("⬅️ Utilisez la barre latérale.")
    with c2: st.markdown("**2. Recherche**"); st.info("🔎 Cliquez sur lancer la recherche.")
    with c3: st.markdown("**3. Analyse**"); st.info("⬇️ Les questions ciblées sont en bleu.")
    st.markdown("<p class='cpge-warning'>⚠️ La liste des thématiques correspond au programme de CPGE. Les niveaux sont indicatifs.</p>", unsafe_allow_html=True)

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.header("⚙️ Filtres")
    criteres = []
    niveaux_lower = [n.lower().strip() for n in NIVEAUX_ORDRE]
    try: s_idx, e_idx = niveaux_lower.index("facile"), niveaux_lower.index("difficile")
    except: s_idx, e_idx = 0, len(NIVEAUX_ORDRE) - 1

    for n in range(st.session_state.nb_filtres):
        if n > 0: st.divider()
        t = st.selectbox(f"Thème", THEMES_LISTE, key=f"t_{n}")
        d_range = st.select_slider(f"Difficulté", options=NIVEAUX_ORDRE, value=(NIVEAUX_ORDRE[s_idx], NIVEAUX_ORDRE[e_idx]), key=f"d_{n}")
        m = st.number_input(f"Quantité min.", min_value=1, value=1, key=f"m_{n}")
        criteres.append({"theme": t, "diff_range": d_range, "min": m})

    col1, col2 = st.columns(2)
    if col1.button("➕ Ajouter"): st.session_state.nb_filtres += 1; st.rerun()
    if col2.button("🗑️ Effacer") and st.session_state.nb_filtres > 1: st.session_state.nb_filtres -= 1; st.rerun()

# --- LOGIQUE DE RECHERCHE ---
if st.button("🔎 Lancer la recherche d'annales", type="primary", use_container_width=True):
    with st.spinner("Analyse en cours..."):
        data = charger_donnees(URL_CSV)
        trouves = []
        for s in data:
            q = s['questions']
            valid = True
            stats = []
            themes_sujet = q['Thème'].astype(str).str.strip().str.lower()
            difficultes_sujet = q['Difficulté'].astype(str).str.strip().str.lower()

            for c in criteres:
                theme_recherche = str(c['theme']).strip().lower()
                try:
                    idx_start = NIVEAUX_ORDRE.index(c['diff_range'][0])
                    idx_end = NIVEAUX_ORDRE.index(c['diff_range'][1])
                    n_acc = [n.lower().strip() for n in NIVEAUX_ORDRE[idx_start : idx_end + 1]]
                except: n_acc = [n.lower().strip() for n in NIVEAUX_ORDRE]

                mask_theme = themes_sujet.str.contains(theme_recherche, regex=False, na=False)
                mask_diff = difficultes_sujet.isin(n_acc)
                count = len(q[mask_theme & mask_diff])
                stats.append(f"{c['theme']} ({count})")
                if count < c['min']:
                    valid = False
                    break 

            if valid:
                s['stats'] = " | ".join(stats)
                trouves.append(s)
        
        trouves.sort(key=lambda x: x['nom'].lower())
        st.session_state.resultats_recherche = sorted(trouves, key=lambda x: x['annee'], reverse=True)

# --- RÉSULTATS ---
if st.session_state.resultats_recherche:
    nb = len(st.session_state.resultats_recherche)
    st.success(f"✅ {nb} {'sujet trouvé' if nb == 1 else 'sujets trouvés'}")

    for idx, r in enumerate(st.session_state.resultats_recherche):
        titre_html = f"{r['nom']} ({r['annee']}) <span class='sujet-themes'> • {r['stats']}</span>"
        
        with st.expander(titre_html):
            nom_comp = r['nom'].lower()
            lien = None
            if "présélection icho" in nom_comp: lien = "https://www.sciencesalecole.org/olympiades-internationales-de-chimie-ressources/"
            elif "agrégation externe spéciale" in nom_comp: lien = "https://agregation-chimie.fr/index.php/composition-de-physique-chimie/annales-des-epreuves-ecrites"
            elif "agrégation externe" in nom_comp: lien = "https://agregation-chimie.fr/index.php/les-epreuves-ecrites/annales-des-epreuves-ecrites"
            elif "capes" in nom_comp: lien = "http://b.louchart.free.fr/Concours_et_examens/CAPES/CAPES_externe_Physique_Chimie/Sujets_et_corriges_ecrits.htmls"

            if lien: st.link_button("📄 Lien vers le sujet", lien, type="secondary")

            def highlight_rows(row):
                for c in criteres:
                    try:
                        n_acc = NIVEAUX_ORDRE[NIVEAUX_ORDRE.index(c['diff_range'][0]) : NIVEAUX_ORDRE.index(c['diff_range'][1]) + 1]
                    except: n_acc = NIVEAUX_ORDRE
                    if c['theme'].lower() in str(row['Thème']).lower() and str(row['Difficulté']).strip() in n_acc:
                        return ['background-color: #d1e7ff; color: black'] * len(row)
                return [''] * len(row)

            st.dataframe(r['questions'].style.apply(highlight_rows, axis=1), use_container_width=True, hide_index=True)
elif st.session_state.resultats_recherche == []:
    st.warning("Aucun résultat.")
