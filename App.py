import streamlit as st
from streamlit_analytics2 import track

# On entoure tout le code par la fonction track()
with track():
    st.title("Annales Lab Chimie")
    # ... le reste de votre code ...
    st.write("Bienvenue sur l'application.")
