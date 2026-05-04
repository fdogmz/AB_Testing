import pandas as pd
import streamlit as st

from src.ui.layout import info_box, methodological_note, page_header
from src.ui.styles import apply_base_styles


st.set_page_config(
    page_title="Cuándo usar A/B Testing | A/B Testing",
    page_icon="🧭",
    layout="wide",
)
apply_base_styles()

page_header(
    title="¿Cuándo conviene usar A/B Testing?",
    subtitle=(
        "Del caso de la landing page a otras decisiones de marketing que pueden "
        "evaluarse experimentalmente."
    ),
)

st.write(
    """
    El A/B Testing permite convertir una decisión de marketing en un experimento
    controlado. En lugar de elegir la versión que parece mejor, se compara el
    desempeño de dos alternativas con usuarios reales y una métrica previamente
    definida.
    """
)

info_box(
    title="De una opinión a una comparación controlada",
    body=(
        "Un A/B Test es útil cuando se desea comparar alternativas bajo condiciones "
        "similares, medir su efecto sobre una métrica definida y tomar una decisión "
        "con base en evidencia."
    ),
)

st.subheader("Situaciones típicas en marketing")

examples_df = pd.DataFrame(
    [
        {
            "Decisión de marketing": "Landing page",
            "Versión A": "Diseño actual",
            "Versión B": "Nuevo diseño",
            "Métrica posible": "Tasa de conversión",
        },
        {
            "Decisión de marketing": "Email marketing",
            "Versión A": "Asunto tradicional",
            "Versión B": "Asunto personalizado",
            "Métrica posible": "Tasa de apertura",
        },
        {
            "Decisión de marketing": "Botón o llamada a la acción",
            "Versión A": "Descargar guía",
            "Versión B": "Quiero mi guía gratis",
            "Métrica posible": "Clics o registros",
        },
        {
            "Decisión de marketing": "Promoción comercial",
            "Versión A": "10% de descuento",
            "Versión B": "Envío gratis",
            "Métrica posible": "Compras o ingreso promedio",
        },
        {
            "Decisión de marketing": "Anuncio digital",
            "Versión A": "Imagen del producto",
            "Versión B": "Imagen con beneficio principal",
            "Métrica posible": "CTR",
        },
        {
            "Decisión de marketing": "Proceso de checkout",
            "Versión A": "Formulario largo",
            "Versión B": "Formulario simplificado",
            "Métrica posible": "Tasa de abandono",
        },
        {
            "Decisión de marketing": "Recomendaciones de producto",
            "Versión A": "Recomendaciones genéricas",
            "Versión B": "Recomendaciones personalizadas",
            "Métrica posible": "Clics o compras",
        },
    ]
)

st.dataframe(examples_df, use_container_width=True, hide_index=True)

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("¿Cuándo es recomendable?")
    st.markdown(
        """
        - Cuando hay una decisión concreta entre alternativas.
        - Cuando se puede asignar usuarios de manera comparable.
        - Cuando existe una métrica clara y observable.
        - Cuando el resultado puede medirse después de la exposición.
        - Cuando el cambio puede implementarse de forma controlada.
        """
    )

with right_col:
    st.subheader("¿Cuándo hay que tener cuidado?")
    st.markdown(
        """
        - Cuando hay poco tráfico o tamaño de muestra insuficiente.
        - Cuando no se puede controlar quién ve cada versión.
        - Cuando otros cambios ocurren al mismo tiempo y contaminan la comparación.
        - Cuando la métrica no está bien definida.
        - Cuando el experimento puede generar riesgos éticos, legales o reputacionales.
        """
    )

st.divider()

st.subheader("Puente hacia la metodología")
st.write(
    """
    Una vez identificada una decisión susceptible de experimentación, el siguiente
    paso es diseñar correctamente la prueba: definir hipótesis, seleccionar la
    métrica, asignar usuarios, calcular resultados e interpretar la evidencia.
    """
)

methodological_note(
    "El A/B Testing no reemplaza el criterio de marketing; lo organiza como una "
    "comparación medible cuando la decisión puede observarse en el comportamiento "
    "de usuarios reales."
)
