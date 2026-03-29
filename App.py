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
        header[data-testid="stHeader"] { display: none !important; }
        .stExpander summary p { font-size: 1rem !important; color: #2c3e50; font-weight: 600; }
        .block-container { padding-top: 1.5rem !important; }

        /* Style Logo */
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
            top: 48px; right: 25px; transform: rotate(-10deg); z-index: 2;
        }
        .logo-chimie {
            font-size: 3.5rem !important; background: linear-gradient(135deg, #1f77b4 0%, #3498db 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; display: block;
        }
        
        [data-testid="stSidebarCollapseIcon"] { background-color: #fc6076 !important; color: white !important; border-radius: 50% !important; }
        .stSlider [data-baseweb="slider"] div[role="presentation"] div { background-color: #fc6076 !important; }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURATION DONNÉES ---
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTsADsmsMnYgQXIUlU25_FlKrtTffM5XOL69taw9Pco8AHV4suIUtT0tg384XBtBAo28qGKGbtSJtIy/pub?gid=0&single=true&output=csv"
URL_THEMES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTsADsmsMnYgQXIUlU25_FlKrtTffM5XOL69taw9Pco8AHV4suIUtT0tg384XBtBAo28qGKGbtSJtIy/pub?gid=1733310474&single=true&output=csv"
URL_NIVEAUX = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTsADsmsMnYgQXIUlU25_FlKrtTffM5XOL69taw9Pco8AHV4suIUtT0tg384XBtBAo28qGKGbtSJtIy/pub?gid=1879771001&single=true&output=csv"

@st.cache_data(ttl=60)
def recuperer_listes(url_themes, url_niveaux):
    try:
        themes = pd.read_csv(url_themes, header=None).iloc[0].dropna().astype(str).tolist()
        niveaux = pd.read_csv(url_niveaux, header=None).iloc[0].dropna().astype(str).tolist()
        return themes, niveaux
    except: return ["Erreur"], ["facile", "moyen", "difficile"]

@st.cache_data(ttl=30)
def charger_donnees(url):
    try:
        df = pd.read_csv(url, header=None, low_memory=False)
        sujets = []
        for i in range(1, df.shape[1], 4):
            nom_sujet = df.iloc[1, i]
            if pd.isna(nom_sujet) or str(nom_sujet).strip() == "": continue
            questions = df.iloc[4:, i : i+4].copy()
            questions.columns = ['Numéro', 'Thème', 'Difficulté', 'Remarque']
            questions = questions.dropna(subset=['Thème'])
            sujets.append({"nom": str(nom_sujet).strip(), "annee": str(df.iloc[2, i]).strip(), "questions": questions})
        return sujets
    except: return []

THEMES_LISTE, NIVEAUX_ORDRE = recuperer_listes(URL_THEMES, URL_NIVEAUX)

if 'resultats_recherche' not in st.session_state: st.session_state.resultats_recherche = None
if 'nb_filtres' not in st.session_state: st.session_state.nb_filtres = 1

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Filtres")
    criteres = []
    for i in range(st.session_state.nb_filtres):
        t = st.selectbox(f"Thème {i+1}", THEMES_LISTE, key=f"sel_{i}")
        d = st.select_slider(f"Difficulté {i+1}", options=NIVEAUX_ORDRE, value=(NIVEAUX_ORDRE[0], NIVEAUX_ORDRE[-1]), key=f"sld_{i}")
        m = st.number_input(f"Quantité min {i+1}", min_value=1, value=1, key=f"num_{i}")
        criteres.append({"theme": t, "diff_range": d, "min": m}) # "diff_range" pour correspondre à la suite
        st.divider()

    c1, c2 = st.columns(2)
    if c1.button("➕ Ajouter"): st.session_state.nb_filtres += 1; st.rerun()
    if c2.button("🗑️ Retirer") and st.session_state.nb_filtres > 1: st.session_state.nb_filtres -= 1; st.rerun()

# --- INTERFACE ---
st.markdown('<div class="logo-graphic-container"><span class="logo-text-base logo-annales">Annales</span><span class="logo-lab-badged">Lab</span><span class="logo-text-base logo-chimie">Chimie</span></div>', unsafe_allow_html=True)

if st.button("🔎 Lancer la recherche", type="primary", use_container_width=True):
    with st.spinner("Analyse en cours..."):
        data = charger_donnees(URL_CSV)
        trouves = []
        for s in data:
            q = s['questions']
            valid, stats = True, []
            for c in criteres:
                theme_recherche = str(c['theme']).strip().lower()
                try:
                    idx_start, idx_end = NIVEAUX_ORDRE.index(c['diff_range'][0]), NIVEAUX_ORDRE.index(c['diff_range'][1])
                    n_acc = [n.lower().strip() for n in NIVEAUX_ORDRE[idx_start : idx_end + 1]]
                except: n_acc = [n.lower().strip() for n in NIVEAUX_ORDRE]

                mask = (q['Thème'].astype(str).str.lower().str.contains(theme_recherche, na=False)) & \
                       (q['Difficulté'].astype(str).str.lower().str.strip().isin(n_acc))
                
                count = len(q[mask])
                stats.append(f"{c['theme']} ({count})")
                if count < c['min']: valid = False; break 

            if valid:
                s['stats'] = " | ".join(stats)
                trouves.append(s)
        
        st.session_state.resultats_recherche = sorted(trouves, key=lambda x: x['annee'], reverse=True)

# --- RÉSULTATS ET DÉTAILS ---
if st.session_state.resultats_recherche:
    nb = len(st.session_state.resultats_recherche)
    label_sujet = "sujet trouvé" if nb == 1 else "sujets trouvés"
    st.success(f"✅ {nb} {label_sujet}")

    for idx, r in enumerate(st.session_state.resultats_recherche):
        # On utilise une flèche ou un séparateur pour bien distinguer les deux parties
        # Le gras de l'expander s'appliquera, mais la séparation sera nette
        titre_header = f"📄 {r['nom']} ({r['annee']})  |  {r['stats']}"
        
        with st.expander(titre_header):
            # Optionnel : On rappelle le titre avec le vrai style à l'intérieur
            st.markdown(f"""
                <div style="margin-bottom: 15px;">
                    <span style="color: #2c3e50; font-weight: 700; font-size: 1.1rem;">📄 {r['nom']} ({r['annee']})</span>
                    <span style="color: #888; font-weight: 400; margin-left: 10px;">• {r['stats']}</span>
                </div>
            """, unsafe_allow_html=True)
            # --- LOGIQUE DU LIEN ---
            nom_comparaison = r['nom'].lower()
            lien_sujet = None
            if "présélection icho" in nom_comparaison:
                lien_sujet = "https://www.sciencesalecole.org/olympiades-internationales-de-chimie-ressources/"
            elif "agrégation externe spéciale" in nom_comparaison:
                lien_sujet = "https://agregation-chimie.fr/index.php/composition-de-physique-chimie/annales-des-epreuves-ecrites"
            elif "agrégation externe" in nom_comparaison:
                lien_sujet = "https://agregation-chimie.fr/index.php/les-epreuves-ecrites/annales-des-epreuves-ecrites"
            elif "capes" in nom_comparaison:
                lien_sujet = "http://b.louchart.free.fr/Concours_et_examens/CAPES/CAPES_externe_Physique_Chimie/Sujets_et_corriges_ecrits.htmls"

            if lien_sujet:
                st.link_button("📄 Lien vers le sujet", lien_sujet, type="secondary")

            # Fonction de surbrillance
            def highlight_rows(row):
                for c in criteres:
                    try:
                        i_min, i_max = NIVEAUX_ORDRE.index(c['diff_range'][0]), NIVEAUX_ORDRE.index(c['diff_range'][1])
                        n_acc = NIVEAUX_ORDRE[i_min : i_max + 1]
                    except: n_acc = NIVEAUX_ORDRE
                    if c['theme'].lower() in str(row['Thème']).lower() and str(row['Difficulté']).strip() in n_acc:
                        return ['background-color: #d1e7ff; color: black'] * len(row)
                return [''] * len(row)

            st.dataframe(r['questions'].style.apply(highlight_rows, axis=1), use_container_width=True, hide_index=True)

elif st.session_state.resultats_recherche == []:
    st.warning("Aucun résultat.")
