import streamlit as st

from src.ui.layout import info_box, methodological_note, page_header
from src.ui.styles import apply_base_styles


st.set_page_config(
    page_title="A/B Testing | Analitica del Marketing",
    page_icon="📊",
    layout="wide",
)

apply_base_styles()

page_header(
    title="A/B Testing",
    subtitle="Aplicacion educativa para un curso de Analitica del Marketing a nivel posgrado.",
)

info_box(
    title="Estructura del curso",
    body=(
        "Esta aplicacion servira como base para integrar conceptos, metodologia, "
        "casos de estudio, simulaciones y buenas practicas de experimentacion."
    ),
)

methodological_note(
    "Por ahora la aplicacion contiene solo la estructura modular. "
    "Cada pagina queda lista para incorporar contenido didactico e interactividad."
)

st.divider()

st.subheader("Navegacion sugerida")
st.write(
    "Usa el menu lateral para explorar las secciones iniciales: introduccion, "
    "metodologia, caso de estudio, simulador y buenas practicas."
)
