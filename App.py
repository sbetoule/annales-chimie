import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Annales Lab Chimie", layout="wide")

# --- TEST DE SURVIE (SCÉNARIO B) ---
st.write("### Diagnostic : Si vous voyez ce message, le script fonctionne.")
st.sidebar.success("La sidebar est active !")

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

with st.sidebar:
    st.write("### 🔍 Diagnostic Source")
    if not THEMES_LISTE or THEMES_LISTE == ["Erreur"]:
        st.error("❌ Les thèmes n'ont pas pu être chargés depuis Google Sheets.")
    else:
        st.success(f"✅ {len(THEMES_LISTE)} thèmes chargés.")
        st.write("Aperçu :", THEMES_LISTE[:3]) # Affiche les 3 premiers

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
