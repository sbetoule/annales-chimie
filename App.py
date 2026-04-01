import streamlit as st
import streamlit.components.v1 as components

def add_analytics():
    ga_js = """
    <script>
        var script = window.parent.document.createElement('script');
        script.async = true;
        script.src = 'https://www.googletagmanager.com/gtag/js?id=G-G7EE1V3XFL';
        window.parent.document.head.appendChild(script);

        var config = window.parent.document.createElement('script');
        config.innerHTML = "window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'G-G7EE1V3XFL');";
        window.parent.document.head.appendChild(config);
    </script>
    """
    components.html(ga_js, height=0)

# Appelez la fonction au début
add_analytics()
