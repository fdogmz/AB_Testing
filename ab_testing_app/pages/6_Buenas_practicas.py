import streamlit as st

from src.ui.layout import methodological_note, page_header
from src.ui.styles import apply_base_styles


st.set_page_config(page_title="Buenas practicas | A/B Testing", page_icon="✅", layout="wide")
apply_base_styles()

page_header(
    title="Buenas practicas",
    subtitle="Criterios para planear, ejecutar y comunicar experimentos con rigor.",
)

methodological_note(
    "Aqui se agregaran recomendaciones sobre validez, sesgos, lectura de resultados y comunicacion ejecutiva."
)
