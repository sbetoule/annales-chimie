import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
import numpy as np
import textwrap

# Configuration de la page
st.set_page_config(
    page_title="Annales Lab Chimie",
    page_icon="🧪",
    layout="wide",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': """
            # Annales Lab Chimie
            Outil de recherche d'annales de chimie (CPGE, Agrégation, CAPES, IChO).
            Développé par Sylvain Betoule, Ulysse Garnier et Morgane Leite.
        """
    })

# --- STYLE CSS (LOGO, CRÉDITS, ANIMATION MOBILE) ---
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@800;900&family=Permanent+Marker&family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    
    <style>
  
        /* Réduire spécifiquement l'espace autour des dividers dans la sidebar */
        [data-testid="stSidebarUserContent"] hr {
            margin-top: 5px !important;
            margin-bottom: 15px !important;
        }
        
        /* Ajuster l'espacement du slider */
        [data-testid="stSidebarUserContent"] .stSlider {
            padding-bottom: 0px !important;
        } 
      /* Style de base du texte dans l'expander */
        .stExpander summary p {
            font-size: 0.95rem !important;
            color: #2c3e50; /* Couleur sombre pour le titre */
        }

        /* On retire la règle ::first-line qui causait le bug */
        /* Optionnel : Enlever la bordure rouge de l'expander quand on clique dessus */
        .stExpander:focus {
            outline: none !important;
            box-shadow: none !important;
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

@st.cache_data(ttl=60)

def recuperer_structure_complete(url_themes):
    try:
        df_t = pd.read_csv(url_themes, header=None)
        noms = df_t.iloc[0].dropna().astype(str).tolist()
        cats = df_t.iloc[1].dropna().astype(str).tolist()
        sous_themes = df_t.iloc[2].dropna().astype(str).tolist() 
        
        mapping_cat = dict(zip(noms, cats))
        mapping_sous = dict(zip(noms, sous_themes))
        return mapping_cat, mapping_sous
    except:
        return {}, {}
        
with st.spinner("Initialisation des thématiques..."):
    THEMES_LISTE, NIVEAUX_ORDRE = recuperer_listes(URL_THEMES, URL_NIVEAUX)
    DICT_CATEGORIES, DICT_SOUS_THEMES = recuperer_structure_complete(URL_THEMES)

if 'resultats_recherche' not in st.session_state: st.session_state.resultats_recherche = None
if 'nb_filtres' not in st.session_state: st.session_state.nb_filtres = 0
default_theme_index = 3

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

def obtenir_couleur_gradient(base_hex, intensite):
    """
    Simule un gradient en modifiant l'opacité ou la saturation.
    intensite: float entre 0.1 (clair) et 1.0 (foncé)
    """
    # Pour simplifier avec Plotly, on peut utiliser des échelles de couleurs intégrées
    # ou passer par des RGBA. Ici, on va utiliser des échelles prédéfinies plus bas.
    return intensite

def formater_nom_theme(nom, largeur=15):
    """Insère des retours à la ligne sans couper les mots techniques."""
    if not nom or nom == "CHIMIE": return nom
    lignes = textwrap.wrap(nom, width=largeur, break_long_words=False)
    return "<br>".join(lignes)

def afficher_mind_map_thematique(resultats):
    if not resultats:
        return

    import time
    counts = {}
    adjacence = {}

    # --- 1. CALCUL DES COMPTAGES ET DES LIENS ---
    for s in resultats:
        df_q = s['questions']
        # On traite par bloc (Partie) si l'info existe, sinon sur tout le sujet
        groupes = df_q.groupby('Partie') if 'Partie' in df_q.columns else [("Unique", df_q)]
        
        for _, data_partie in groupes:
            themes = [t.strip() for t in data_partie['Thème'].dropna().astype(str).tolist() 
                      if t.strip() != ""]
            
            for i in range(len(themes)):
                t = themes[i]
                counts[t] = counts.get(t, 0) + 1
                # Création d'un lien si deux thèmes se suivent
                if i < len(themes) - 1:
                    t_next = themes[i+1]
                    if t != t_next:
                        pair = tuple(sorted((t, t_next)))
                        adjacence[pair] = adjacence.get(pair, 0) + 1

    # --- 2. CONSTRUCTION DU GRAPHE HIÉRARCHIQUE ---
    G = nx.Graph()
    
    # Niveaux structurels (N0 et N1)
    G.add_node("CHIMIE", cat="ROOT", label="<b>CHIMIE</b>", lvl=0)
    G.add_node("CHIMIE ORGANIQUE", cat="ORGA_HUB", label="<b>CHIMIE<br>ORGANIQUE</b>", lvl=1)
    G.add_node("CHIMIE GÉNÉRALE", cat="GEN_HUB", label="<b>CHIMIE<br>GÉNÉRALE</b>", lvl=1)
    
    G.add_edge("CHIMIE", "CHIMIE ORGANIQUE")
    G.add_edge("CHIMIE", "CHIMIE GÉNÉRALE")

    for t, count in counts.items():
        t_clean = t.strip()
        cat = DICT_CATEGORIES.get(t_clean, "AUTRE").upper()
        sous_t = DICT_SOUS_THEMES.get(t_clean, "Autre").strip()
        hub_parent = "CHIMIE ORGANIQUE" if "ORGA" in cat else "CHIMIE GÉNÉRALE"

        # RÈGLE A : Le Thème est "Autre" -> Branchement direct sur le Root (Chimie)
        if "autre" in t_clean.lower():
            node_id = f"AUTRE_ROOT_{t_clean}_{cat}" # ID unique technique
            G.add_node(node_id, cat=cat, count=count, label="Autre", lvl=3)
            G.add_edge("CHIMIE", node_id)
            continue

        # RÈGLE B : Le Sous-Thème est "Autre" -> Branchement sur le Hub (Orga ou Générale)
        if "autre" in sous_t.lower():
            G.add_node(t_clean, cat=cat, count=count, label=formater_nom_theme(t_clean), lvl=3)
            G.add_edge(hub_parent, t_clean)
        
        # CAS GÉNÉRAL : Hub -> Sous-Thème -> Thème
        else:
            if not G.has_node(sous_t):
                G.add_node(sous_t, cat=cat, label=f"<i>{sous_t}</i>", lvl=2)
                G.add_edge(hub_parent, sous_t)
            
            G.add_node(t_clean, cat=cat, count=count, label=formater_nom_theme(t_clean), lvl=3)
            G.add_edge(sous_t, t_clean)

    # Ajout des liens d'affinité (inter-thèmes)
    for (u, v), w in adjacence.items():
        if u in G and v in G:
            G.add_edge(u, v, weight=w * 0.3)

    # --- 3. POSITIONNEMENT STABLE ---
    # k augmenté pour aérer la structure à 4 niveaux
    pos = nx.spring_layout(G, k=2.0/np.sqrt(len(G.nodes())), iterations=200, seed=42)

    # --- 4. ANIMATION FLUIDE (SANS CLIGNOTEMENT) ---
    placeholder = st.empty()
    
    # Ordre d'apparition : Hubs -> Sous-thèmes -> Thèmes (triés par fréquence)
    hubs = [n for n, d in G.nodes(data=True) if d.get('lvl', 3) <= 1]
    sous_themes = [n for n, d in G.nodes(data=True) if d.get('lvl') == 2]
    feuilles = sorted([n for n, d in G.nodes(data=True) if d.get('lvl') == 3], 
                     key=lambda x: G.nodes[x].get('count', 0), reverse=True)
    
    # On groupe les feuilles par 2 pour la fluidité
    chunks_feuilles = [feuilles[i:i + 2] for i in range(0, len(feuilles), 2)]
    sequence = [hubs] + [sous_themes] + chunks_feuilles
    
    noeuds_visibles = []
    max_q = max(counts.values()) if counts else 1

    for step_nodes in sequence:
        noeuds_visibles.extend(step_nodes)
        
        fig = go.Figure()

        # Dessin des arrêtes
        edge_x, edge_y = [], []
        for u, v in G.edges():
            if u in noeuds_visibles and v in noeuds_visibles:
                edge_x.extend([pos[u][0], pos[v][0], None])
                edge_y.extend([pos[u][1], pos[v][1], None])

        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y, 
            line=dict(width=0.5, color='rgba(200, 200, 200, 0.3)'), 
            mode='lines', hoverinfo='none'
        ))

        # Dessin des noeuds
        nx_v, ny_v, nt_v, nc_v, ns_v, nh_v = [], [], [], [], [], []
        for n_id in noeuds_visibles:
            nx_v.append(pos[n_id][0])
            ny_v.append(pos[n_id][1])
            nt_v.append(G.nodes[n_id].get('label', ''))
            
            lvl = G.nodes[n_id].get('lvl', 3)
            cat = G.nodes[n_id].get('cat', 'AUTRE')
            q = G.nodes[n_id].get('count', 0)
            
            # Style selon le niveau
            if lvl == 0: # CHIMIE
                ns_v.append(50); nc_v.append("#fc6076"); nh_v.append("<b>RACINE</b>")
            elif lvl == 1: # HUBS
                ns_v.append(38); nc_v.append("#7a7aff" if "ORGA" in cat else "#ffb366"); nh_v.append(f"<b>{n_id}</b>")
            elif lvl == 2: # SOUS-THÈMES
                ns_v.append(28); nc_v.append("#dfe6e9"); nh_v.append(f"Sous-thème : {n_id}")
            else: # THÈMES (Feuilles)
                ratio = q / max_q
                ns_v.append(22)
                if "ORGA" in cat:
                    nc_v.append("#0000bb" if ratio > 0.6 else "#7a7aff" if ratio > 0.2 else "#d1d1ff")
                else:
                    nc_v.append("#e67e00" if ratio > 0.6 else "#ffb366" if ratio > 0.2 else "#ffe8cc")
                nh_v.append(f"<b>{n_id}</b><br>{q} questions")

        fig.add_trace(go.Scatter(
            x=nx_v, y=ny_v, mode='markers+text', text=nt_v, 
            textposition="top center",
            textfont=dict(size=10, family="Arial", color="black"),
            marker=dict(color=nc_v, size=ns_v, line=dict(width=1, color='white')),
            hoverinfo='text', hovertext=nh_v
        ))

        # Fixer les axes est la clé pour stopper le clignotement (zoom constant)
        fig.update_layout(
            showlegend=False, height=750, margin=dict(t=0, b=0, l=0, r=0),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.4, 1.4], fixedrange=True),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.4, 1.4], fixedrange=True),
            template="plotly_white",
            dragmode=False
        )

        placeholder.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, key=f"step_{len(noeuds_visibles)}")
        time.sleep(0.04)

    # Rendu final interactif
    fig.update_layout(dragmode='pan')
    placeholder.plotly_chart(fig, use_container_width=True, config={'scrollZoom': True, 'displayModeBar': False}, key="final_map")
# --- CHARGEMENT INITIAL POUR LES BORNES DE DATE ---
data_full = charger_donnees(URL_CSV)
if data_full:
    # Extraction de toutes les années sous forme d'entiers pour le tri
    toutes_annees = sorted(list(set([int(s['annee']) for s in data_full])), reverse=True)
    annee_max_data = max(toutes_annees)
    annee_min_data = min(toutes_annees)
    liste_annees_desc = list(range(annee_max_data, annee_min_data - 1, -1))
# --- AFFICHAGE ---
st.markdown("""
<div class="credits-compact">
    <span class="credits-qsn">Développé par </span>
    <b>Sylvain Betoule</b> (Doctorant, Sorbonne Univ.) • 
    <b>Ulysse Garnier</b> (Doctorant, Sorbonne Univ.) • 
    <b>Morgane Leite</b> (Resp. prépa agrégation de chimie, ENS) • 
    <a href="mailto:sylvain.betoule@gmail.com?subject=Annales%20Lab%20Chimie" 
       style="color: #2c3e50; text-decoration: none; font-weight: bold; font-size: 0.85rem; margin-left: 5px;">
       📩 Contact
    </a>
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
        st.markdown("**1. Filtres**"); st.info("""⬅️ Utilisez la barre latérale pour sélectionner vos thèmes.""")
    with c2:
        st.markdown("**2. Recherche**"); st.info("Cliquez sur le bouton 🔎 **Lancer la recherche**.")
    with c3:
        st.markdown("**3. Analyse**"); st.info("⬇️ Les questions ciblées apparaîtront en bleu dans les détails et les changements de partie en pointillés.")
    st.markdown("<p class='cpge-warning'>⚠️ La liste des thématiques correspond au contenu des programmes de CPGE. Des niveaux de difficulté sont indiqués par rapport à un élève de CPGE. Ces derniers sont purement indicatifs et propres à l'interprétation des concepteurs de ce site.</p>", unsafe_allow_html=True)

# --- BARRE LATÉRALE ---
def classifier_concours(nom_sujet):
    nom = str(nom_sujet).upper()
    if "ICHO" in nom:
        return "IChO"
    if "CAPES" in nom or "AGREG" in nom:
        return "Agreg / CAPES"
    return "CPGE"
with st.sidebar:
    st.header("⚙️ Filtres")
    categories_choisies = st.multiselect(
        "Type de concours :",
        options=["CPGE", "Agreg / CAPES", "IChO"],
        default=["CPGE", "Agreg / CAPES", "IChO"]
    )
    borne_gauche = annee_max_data
    borne_droite = annee_min_data

    periode_choisie = st.select_slider(
        "Période",
        options=liste_annees_desc, 
        value=(borne_gauche, borne_droite),
        )
    st.divider()
    regrouper_par_partie = False 
    if st.session_state.nb_filtres > 0:
        regrouper_par_partie = st.checkbox(
            "🎯 Je souhaite que les questions vérifiant ces critères apparaissent dans la même partie du sujet", 
            value=False)
    
    criteres = []
    niveaux_lower = [n.lower().strip() for n in NIVEAUX_ORDRE]
    try: s_idx, e_idx = niveaux_lower.index("facile"), niveaux_lower.index("difficile")
    except: s_idx, e_idx = 0, len(NIVEAUX_ORDRE) - 1

    # Affichage des filtres thématiques uniquement si nb_filtres > 0
    for n in range(st.session_state.nb_filtres):
        if n > 0: st.divider()
        # On utilise l'index 3 (4ème thème) pour le premier filtre, 0 pour les autres
        current_default = default_theme_index if n == 0 else 0
        
        t = st.selectbox(f"Thème", THEMES_LISTE, index=current_default, key=f"t_{n}")
        d_range = st.select_slider(f"Difficulté", options=NIVEAUX_ORDRE, value=(NIVEAUX_ORDRE[s_idx], NIVEAUX_ORDRE[e_idx]), key=f"d_{n}")
        m = st.number_input(f"Quantité min.", min_value=1, value=1, key=f"m_{n}")
        criteres.append({"theme": t, "diff_range": d_range, "min": m})

    if st.session_state.nb_filtres == 0:
        st.info("💡 Aucun filtre thématique actif.")

    label_plus = "➕ Filtre thématique" if st.session_state.nb_filtres == 0 else "➕ Filtre supplémentaire"
    if st.button(label_plus, use_container_width=True): 
        st.session_state.nb_filtres += 1
        st.rerun()
    if st.session_state.nb_filtres > 0:
        if st.button("🗑️ Retirer le dernier filtre", use_container_width=True): 
            st.session_state.nb_filtres -= 1
            st.rerun()
   
if st.button("🔎 Lancer la recherche d'annales", type="primary", use_container_width=True):
    if 'sujet_selectionne' in st.session_state:
        del st.session_state.sujet_selectionne
    with st.spinner("Analyse de la base de données en cours..."):
        data = charger_donnees(URL_CSV)
        trouves = []
        for s in data:
            categorie_sujet = classifier_concours(s['nom'])
            if categorie_sujet not in categories_choisies:
                continue 
            annee_sujet = int(s['annee'])
            annee_debut = min(periode_choisie)
            annee_fin = max(periode_choisie)
            if not (annee_debut <= annee_sujet <= annee_fin):
                continue
            q = s['questions'].copy()
            valid = True
            stats = []
            
            # --- NOUVELLE LOGIQUE DE VALIDATION ---
            if regrouper_par_partie and criteres:
                # 1. Découpage du sujet en listes de DataFrames (une par partie)
                parties = []
                debut_idx = 0
                for i, (idx_row, row) in enumerate(q.iterrows()):
                    if str(row['Numéro']).lower().strip().endswith("end"):
                        parties.append(q.iloc[debut_idx : i+1])
                        debut_idx = i + 1
                if debut_idx < len(q): # Ajoute la dernière partie si pas de "end"
                    parties.append(q.iloc[debut_idx:])

                # 2. Vérification : Il doit exister au moins UNE partie qui satisfait TOUS les critères
                sujet_valide_par_bloc = False
                
                for p in parties:
                    tous_criteres_dans_cette_partie = True
                    
                    for c in criteres:
                        theme_recherche = str(c['theme']).strip().lower()
                        try:
                            idx_start = NIVEAUX_ORDRE.index(c['diff_range'][0])
                            idx_end = NIVEAUX_ORDRE.index(c['diff_range'][1])
                            n_acc = [n.lower().strip() for n in NIVEAUX_ORDRE[idx_start : idx_end + 1]]
                        except: 
                            n_acc = [n.lower().strip() for n in NIVEAUX_ORDRE]

                        # On vérifie si CETTE partie 'p' contient le quota pour CE critère 'c'
                        mask_p = p['Thème'].astype(str).str.lower().str.contains(theme_recherche, regex=False, na=False) & \
                                 p['Difficulté'].astype(str).str.lower().str.strip().isin(n_acc)
                        
                        if len(p[mask_p]) < c['min']:
                            tous_criteres_dans_cette_partie = False
                            break # On sort de la boucle des critères, cette partie ne convient pas
                    
                    if tous_criteres_dans_cette_partie:
                        sujet_valide_par_bloc = True
                        break # On a trouvé une partie qui match tout, on peut valider le sujet
                
                valid = sujet_valide_par_bloc

            else:
                # LOGIQUE ACTUELLE (Globale sur tout le sujet)
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
                    if len(q[mask_theme & mask_diff]) < c['min']:
                        valid = False
                        break

            if valid:
                # --- NOUVELLE LOGIQUE DE FUSION DES STATS ---
                stats_map = {} # Dictionnaire pour cumuler les comptes par thème
                
                for c in criteres:
                    try:
                        idx_s = NIVEAUX_ORDRE.index(c['diff_range'][0])
                        idx_e = NIVEAUX_ORDRE.index(c['diff_range'][1])
                        n_criteres_acc = [n.lower().strip() for n in NIVEAUX_ORDRE[idx_s : idx_e + 1]]
                    except:
                        n_criteres_acc = [n.lower().strip() for n in NIVEAUX_ORDRE]
                    
                    # On calcule le masque pour ce critère précis
                    mask_stat = q['Thème'].astype(str).str.lower().str.contains(str(c['theme']).lower(), regex=False, na=False) & \
                                q['Difficulté'].astype(str).str.lower().str.strip().isin(n_criteres_acc)
                    
                    # On récupère les indices des questions qui matchent
                    indices_match = q[mask_stat].index.tolist()
                    
                    # On ajoute ces indices au set du thème (le set gère l'union A U B automatiquement)
                    theme_nom = str(c['theme'])
                    if theme_nom not in stats_map:
                        stats_map[theme_nom] = set()
                    stats_map[theme_nom].update(indices_match)
                
                # On transforme le dictionnaire en liste de chaînes "Thème (Total)"
                stats_list = [f"{t} ({len(indices)})" for t, indices in stats_map.items()]
                s['stats'] = " | ".join(stats_list) if stats_list else ""
                trouves.append(s)
                
        # --- NOUVEAU SYSTÈME DE TRI ---
        trouves.sort(key=lambda x: x['nom'].lower()) # Tri alphabétique A-Z
        st.session_state.resultats_recherche = sorted(trouves, key=lambda x: x['annee'], reverse=True) # Tri année 2024-2000
        
# --- RÉSULTATS ET DÉTAILS ---
if st.session_state.resultats_recherche:
    with st.expander("💡 Architecture des sujets trouvés", expanded=False):
        st.info("""
**Densité :** Les thèmes les plus fréquents s'affichent avec les couleurs les plus sombres.  
**Affinité :** Plus les notions se succèdent régulièrement dans les sujets, plus ils apparaissent proches sur le graphe.
""")
        afficher_mind_map_thematique(st.session_state.resultats_recherche)
    nb = len(st.session_state.resultats_recherche)
    label_sujet = "sujet trouvé" if nb == 1 else "sujets trouvés"
    st.success(f"✅ {nb} {label_sujet}")

    for idx, r in enumerate(st.session_state.resultats_recherche):
        # On utilise une flèche ou un séparateur pour bien distinguer les deux parties
        # Le gras de l'expander s'appliquera, mais la séparation sera nette
        stats_info = f"  |  {r['stats']}" if r['stats'] else ""
        titre_header = f"📄 {r['nom']} ({r['annee']}){stats_info}"
        
        with st.expander(titre_header):
            # --- LOGIQUE DU LIEN ---
            nom_comparaison = r['nom'].lower()
            lien_sujet = None
            if "icho - présélection" in nom_comparaison:
                lien_sujet = "https://www.sciencesalecole.org/olympiades-internationales-de-chimie-ressources/"
            elif "agreg externe spéciale chimie" in nom_comparaison:
                lien_sujet = "https://agregation-chimie.fr/index.php/composition-de-physique-chimie/annales-des-epreuves-ecrites"
            elif "agreg externe spéciale physique" in nom_comparaison:
                lien_sujet = "https://docteurs.agregation-physique.org/sc2019-3/"
            elif "agreg externe physique" in nom_comparaison:
                lien_sujet = "https://nc.agregation-physique.org/index.php/s/XzZWHcEfQjWwD8f"
            elif "agreg externe chimie" in nom_comparaison:
                lien_sujet = "https://agregation-chimie.fr/index.php/les-epreuves-ecrites/annales-des-epreuves-ecrites"
            elif "capes" in nom_comparaison:
                lien_sujet = "http://b.louchart.free.fr/Concours_et_examens/CAPES/CAPES_externe_Physique_Chimie/Sujets_et_corriges_ecrits.html"
            elif "agreg interne" in nom_comparaison:
                lien_sujet = "http://www.agregation-interne-physique-chimie.org/annales-des-eacutepreuves-eacutecrites.html"
            elif "ccp" in nom_comparaison:
                lien_sujet = "https://www.concours-commun-inp.fr/fr/epreuves/annales/annales-pc.html"
            elif "centrale" in nom_comparaison:
                lien_sujet = "https://www.concours-centrale-supelec.fr/sujets-rapports"
            elif "mines" in nom_comparaison:
                lien_sujet = "https://concoursminesponts.fr/annales/"
            elif "e3a" in nom_comparaison:
                lien_sujet = "https://www.e3a-polytech.fr/annales-et-rapport/"
            elif "agro véto" in nom_comparaison:
                lien_sujet = "https://www.concours-agro-veto.fr/archives-sujets-rapports/sujets-rapports-concours-cpge-bcpst/epreuves-ecrites-concours-cpge-bcpst#Chimie"
            elif "ENS - Chimie - BCPST" in nom_comparaison:
                lien_sujet = "https://banques-ecoles.fr/cms/filiere-bcpst/les-annales-et-rapports-des-jurys/#chimie"
            elif "ENS" in nom_comparaison:
                lien_sujet = "https://banques-ecoles.fr/cms/filiere-pc/annales-de-la-banque-pc/"

            if lien_sujet:
                st.link_button("🔗 Lien vers le sujet", lien_sujet, type="secondary")
     
            # 1. PRÉPARATION DES DONNÉES AVEC LIGNES DE SÉPARATION
            questions_originales = r['questions'].copy()
            lignes_avec_separateurs = []
            
            for _, row in questions_originales.iterrows():
                val_num = str(row['Numéro']).lower().strip()
                is_end = val_num.endswith("end")
                
                # On nettoie le numéro pour l'affichage
                row_copie = row.copy()
                row_copie['Numéro'] = str(row['Numéro']).replace("end", "").replace("END", "").strip()
                lignes_avec_separateurs.append(row_copie)
                
                # Si c'est une fin de partie, on injecte la ligne "Changement de Partie"
                motif = "─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─"
                if is_end:
                    separateur = pd.Series({
                        'Numéro': motif, 
                        'Thème': motif,
                        'Difficulté': motif,
                        'Remarque': motif
                    })
                    lignes_avec_separateurs.append(separateur)

            df_final = pd.DataFrame(lignes_avec_separateurs)

                      # 2. FONCTION DE STYLE MISE À JOUR
            def style_separateurs(row):                
                # Sinon, logique de surbrillance classique
                is_highlighted = False
                for c in criteres:
                    try:
                        i_min, i_max = NIVEAUX_ORDRE.index(c['diff_range'][0]), NIVEAUX_ORDRE.index(c['diff_range'][1])
                        n_acc = [n.lower().strip() for n in NIVEAUX_ORDRE[i_min : i_max + 1]]
                    except: n_acc = [n.lower().strip() for n in NIVEAUX_ORDRE]
                    
                    if c['theme'].lower() in str(row['Thème']).lower() and str(row['Difficulté']).strip().lower() in n_acc:
                        is_highlighted = True
                        break
                
                if is_highlighted:
                    return ['background-color: #d1e7ff; color: black'] * len(row)
                return [''] * len(row)

            # 3. AFFICHAGE
            st.dataframe(
                df_final.style.apply(style_separateurs, axis=1),
                use_container_width=True,
                hide_index=True
            )

elif st.session_state.resultats_recherche == []:
    st.warning("Aucun résultat correspondant à la recherche, essayez d'élargir les critères.")
