import streamlit as st
import streamlit.components.v1 as components

# 1. Configuration de la page (doit être la toute première commande Streamlit)
st.set_page_config(page_title="Annales Lab Chimie", layout="wide")

# 2. Injection du code Google Analytics
ga_code = """
<script async src="https://www.googletagmanager.com/gtag/js?id=G-G7EE1V3XFL"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-G7EE1V3XFL');
</script>
"""

# Utilisation d'un composant vide pour injecter le JS dans le DOM
st.components.v1.html(ga_code, height=0)
