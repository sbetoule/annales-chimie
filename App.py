import streamlit as st
import pandas as pd

st.set_page_config(page_title="Annales Lab", layout="wide")

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
        niveaux_bruts = df_n.iloc[0].dropna().astype(str).tolist()
        niveaux = ["Peu importe"] + niveaux_bruts
        return themes, niveaux
    except:
        return ["Erreur"], ["Peu importe"]

THEMES_LISTE, DIFF_LISTE = recuperer_listes(URL_THEMES, URL_NIVEAUX)

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
            auteur = df.iloc[0, i]
            annee = df.iloc[2, i]
            questions = df.iloc[4:, i : i+4].copy()
            questions.columns = ['Numéro', 'Thème', 'Difficulté', 'Remarque']
            questions = questions.dropna(subset=['Thème'])
            questions = questions[questions['Thème'].astype(str).str.lower() != "thème"]
            sujets.append({
                "nom": str(nom_sujet).strip(),
                "auteur": str(auteur).strip() if pd.notna(auteur) else "Inconnu",
                "annee": str(annee).strip() if pd.notna(annee) else "N/A",
                "questions": questions,
                "label": f"{str(nom_sujet).strip()} ({str(annee).strip()})"
            })
        return sujets
    except Exception as e:
        st.error(f"Erreur : {e}"); return []

# --- BANDEAU DES CRÉDITS ---
st.caption("🛠️ **Conception et Développement :**")
st.markdown("""
<div style="font-size: 0.9rem; color: #555; border-bottom: 1px solid #ddd; padding-bottom: 10px; margin-bottom: 20px;">
    <b>Sylvain Betoule</b> (Doctorant, Sorbonne Université) • 
    <b>Ulysse Garnier</b> (Doctorant, Sorbonne Université) • 
    <b>Morgane Leite</b> (Resp. Agrégation Chimie, ENS)
</div>
""", unsafe_allow_html=True)

st.title("🧪 Recherche d'Annales de Chimie")

# --- INSTRUCTIONS DE DÉPART (Point 3 ajouté) ---
with st.expander("👋 Comment utiliser cet outil ?", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**1. Filtres**")
        st.info("⬅️ Cliquez sur la flèche en haut à gauche (mobile) pour choisir vos thèmes.")
    with c2:
        st.markdown("**2. Recherche**")
        st.info("Cliquez sur le bouton rouge **🚀 Lancer la recherche** en bas.")
    with c3:
        st.markdown("**3. Analyse**")
        st.info("Sélectionnez un sujet en bas : les questions ciblées apparaîtront en couleur.")

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.header("⚙️ Paramètres")
    criteres = []
    for n in range(st.session_state.nb_filtres):
        st.subheader(f"Filtre {n+1}")
        t = st.selectbox(f"Thème", THEMES_LISTE, key=f"t_{n}")
        d = st.selectbox(f"Difficulté", DIFF_LISTE, key=f"d_{n}")
        m = st.number_input(f"Quantité", min_value=1, value=1, key=f"m_{n}")
        criteres.append({"theme": t, "diff": d, "min": m})
    
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
            mask = q['Thème'].astype(str).str.contains(c['theme'], case=False, na=False)
            if c['diff'] != "Peu importe":
                mask &= (q['Difficulté'].astype(str).str.strip() == c['diff'])
            count = len(q[mask])
            stats.append(f"{c['theme']} : {count}")
            if count < c['min']:
                valid = False
                break
        if valid:
            s['stats'] = " | ".join(stats)
            trouves.append(s)
    st.session_state.resultats_recherche = trouves

# --- AFFICHAGE ---
if st.session_state.resultats_recherche is not None:
    res = st.session_state.resultats_recherche
    if res:
        st.success(f"✅ {len(res)} sujet(s) trouvé(s)")
        df_res = pd.DataFrame([{"Sujet": r['nom'], "Année": r['annee'], "Auteur": r['auteur'], "Détails": r['stats']} for r in res])
        st.table(df_res)
        
        st.divider()
        options_affichage = [r.get('label', r.get('nom')) for r in res]
        choix_label = st.selectbox("🔍 Afficher les détails du sujet :", options_affichage)
        
        sujet_choisi = next(r for r in res if r['label'] == choix_label)
        df_details = sujet_choisi['questions']
        
        # Fonction de mise en couleur
        def highlight_rows(row):
            for c in criteres:
                theme_match = c['theme'].lower() in str(row['Thème']).lower()
                diff_match = (c['diff'] == "Peu importe") or (str(row['Difficulté']).strip() == c['diff'])
                if theme_match and diff_match:
                    return ['background-color: #d1e7ff; color: black'] * len(row)
            return [''] * len(row)

        st.subheader(f"Détails : {choix_label}")
        st.markdown("*Les lignes surlignées en bleu correspondent à vos critères.*")
        
        styled_df = df_details.style.apply(highlight_rows, axis=1)
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Aucun résultat ne correspond à tous vos critères.")