import streamlit as st
import pandas as pd

st.set_page_config(page_title="Annales Lab Chimie", layout="wide")

# --- STYLE CSS (LOGO DYNAMIQUE CORAIL + Curseur + Tableaux) ---
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@800;900&family=Permanent+Marker&family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    
    <style>
        /* Container principal du Logo avec fond graphique arrondi */
        .logo-graphic-container {
            text-align: center;
            margin-top: 20px;
            margin-bottom: 40px;
            padding: 25px 30px;
            background: linear-gradient(165deg, rgba(255, 154, 68, 0.05) 0%, rgba(252, 96, 118, 0.1) 100%);
            border-radius: 60px 20px 80px 30px;
            display: inline-block;
            position: relative;
            left: 50%;
            transform: translateX(-50%);
            box-shadow: 0 10px 30px rgba(0,0,0,0.03);
        }

        .logo-text-base {
            font-family: 'Poppins', sans-serif !important;
            font-weight: 900 !important;
            text-transform: uppercase;
            letter-spacing: -2px;
            line-height: 0.9;
            margin: 0;
            display: inline-block;
        }

        /* "Annales" : Dégradé sombre élégant */
        .logo-annales {
            font-size: 4rem !important;
            color: #2c3e50;
            position: relative;
            z-index: 1;
        }

        /* "Lab" : Dynamique, Corail Solaire & Blanc Glacé */
        .logo-lab-badged {
            font-family: 'Permanent Marker', cursive !important;
            font-size: 2.8rem !important;
            color: #ffffff; 
            background: linear-gradient(135deg, #ff9a44 0%, #fc6076 100%); 
            padding: 5px 25px;
            border-radius: 50px;
            position: absolute;
            top: 20px;
            right: -30px;
            transform: rotate(-12deg);
            z-index: 2;
            box-shadow: 0 4px 15px rgba(252, 96, 118, 0.4);
        }

        /* "Chimie" : Bleu profond pour le rappel scientifique */
        .logo-chimie {
            font-size: 3.5rem !important;
            background: linear-gradient(135deg, #1f77b4 0%, #3498db 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-fill-color: transparent;
            margin-top: -10px;
            display: block;
        }

        .logo-sub-dynamic {
            font-family: 'Roboto', sans-serif !important;
            font-size: 1rem !important;
            color: #7f8c8d;
            text-transform: uppercase;
            letter-spacing: 6px;
            margin-top: 15px;
            font-weight: 400;
        }

        /* --- STYLES STREAMLIT (Curseur & Boutons harmonisés) --- */
        .stButton > button {
            border-radius: 12px !important;
        }
        
        .stSlider [data-baseweb="slider"] div[role="presentation"] div {
            background-color: #fc6076 !important; 
        }
        .stSlider [data-baseweb="slider"] div[role="slider"] {
            background-color: #fc6076 !important;
            border: 2px solid white !important;
        }
        div[data-testid="stThumbValue"] {
            color: #fc6076 !important;
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

# --- LOGO GRAPHIQUE DYNAMIQUE ---
st.markdown("""
    <div class="logo-graphic-container">
        <span class="logo-text-base logo-annales">Annales</span>
        <span class="logo-lab-badged">Lab</span>
        <span class="logo-text-base logo-chimie">Chimie</span>
        <p class="logo-sub-dynamic">Recherche d'annales de chimie</p>
    </div>
    """, unsafe_allow_html=True)

# --- INSTRUCTIONS DE DÉPART ---
with st.expander("👋 Comment utiliser cet outil ?", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**1. Filtres**")
        st.info("⬅️ Utilisez la barre latérale pour choisir vos thèmes.")
    with c2:
        st.markdown("**2. Recherche**")
        st.info("Cliquez sur le bouton **🚀 Lancer la recherche**.")
    with c3:
        st.markdown("**3. Analyse**")
        st.info("Les questions ciblées apparaîtront en bleu dans les détails.")
    
    st.divider()
    st.markdown("⚠️ *La liste des thématiques correspond au contenu des **programmes de CPGE**.*")

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
        styled_df = df_details.style.apply(highlight_rows, axis=1)
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Aucun résultat ne correspond à tous vos critères.")