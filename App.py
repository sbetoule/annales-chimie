import streamlit as st
import pandas as pd

# Titre de l'onglet et mise en page large
st.set_page_config(page_title="Annales Lab Chimie", layout="wide")

# --- STYLE CSS PERSONNALISÉ (Compact & Graphique) ---
# Import de polices Google : Poppins (Grassa/Géométrique), Permanent Marker (Dynamique/Tag), Roboto (Neutre)
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@800;900&family=Permanent+Marker&family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    
    <style>
        /* --- Style Compact pour le bandeau des crédits --- */
        .credits-compact {
            font-size: 0.9rem;
            color: #555;
            text-align: center;
            border-bottom: 1px solid #ddd;
            padding-bottom: 8px;
            margin-bottom: 20px;
            font-family: 'Roboto', sans-serif;
        }
        .credits-compact b {
            color: #333;
        }
        .credits-qsn {
            color: #7f8c8d;
            font-weight: 700;
            margin-right: 8px;
        }

        /* --- Style du Logo Dynamique & Déstructuré --- */
        .logo-graphic-container {
            text-align: center;
            margin-bottom: 35px;
            padding: 20px 30px;
            background: linear-gradient(165deg, rgba(255, 154, 68, 0.05) 0%, rgba(252, 96, 118, 0.08) 100%);
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
            z-index: 1; /* Derrière Lab */
        }

        /* "Lab" : Dynamique, Corail Solaire, PLUS PETIT et SUPERPOSÉ */
        .logo-lab-badged {
            font-family: 'Permanent Marker', cursive !important;
            font-size: 1.8rem !important; /* TAILLE RÉDUITE */
            color: #ffffff; 
            background: linear-gradient(135deg, #ff9a44 0%, #fc6076 100%); 
            padding: 3px 15px; /* Padding ajusté */
            border-radius: 50px;
            position: absolute;
            
            /* POSITION AJUSTÉE POUR LA SUPERPOSITION DISCRÈTE SUR ANNALES */
            top: 45px; /* Plus bas */
            right: 0px; /* Plus à gauche, fin de Annales */
            
            transform: rotate(-10deg); /* Rotation légère */
            z-index: 2; /* Devant Annales */
            box-shadow: 0 4px 10px rgba(252, 96, 118, 0.3);
            letter-spacing: 0;
        }

        /* "Chimie" : Bleu profond scientifique */
        .logo-chimie {
            font-size: 3.5rem !important;
            background: linear-gradient(135deg, #1f77b4 0%, #3498db 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-fill-color: transparent;
            margin-top: -10px; /* Rapproche */
            display: block; /* Va à la ligne */
        }

        .logo-sub-dynamic {
            font-family: 'Roboto', sans-serif !important;
            font-size: 0.95rem !important;
            color: #7f8c8d;
            text-transform: uppercase;
            letter-spacing: 6px;
            margin-top: 15px;
            font-weight: 400;
        }

        /* --- STYLES STREAMLIT (Harmonisation Corail) --- */
        .stButton > button {
            border-radius: 12px !important;
        }
        
        .stSlider [data-baseweb="slider"] div[role="presentation"] div {
            background-color: #fc6076 !important; /* Couleur active Corail */
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

# --- URLS DES FLUX DES FEUILLES DE CALCUL GOOGLE ---
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTsADsmsMnYgQXIUlU25_FlKrtTffM5XOL69taw9Pco8AHV4suIUtT0tg384XBtBAo28qGKGbtSJtIy/pub?gid=0&single=true&output=csv"
URL_THEMES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTsADsmsMnYgQXIUlU25_FlKrtTffM5XOL69taw9Pco8AHV4suIUtT0tg384XBtBAo28qGKGbtSJtIy/pub?gid=1733310474&single=true&output=csv"
URL_NIVEAUX = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTsADsmsMnYgQXIUlU25_FlKrtTffM5XOL69taw9Pco8AHV4suIUtT0tg384XBtBAo28qGKGbtSJtIy/pub?gid=1879771001&single=true&output=csv"

# --- FONCTION DE RÉCUPÉRATION DES LISTES (Thèmes et Difficultés) ---
@st.cache_data(ttl=60)
def recuperer_listes(url_themes, url_niveaux):
    try:
        df_t = pd.read_csv(url_themes, header=None)
        themes = df_t.iloc[0].dropna().astype(str).tolist()
        df_n = pd.read_csv(url_niveaux, header=None)
        # On garde l'ordre brut de l'onglet Excel pour le curseur
        niveaux = df_n.iloc[0].dropna().astype(str).tolist()
        return themes, niveaux
    except:
        return ["Erreur"], ["facile", "moyen", "difficile"]

# Chargement des listes
THEMES_LISTE, NIVEAUX_ORDRE = recuperer_listes(URL_THEMES, URL_NIVEAUX)

# --- GESTION DE L'ÉTAT DE LA SESSION ( Session State) ---
if 'resultats_recherche' not in st.session_state:
    st.session_state.resultats_recherche = None
if 'nb_filtres' not in st.session_state:
    st.session_state.nb_filtres = 1

# --- FONCTION DE CHARGEMENT DES DONNÉES DU CSV PRINCIPAL ---
@st.cache_data(ttl=30)
def charger_donnees(url):
    try:
        df = pd.read_csv(url, header=None, low_memory=False)
        sujets = []
        # Boucle sur les colonnes, 4 par 4 (Numéro, Thème, Difficulté, Remarque)
        for i in range(1, df.shape[1], 4):
            nom_sujet = df.iloc[1, i]
            # Vérifier si la colonne correspond à un vrai sujet
            if pd.isna(nom_sujet) or str(nom_sujet).strip() == "": continue
            annee = df.iloc[2, i]
            
            # Extraction du bloc de questions
            questions = df.iloc[4:, i : i+4].copy()
            questions.columns = ['Numéro', 'Thème', 'Difficulté', 'Remarque']
            
            # Nettoyage des données
            questions = questions.dropna(subset=['Thème'])
            questions = questions[questions['Thème'].astype(str).str.lower() != "thème"]
            
            # Stockage structuré du sujet
            sujets.append({
                "nom": str(nom_sujet).strip(),
                "annee": str(annee).strip() if pd.notna(annee) else "0",
                "questions": questions,
                "label": f"{str(nom_sujet).strip()} ({str(annee).strip()})"
            })
        return sujets
    except Exception as e:
        st.error(f"Erreur de chargement des données : {e}"); return []

# --- BANDEAU DES CRÉDITS COMPACT (Sur une seule ligne) ---
st.markdown("""
<div class="credits-compact">
    <span class="credits-qsn">Qui sommes nous ?</span>
    <b>Sylvain Betoule</b> (Sorbonne Univ.) • 
    <b>Ulysse Garnier</b> (Sorbonne Univ.) • 
    <b>Morgane Leite</b> (Ens)
</div>
""", unsafe_allow_html=True)

# --- LOGO GRAPHIQUE DYNAMIQUE ET DÉSTRUCTURÉ (Corail Solaire) ---
st.markdown("""
    <div class="logo-graphic-container">
        <span class="logo-text-base logo-annales">Annales</span>
        <span class="logo-lab-badged">Lab</span>
        <span class="logo-text-base logo-chimie">Chimie</span>
        <p class="logo-sub-dynamic">Recherche d'annales de chimie</p>
    </div>
    """, unsafe_allow_html=True)

# --- INSTRUCTIONS DE DÉPART (Expander) ---
with st.expander("👋 Comment utiliser cet outil ?", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**1. Filtres**")
        st.info("⬅️ Utilisez la barre latérale pour choisir vos thèmes.")
    with c2:
        st.markdown("**2. Recherche**")
        st.info("Cliquez sur le bouton bleu **🚀 Lancer la recherche**.")
    with c3:
        st.markdown("**3. Analyse**")
        st.info("Les questions ciblées apparaîtront en bleu dans les détails.")
    
    st.divider()
    st.markdown("⚠️ *La liste des thématiques correspond au contenu des **programmes de CPGE**. Des niveaux de difficulté sont indiqués par rapport à un élève de CPGE. Ces derniers sont purement indicatifs et propres à l'interprétation des concepteurs de ce site.*")

# --- BARRE LATÉRALE (Filtres de recherche) ---
with st.sidebar:
    st.header("⚙️ Paramètres de recherche")
    criteres = []
    
    # Génération dynamique des blocs de filtres
    for n in range(st.session_state.nb_filtres):
        st.subheader(f"Filtre {n+1}")
        # Sélection du Thème
        t = st.selectbox(f"Thème", THEMES_LISTE, key=f"t_{n}")
        
        # Initialisation intelligente de la plage de difficulté (insensible à la casse)
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
        
        # Curseur de plage de difficulté
        d_range = st.select_slider(
            f"Plage de difficulté",
            options=NIVEAUX_ORDRE,
            value=(start_val, end_val),
            key=f"d_{n}"
        )
        
        # Quantité minimale de questions
        m = st.number_input(f"Quantité minimale", min_value=1, value=1, key=f"m_{n}")
        
        # Stockage des critères du filtre
        criteres.append({"theme": t, "diff_range": d_range, "min": m})
    
    # Boutons d'ajout/suppression de filtres
    st.divider()
    col_add, col_del = st.columns(2)
    with col_add:
        if st.button("➕ Ajouter un filtre", use_container_width=True):
            st.session_state.nb_filtres += 1
            st.rerun()
    with col_del:
        if st.button("🗑️ Supprimer le dernier", use_container_width=True) and st.session_state.nb_filtres > 1:
            st.session_state.nb_filtres -= 1
            st.rerun()

# --- ESPACE DE RECHERCHE PRINCIPAL ---
if st.button("🚀 Lancer la recherche d'annales", type="primary", use_container_width=True):
    data = charger_donnees(URL_CSV)
    trouves = []
    
    # Parcours de tous les sujets chargés
    for s in data:
        q = s['questions']
        valid = True
        stats = []
        
        # Vérification de chaque filtre sur le sujet en cours
        for c in criteres:
            # Calcul de la plage de difficultés acceptées
            idx_min = NIVEAUX_ORDRE.index(c['diff_range'][0])
            idx_max = NIVEAUX_ORDRE.index(c['diff_range'][1])
            niveaux_acceptes = NIVEAUX_ORDRE[idx_min : idx_max + 1]
            
            # Application des masques de filtrage
            mask_theme = q['Thème'].astype(str).str.contains(c['theme'], case=False, na=False)
            mask_diff = q['Difficulté'].astype(str).str.strip().isin(niveaux_acceptes)
            
            # Comptage des questions valides
            count = len(q[mask_theme & mask_diff])
            
            # Construction des statistiques d'affichage
            stats.append(f"{c['theme']} : {count}")
            
            # Le sujet est invalide s'il n'atteint pas le minimum pour UN seul filtre
            if count < c['min']:
                valid = False
                break
        
        # Si le sujet respecte tous les filtres, on l'ajoute aux résultats
        if valid:
            s['stats'] = " | ".join(stats)
            trouves.append(s)
    
    # --- TRI PAR ANNÉE (DÉCROISSANT) ---
    trouves.sort(key=lambda x: pd.to_numeric(x['annee'], errors='coerce'), reverse=True)
    
    # Sauvegarde des résultats dans la session
    st.session_state.resultats_recherche = trouves

# --- AFFICHAGE DES RÉSULTATS ---
if st.session_state.resultats_recherche is not None:
    res = st.session_state.resultats_recherche
    
    if res:
        st.divider()
        st.success(f"✅ {len(res)} sujet(s) trouvé(s) correspondant à vos critères")
        
        # Tableau de résumé des résultats
        df_res = pd.DataFrame([{
            "Année": r['annee'], 
            "Sujet": r['nom'], 
            "Détails des questions trouvées": r['stats']
        } for r in res])
        st.table(df_res)
        
        st.divider()
        
        # --- SÉLECTION ET AFFICHAGE DES DÉTAILS D'UN SUJET ---
        options_affichage = [r.get('label', r.get('nom')) for r in res]
        choix_label = st.selectbox("🔍 Sélectionner un sujet pour voir le détail des questions :", options_affichage)
        
        # Récupération du sujet choisi
        sujet_choisi = next(r for r in res if r['label'] == choix_label)
        df_details = sujet_choisi['questions']
        
        # --- FONCTION DE MISE EN COULEUR DES LIGNES (Highlighting) ---
        def highlight_rows(row):
            for c in criteres:
                # Recalcul des niveaux acceptés pour ce filtre précis
                idx_min = NIVEAUX_ORDRE.index(c['diff_range'][0])
                idx_max = NIVEAUX_ORDRE.index(c['diff_range'][1])
                niveaux_acceptes = NIVEAUX_ORDRE[idx_min : idx_max + 1]
                
                # Vérification de la correspondance thème ET difficulté
                theme_match = c['theme'].lower() in str(row['Thème']).lower()
                diff_match = str(row['Difficulté']).strip() in niveaux_acceptes
                
                # Si match, on applique la couleur de fond
                if theme_match and diff_match:
                    return ['background-color: #d1e7ff; color: black'] * len(row) # Bleu clair
            return [''] * len(row) # Pas de style

        # Affichage du tableau de détails stylisé
        st.subheader(f"Détails : {choix_label}")
        st.markdown("*Les lignes surlignées en bleu correspondent à vos critères de recherche.*")
        
        # Application du style
        styled_df = df_details.style.apply(highlight_rows, axis=1)
        
        # Affichage du DataFrame Streamlit
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
    else:
        st.divider()
        st.warning("⚠️ Aucun résultat ne correspond à l'intégralité de vos critères de recherche.")