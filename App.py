import streamlit as st
import pandas as pd

st.set_page_config(page_title="Annales Lab Chimie", layout="wide")

# --- STYLE CSS (Curseur + Logo + Tableaux) ---
st.markdown("""
    <style>
        /* Styles du Logo */
        .logo-container {
            text-align: center;
            margin-bottom: 25px;
        }
        .logo-main {
            font-size: 3.5rem !important;
            font-weight: 800 !important;
            color: #1f77b4;
            margin-bottom: 0px;
            letter-spacing: -1px;
        }
        .logo-sub {
            font-size: 1.2rem !important;
            color: #555;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-top: -10px;
        }

        /* La barre de progression du curseur (active) */
        .stSlider [data-baseweb="slider"] div[role="presentation"] div {
            background-color: #1f77b4 !important;
        }
        /* La barre de fond (inactive) */
        .stSlider [data-baseweb="slider"] div[role="presentation"] {
            background-color: #e6e6e6 !important;
            height: 6px !important;
        }
        /* Les poignées (cercles) */
        .stSlider [data-baseweb="slider"] div[role="slider"] {
            background-color: #1f77b4 !important;
            border: 2px solid white !important;
            box-shadow: 0px 2px 4px rgba(0,0,0,0.2) !important;
            height: 18px !important;
            width: 18px !important;
        }
        /* La valeur au-dessus de la poignée */
        div[data-testid="stThumbValue"] {
            color: #1f77b4 !important;
            font-weight: bold !important;
        }
        /* Supprimer les points/labels rouges automatiques */
        .stSlider [data-baseweb="slider"] div div div {
             color: transparent !important;
        }
        .stSlider [data-baseweb="slider"] div div div:last-child {
             color: #1f77b4 !important;
        }
    </style>
    """, unsafe_allow_html=True)

# --- URLS DES FLUX ---
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
    except:
        return ["Erreur"], ["facile", "moyen", "difficile"]

THEMES_LISTE, NIVEAUX_ORDRE = recuperer_listes(URL_THEMES, URL_NIVEAUX)

if 'resultats_recherche' not in st.session_state:
    st.session_state.resultats_recherche = None
if 'nb_filtres' not in st.session_state:
    st.session_state.nb_filtres = 1

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
            sujets.append({
                "nom": str(nom_sujet).strip(),
                "annee": str(annee).strip() if pd.notna(annee) else "0",
                "questions": questions,
                "label": f"{str(nom_sujet).strip()} ({str(annee).strip()})"
            })
        return sujets
    except Exception as e:
        st.error(f"Erreur : {e}"); return []

# --- BANDEAU DES CRÉDITS ---
st.caption("*Qui sommes nous ?*")
st.markdown("""
<div style="font-size: 0.9rem; color: #555; border-bottom: 1px solid #ddd; padding-bottom: 10px; margin-bottom: 25px;">
    <b>Sylvain Betoule</b> (Doctorant, Sorbonne Université) • 
    <b>Ulysse Garnier</b> (Doctorant, Sorbonne Université) • 
    <b>Morgane Leite</b> (Responsable de la préparation à l'agrégation de chimie, ENS)
</div>
""", unsafe_allow_html=True)

# --- LOGO ET SOUS-TITRE (LOGO TEXTUEL) ---
st.markdown("""
    <div class="logo-container">
        <h1 class="logo-main">🧪 Annales Lab Chimie</h1>
        <p class="logo-sub">Recherche d'annales de chimie</p>
    </div>
    """, unsafe_allow_html=True)

# --- INSTRUCTIONS DE DÉPART ---
with st.expander("👋 Comment utiliser cet outil ?", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**1. Filtres**")
        st.info("⬅️ Cliquez sur la flèche en haut à gauche pour choisir vos thèmes.")
    with c2:
        st.markdown("**2. Recherche**")
        st.info("Cliquez sur le bouton bleu **🚀 Lancer la recherche** en bas.")
    with c3:
        st.markdown("**3. Analyse**")
        st.info("Sélectionnez un sujet en bas de la page : les questions ciblées apparaîtront en couleur.")
    
    st.divider()
    st.markdown("⚠️ *La liste des thématiques correspond au contenu des **programmes de CPGE**. Des niveaux de difficulté sont indiqués par rapport à un élève de CPGE. Ces derniers sont purement indicatifs et propres à l'interprétation des concepteurs de ce site.*")

# --- BARRE LATÉRALE (FILTRES) ---
with st.sidebar:
    st.header("⚙️ Paramètres")
    criteres = []
    
    for n in range(st.session_state.nb_filtres):
        st.subheader(f"Filtre {n+1}")
        t = st.selectbox(f"Thème", THEMES_LISTE, key=f"t_{n}")
        
        niveaux_lower = [str(x).lower() for x in NIVEAUX_ORDRE]
        
        try:
            idx_start = niveaux_lower.index("facile")
            start_val = NIVEAUX_ORDRE[idx_start]
        except ValueError:
            start_val = NIVEAUX_ORDRE[0]
            
        try:
            idx_end = niveaux_lower.index("difficile")
            end_val = NIVEAUX_ORDRE[idx_end]
        except ValueError:
            end_val = NIVEAUX_ORDRE[-1]
        
        d_range = st.select_slider(
            f"Plage de difficulté",
            options=NIVEAUX_ORDRE,
            value=(start_val, end_val),
            key=f"d_{n}"
        )
        
        m = st.number_input(f"Quantité", min_value=1, value=1, key=f"m_{n}")
        criteres.append({"theme": t, "diff_range": d_range, "min": m})
    
    if st.button("➕ Ajouter un filtre"):
        st.session_state.nb_filtres += 1
        st.rerun()
    if st.button("🗑️ Supprimer le dernier filtre") and st.session_state.nb_filtres > 1:
        st.session_state.nb_filtres -= 1
        st.rerun()

# --- BOUTON DE RECHERCHE ---
if st.button("🚀 Lancer la recherche", type="primary", use_container_width=True):
    data = charger_donnees(URL_CSV)
    trouves = []
    for s in data:
        q = s['questions']
        valid = True
        stats = []
        for c in criteres:
            idx_min = NIVEAUX_ORDRE.index(c['diff_range'][0])
            idx_max = NIVEAUX_ORDRE.index(c['diff_range'][1])
            niveaux_acceptes = NIVEAUX_ORDRE[idx_min : idx_max + 1]
            
            mask_theme = q['Thème'].astype(str).str.contains(c['theme'], case=False, na=False)
            mask_diff = q['Difficulté'].astype(str).str.strip().isin(niveaux_acceptes)
            
            count = len(q[mask_theme & mask_diff])
            stats.append(f"{c['theme']} : {count}")
            
            if count < c['min']:
                valid = False
                break
        
        if valid:
            s['stats'] = " | ".join(stats)
            trouves.append(s)
    
    trouves.sort(key=lambda x: pd.to_numeric(x['annee'], errors='coerce'), reverse=True)
    st.session_state.resultats_recherche = trouves

# --- AFFICHAGE DES RÉSULTATS ---
if st.session_state.resultats_recherche is not None:
    res = st.session_state.resultats_recherche
    if res:
        st.success(f"✅ {len(res)} sujet(s) trouvé(s)")
        
        df_res = pd.DataFrame([{
            "Année": r['annee'], 
            "Sujet": r['nom'], 
            "Détails": r['stats']
        } for r in res])
        st.table(df_res)
        
        st.divider()
        options_affichage = [r.get('label', r.get('nom')) for r in res]
        choix_label = st.selectbox("🔍 Afficher les détails du sujet :", options_affichage)
        
        sujet_choisi = next(r for r in res if r['label'] == choix_label)
        df_details = sujet_choisi['questions']
        
        def highlight_rows(row):
            for c in criteres:
                idx_min = NIVEAUX_ORDRE.index(c['diff_range'][0])
                idx_max = NIVEAUX_ORDRE.index(c['diff_range'][1])
                niveaux_acceptes = NIVEAUX_ORDRE[idx_min : idx_max + 1]
                
                theme_match = c['theme'].lower() in str(row['Thème']).lower()
                diff_match = str(row['Difficulté']).strip() in niveaux_acceptes
                
                if theme_match and diff_match:
                    return ['background-color: #d1e7ff; color: black'] * len(row)
            return [''] * len(row)

        st.subheader(f"Détails : {choix_label}")
        st.markdown("*Les lignes surlignées en bleu correspondent à vos critères de recherche.*")
        
        styled_df = df_details.style.apply(highlight_rows, axis=1)
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Aucun résultat ne correspond à tous vos critères.")