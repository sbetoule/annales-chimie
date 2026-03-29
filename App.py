import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Annales Lab Chimie", layout="wide")

# --- STYLE CSS (LOGO, CRÉDITS, ANIMATION MOBILE) ---
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@800;900&family=Permanent+Marker&family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    
    <style>
        /* Masquer complètement la barre d'outils Streamlit en haut */
        header[data-testid="stHeader"] {
            display: none !important;
        }
        /* Style du texte à l'intérieur de la barre de l'expander */
        .stExpander summary p {
            font-size: 0.95rem !important;
            color: #888; /* Couleur grise par défaut pour tout le titre */
        }
        
        /* On force le début du texte (le nom du sujet) en noir et gras */
        .stExpander summary p::first-line {
            color: #2c3e50 !important;
            font-weight: 700 !important;
        }

        /* Optionnel : Enlever la bordure rouge de l'expander quand on clique dessus */
        .stExpander:focus {
            outline: none !important;
            box-shadow: none !important;
        }
        /* Ajustement de la marge pour que le texte "Qui sommes-nous" 
           ne soit pas trop collé au bord maintenant que le header est parti */
        .block-container {
            padding-top: 1.5rem !important;
        }
        /* Titres des résultats plus petits et serrés */
        .result-title {
            font-size: 1.1rem !important;
            font-weight: 700;
            margin-bottom: -5px !important;
        }
        /* Stats (sous-titre) plus discrètes */
        .result-stats {
            font-size: 0.85rem !important;
            color: #666;
            margin-bottom: 0px !important;
        }
        /* Titre de la section Détails */
        .details-title {
            font-size: 1.2rem !important;
            margin-top: 20px !important;
            color: #2c3e50;
        }
        /* Réduire l'espace des colonnes Streamlit */
        [data-testid="column"] {
            padding: 0px !important;
        }
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
        
        [data-testid="stSidebarCollapseIcon"] {
            background-color: #fc6076 !important; color: white !important; border-radius: 50% !important; padding: 5px !important; animation: pulse-red 2s infinite;
        }
        @keyframes pulse-red {
            0% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(252, 96, 118, 0.7); }
            70% { transform: scale(1.1); box-shadow: 0 0 0 10px rgba(252, 96, 118, 0); }
            100% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(252, 96, 118, 0); }
        }
        .cpge-warning { font-size: 0.85rem; color: #666; font-style: italic; margin-top: -10px; }
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
            sujets.append({"nom": str(nom_sujet).strip(), "annee": str(annee).strip(), "questions": questions, "label": f"{str(nom_sujet).strip()} ({str(annee).strip()})"})
        return sujets
    except: return []

# --- AFFICHAGE ---
st.markdown("""
<div class="credits-compact">
    <span class="credits-qsn">Qui sommes-nous ?</span>
    <b>Sylvain Betoule</b> (Doctorant, Sorbonne Univ.) • 
    <b>Ulysse Garnier</b> (Doctorant, Sorbonne Univ.) • 
    <b>Morgane Leite</b> (Resp. prépa agrégation de chimie, ENS)
</div>
""", unsafe_allow_html=True)
st.markdown("""
    <div class="logo-graphic-container">
        <span class="logo-text-base logo-annales">Annales</span>
        <span class="logo-lab-badged">Lab</span>
        <span class="logo-text-base logo-chimie">Chimie</span>
        <p class="logo-sub-dynamic">Trouvez le sujet sur mesure</p>
    </div>
    """, unsafe_allow_html=True)

with st.expander("👋 Comment utiliser cet outil ?", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**1. Filtres**"); st.info("⬅️ Utilisez la barre latérale pour choisir vos thèmes.")
    with c2:
        st.markdown("**2. Recherche**"); st.info("Cliquez sur le bouton 🔎 **Lancer la recherche**.")
    with c3:
        st.markdown("**3. Analyse**"); st.info("⬇️ Les questions ciblées apparaîtront en bleu dans les détails.")
    st.markdown("<p class='cpge-warning'>⚠️ La liste des thématiques correspond au contenu des programmes de CPGE. Des niveaux de difficulté sont indiqués par rapport à un élève de CPGE. Ces derniers sont purement indicatifs et propres à l'interprétation des concepteurs de ce site.</p>", unsafe_allow_html=True)

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
if st.button("🔎 Lancer la recherche d'annales", type="primary", use_container_width=True):
    if 'sujet_selectionne' in st.session_state:
        del st.session_state.sujet_selectionne
    with st.spinner("Analyse de la base de données en cours..."):
        data = charger_donnees(URL_CSV)
        trouves = []
        
        for s in data:
            q = s['questions']
            valid = True
            stats = []
            
            # On crée une copie propre de la colonne Thème pour éviter les espaces ou majuscules parasites
            themes_sujet = q['Thème'].astype(str).str.strip().str.lower()
            difficultes_sujet = q['Difficulté'].astype(str).str.strip().str.lower()

            for c in criteres:
                # Préparation du critère (nettoyage)
                theme_recherche = str(c['theme']).strip().lower()
                
                # Récupération de la plage de difficulté
                try:
                    idx_start = NIVEAUX_ORDRE.index(c['diff_range'][0])
                    idx_end = NIVEAUX_ORDRE.index(c['diff_range'][1])
                    n_acc = [n.lower().strip() for n in NIVEAUX_ORDRE[idx_start : idx_end + 1]]
                except:
                    n_acc = [n.lower().strip() for n in NIVEAUX_ORDRE]

                # --- LA LOGIQUE DE FILTRAGE ---
                # On vérifie si le thème recherché est contenu dans le texte de la cellule
                mask_theme = themes_sujet.str.contains(theme_recherche, regex=False, na=False)
                mask_diff = difficultes_sujet.isin(n_acc)
                
                count = len(q[mask_theme & mask_diff])
                stats.append(f"{c['theme']} ({count})")
                
                # Si le nombre de questions pour ce thème est insuffisant, on rejette le sujet
                if count < c['min']:
                    valid = False
                    break 

            if valid:
                s['stats'] = " | ".join(stats)
                trouves.append(s)
        
        # --- NOUVEAU SYSTÈME DE TRI ---
        trouves.sort(key=lambda x: x['nom'].lower()) # Tri alphabétique A-Z
        st.session_state.resultats_recherche = sorted(trouves, key=lambda x: x['annee'], reverse=True) # Tri année 2024-2000
        
# --- RÉSULTATS ET DÉTAILS ---
if st.session_state.resultats_recherche:
    nb = len(st.session_state.resultats_recherche)
    label_sujet = "sujet trouvé" if nb == 1 else "sujets trouvés"
    st.success(f"✅ {nb} {label_sujet}")

    for idx, r in enumerate(st.session_state.resultats_recherche):
        # On formate le titre de l'expander : 
        # Le nom est en gras, les thèmes sont après un point médian, en texte normal
        titre_header = f"📄 {r['nom']} ({r['annee']})  •  {r['stats']}"
        
        with st.expander(titre_header):
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
