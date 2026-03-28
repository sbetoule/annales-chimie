import streamlit as st
import pandas as pd

st.set_page_config(page_title="Annales Lab", layout="wide")

# --- URLS DES FLUX ---
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTsADsmsMnYgQXIUlU25_FlKrtTffM5XOL69taw9Pco8AHV4suIUtT0tg384XBtBAo28qGKGbtSJtIy/pub?gid=0&single=true&output=csv"
URL_THEMES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTsADsmsMnYgQXIUlU25_FlKrtTffM5XOL69taw9Pco8AHV4suIUtT0tg384XBtBAo28qGKGbtSJtIy/pub?gid=1733310474&single=true&output=csv"
URL_NIVEAUX = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTsADsmsMnYgQXIUlU25_FlKrtTffM5XOL69taw9Pco8AHV4suIUtT0tg384XBtBAo28qGKGbtSJtIy/pub?gid=1879771001&single=true&output=csv"

@st.cache_data(ttl=60)
def recuperer_listes(url_themes, url_niveaux):
    # Lecture des thèmes (Ligne 1)
    df_t = pd.read_csv(url_themes, header=None)
    # .iloc[0] récupère la première ligne, .tolist() en fait une liste
    themes = df_t.iloc[0].dropna().astype(str).tolist()
    
    # Lecture des niveaux (Ligne 1)
    df_n = pd.read_csv(url_niveaux, header=None)
    # On récupère la ligne 1 et on ajoute "Peu importe" au début
    niveaux_bruts = df_n.iloc[0].dropna().astype(str).tolist()
    niveaux = ["Peu importe"] + niveaux_bruts
    
    return themes, niveaux

# Chargement dynamique des listes
THEMES_LISTE, DIFF_LISTE = recuperer_listes(URL_THEMES, URL_NIVEAUX)

# --- INITIALISATION DE LA MÉMOIRE ---
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
            if pd.isna(nom_sujet) or str(nom_sujet).strip() == "":
                continue
            
            auteur = df.iloc[0, i]
            annee = df.iloc[2, i]
            questions = df.iloc[4:, i : i+4].copy()
            
            # Renommage explicite des colonnes selon votre demande
            questions.columns = ['Numéro', 'Thème', 'Difficulté', 'Remarque']
            
            questions = questions.dropna(subset=['Thème'])
            questions = questions[questions['Thème'].astype(str).str.lower() != "thème"]
            
            sujets.append({
                "nom": str(nom_sujet).strip(),
                "auteur": str(auteur).strip() if pd.notna(auteur) else "Inconnu",
                "annee": str(annee).strip() if pd.notna(annee) else "N/A",
                "questions": questions,
                # Label combiné pour la liste déroulante
                "label": f"{str(nom_sujet).strip()} ({str(annee).strip()})"
            })
        return sujets
    except Exception as e:
        st.error(f"Erreur : {e}")
        return []

st.title("🧪 Recherche d'Annales")

# --- BARRE LATÉRALE (FILTRES) ---
with st.sidebar:
    st.header("Paramètres")
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
if st.button("🚀 Lancer la recherche", type="primary"):
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

# --- AFFICHAGE (SI RÉSULTATS EN MÉMOIRE) ---
if st.session_state.resultats_recherche is not None:
    res = st.session_state.resultats_recherche
    
    if res:
        st.success(f"{len(res)} sujet(s) trouvé(s)")
        
        # Tableau résumé
        df_res = pd.DataFrame([{
            "Sujet": r.get('nom', 'Inconnu'),
            "Année": r.get('annee', 'N/A'),
            "Auteur": r.get('auteur', 'Inconnu'),
            "Détails": r.get('stats', '')
        } for r in res])
        st.table(df_res)
        
        st.divider()
        
        # SÉCURITÉ : On vérifie si 'label' existe, sinon on utilise 'nom'
        options_affichage = [r.get('label', r.get('nom', 'Sujet sans nom')) for r in res]
        
        choix_label = st.selectbox("Afficher les détails du sujet :", options_affichage)
        
        # Récupération du sujet (recherche par label ou par nom)
        try:
            data_sujet = next(r['questions'] for r in res if r.get('label') == choix_label or r.get('nom') == choix_label)
            st.subheader(f"Contenu : {choix_label}")
            st.dataframe(data_sujet, use_container_width=True, hide_index=True)
        except StopIteration:
            st.warning("Sélectionnez un sujet pour voir les détails.")
    else:
        st.warning("Aucun résultat trouvé.")