from math import sqrt
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from scipy.stats import norm

from src.stats.ab_tests import absolute_difference, conversion_rate, relative_difference
from src.ui.layout import methodological_note, page_header
from src.ui.styles import apply_base_styles


APP_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = APP_DIR / "assets"

VISITORS_A = 2000
CONVERSIONS_A = 190
VISITORS_B = 2000
CONVERSIONS_B = 230

HYPOTHESIS_OPTIONS = {
    "A": {"h0": r"p_B > p_A", "h1": r"p_B = p_A"},
    "B": {"h0": r"p_A = p_B", "h1": r"p_B > p_A"},
    "C": {"h0": r"p_A \ne p_B", "h1": r"p_A = p_B"},
    "D": {"h0": r"p_B < p_A", "h1": r"p_B > p_A"},
}


def display_landing_card(title: str, image_path: Path, caption: str) -> None:
    """Muestra una tarjeta visual para una version de landing page."""
    with st.container(border=True):
        st.subheader(title)
        if image_path.exists():
            try:
                st.image(str(image_path), use_container_width=True)
            except TypeError:
                st.image(str(image_path), use_column_width=True)
        else:
            st.warning(f"No se encontró la imagen {image_path.relative_to(APP_DIR)}")
        st.caption(caption)


def one_sided_two_proportion_z_test(
    conversions_a: int,
    visitors_a: int,
    conversions_b: int,
    visitors_b: int,
) -> dict[str, float]:
    """Calcula una prueba z unilateral para H1: p_B > p_A."""
    rate_a = conversion_rate(conversions_a, visitors_a)
    rate_b = conversion_rate(conversions_b, visitors_b)
    pooled_rate = (conversions_a + conversions_b) / (visitors_a + visitors_b)
    standard_error = sqrt(
        pooled_rate * (1 - pooled_rate) * ((1 / visitors_a) + (1 / visitors_b))
    )

    if standard_error == 0:
        raise ValueError("No se puede calcular la prueba z con error estándar cero.")

    z_score = (rate_b - rate_a) / standard_error
    p_value = 1 - norm.cdf(z_score)

    return {
        "rate_a": rate_a,
        "rate_b": rate_b,
        "pooled_rate": pooled_rate,
        "standard_error": standard_error,
        "z_score": z_score,
        "p_value": p_value,
    }


def format_percent(value: float, decimals: int = 2) -> str:
    """Formatea proporciones como porcentajes."""
    return f"{value:.{decimals}%}"


def format_percentage_points(value: float) -> str:
    """Formatea diferencias de proporciones como puntos porcentuales."""
    return f"{value * 100:.2f} pp"


def render_hypothesis_option(label: str, latex_h0: str, latex_h1: str) -> None:
    """Renderiza una opcion de hipotesis con matematicas legibles."""
    with st.container(border=True):
        label_col, h0_col, h1_col = st.columns([0.45, 1.7, 1.7])
        label_col.markdown(f"**{label}.**")
        h0_col.latex(rf"H_0: {latex_h0}")
        h1_col.latex(rf"H_1: {latex_h1}")


def verify_hypothesis(selected_option: str | None) -> None:
    """Muestra retroalimentacion para la pregunta de hipotesis."""
    if selected_option is None:
        st.warning("Selecciona una opción antes de verificar.")
        return

    st.session_state["case_hypothesis_checked"] = True
    st.session_state["case_hypothesis_selected"] = selected_option

    if selected_option == "B":
        st.success(
            r"Correcto. La hipótesis nula $H_0$ representa ausencia de mejora y la "
            r"hipótesis alternativa $H_1$ expresa que $p_B > p_A$."
        )
    else:
        st.warning(
            r"No es el planteamiento correcto. Para una prueba unilateral de mejora, "
            r"$H_0$ representa que no hay mejora frente a A y $H_1$ plantea que "
            r"$p_B > p_A$."
        )


def verify_interpretation(selected_option: str | None) -> None:
    """Muestra retroalimentacion para la pregunta de interpretacion."""
    if selected_option is None:
        st.warning("Selecciona una opción antes de verificar.")
        return

    st.session_state["case_interpretation_checked"] = True
    st.session_state["case_interpretation_selected"] = selected_option

    if selected_option.startswith("B."):
        st.success(
            "Correcto. La conclusión debe expresarse en términos de evidencia "
            r"estadística frente a $H_0$, no como certeza absoluta."
        )
    else:
        st.warning(
            "No es la interpretación más adecuada. En una prueba de hipótesis se "
            r"evalúa si la evidencia es suficiente para rechazar $H_0$ bajo el nivel "
            "de significancia seleccionado."
        )


st.set_page_config(page_title="Caso de estudio | A/B Testing", page_icon="📈", layout="wide")
apply_base_styles()

page_header(
    title="Caso de estudio: ¿la nueva landing page convierte mejor?",
    subtitle="Aplicación guiada de un A/B Test con datos sintéticos.",
)

st.write(
    """
    La empresa decide no sustituir automáticamente la landing page actual. En su
    lugar, ejecuta un experimento: una parte de los visitantes ve la versión A y
    otra parte ve la versión B. El objetivo es evaluar si la nueva página mejora
    la tasa de conversión.
    """
)

st.subheader("Versiones comparadas")
landing_a_col, landing_b_col = st.columns(2)

with landing_a_col:
    display_landing_card(
        title="Versión A: landing page actual",
        image_path=ASSETS_DIR / "landing_a.svg",
        caption="Grupo de control",
    )

with landing_b_col:
    display_landing_card(
        title="Versión B: nueva landing page",
        image_path=ASSETS_DIR / "landing_b.svg",
        caption="Grupo de tratamiento",
    )

st.subheader("Datos observados")

rate_a = conversion_rate(CONVERSIONS_A, VISITORS_A)
rate_b = conversion_rate(CONVERSIONS_B, VISITORS_B)
abs_diff = absolute_difference(rate_b, rate_a)
rel_diff = relative_difference(rate_b, rate_a)

observed_df = pd.DataFrame(
    [
        {
            "Versión": "A: landing page actual",
            "Visitantes": VISITORS_A,
            "Conversiones": CONVERSIONS_A,
            "Tasa de conversión": format_percent(rate_a),
        },
        {
            "Versión": "B: nueva landing page",
            "Visitantes": VISITORS_B,
            "Conversiones": CONVERSIONS_B,
            "Tasa de conversión": format_percent(rate_b),
        },
    ]
)

st.dataframe(observed_df, use_container_width=True, hide_index=True)

metric_a_col, metric_b_col, metric_abs_col, metric_rel_col = st.columns(4)
metric_a_col.metric("Conversión A", format_percent(rate_a))
metric_b_col.metric("Conversión B", format_percent(rate_b))
metric_abs_col.metric("Diferencia absoluta", format_percentage_points(abs_diff))
metric_rel_col.metric("Diferencia relativa", format_percent(rel_diff))

st.subheader("Paso 1. Formular las hipótesis")
st.write(
    "Como la empresa desea saber si la versión B mejora la conversión respecto a "
    "la versión A, se plantea una prueba unilateral."
)

st.markdown("**¿Cuál es el planteamiento correcto de las hipótesis?**")
hypothesis_selection = st.radio(
    "Selecciona una opción:",
    ["A", "B", "C", "D"],
    index=None,
    horizontal=True,
    key="case_hypothesis_radio",
)

for option_label, hypothesis in HYPOTHESIS_OPTIONS.items():
    render_hypothesis_option(
        label=option_label,
        latex_h0=hypothesis["h0"],
        latex_h1=hypothesis["h1"],
    )

if st.button("Verificar hipótesis"):
    verify_hypothesis(hypothesis_selection)
elif st.session_state.get("case_hypothesis_checked"):
    verify_hypothesis(st.session_state.get("case_hypothesis_selected"))

st.markdown("**Lectura de las hipótesis**")
st.markdown(
    r"""
    $p_A$ representa la tasa real de conversión de la versión A y
    $p_B$ representa la tasa real de conversión de la versión B.
    $H_0$ representa ausencia de mejora; $H_1$ representa la mejora que se desea detectar.
    """
)

st.subheader("Paso 2. Elegir el nivel de significancia")
st.write(
    "El nivel de significancia define el umbral para decidir si la evidencia "
    "observada es suficientemente fuerte contra la hipótesis nula."
)

alpha = st.radio(
    "Selecciona α:",
    options=[0.10, 0.05, 0.01],
    index=1,
    format_func=lambda value: f"{value:.2f}",
    horizontal=True,
)

st.subheader("Paso 3. Analizar los resultados")

with st.container(border=True):
    st.markdown("**¿Qué evalúa la prueba?**")
    st.markdown(
        r"""
        En esta prueba se compara la diferencia observada entre las tasas de
        conversión de B y A contra la diferencia que esperaríamos observar por
        variabilidad muestral si no existiera una mejora real. El estadístico $z$
        resume qué tan lejos está la diferencia observada del escenario planteado
        por la hipótesis nula.

        Como la hipótesis alternativa es $H_1: p_B > p_A$, se utiliza una prueba
        unilateral a la derecha. Por ello, el valor p representa la probabilidad
        de observar una diferencia tan grande como la obtenida, o mayor,
        suponiendo que $H_0$ fuera cierta.
        """
    )

test_result = one_sided_two_proportion_z_test(
    conversions_a=CONVERSIONS_A,
    visitors_a=VISITORS_A,
    conversions_b=CONVERSIONS_B,
    visitors_b=VISITORS_B,
)

reject_h0 = bool(np.less(test_result["p_value"], alpha))

analysis_col_1, analysis_col_2, analysis_col_3 = st.columns(3)
analysis_col_1.metric("Estadístico z", f"{test_result['z_score']:.3f}")
analysis_col_2.metric("Valor p", f"{test_result['p_value']:.4f}")
analysis_col_3.metric("Alpha seleccionado", f"{alpha:.2f}")

st.subheader("Lectura del resultado")

if reject_h0:
    st.markdown(
        rf"""
        El valor p obtenido es ${test_result["p_value"]:.4f}$, que es menor que
        el nivel de significancia seleccionado $\alpha = {alpha:.2f}$. Por tanto,
        la evidencia observada es suficientemente fuerte para rechazar $H_0$.
        """
    )
else:
    st.markdown(
        rf"""
        El valor p obtenido es ${test_result["p_value"]:.4f}$, que es mayor o
        igual que el nivel de significancia seleccionado $\alpha = {alpha:.2f}$.
        Por tanto, la evidencia observada no es suficientemente fuerte para
        rechazar $H_0$.
        """
    )

st.caption(
    r"Un valor $z$ positivo indica que la tasa observada de B es mayor que la de A. "
    r"Sin embargo, la decisión no depende solo del signo de $z$, sino de si el "
    r"valor p asociado es menor que $\alpha$."
)

if reject_h0:
    st.success(
        r"Decisión estadística: Existe evidencia estadística para rechazar $H_0$ y "
        "apoyar que la versión B mejora la conversión."
    )
else:
    st.warning(
        "Decisión estadística: No existe evidencia estadística suficiente para "
        r"rechazar $H_0$. Con estos datos, no se puede afirmar que B mejore la conversión."
    )

st.subheader("Paso 4. Interpretar la conclusión")

if reject_h0:
    interpretation_options = [
        "A. Se acepta definitivamente que B siempre será mejor que A.",
        "B. Existe evidencia estadística para rechazar H₀ y apoyar que B mejora la conversión.",
        "C. Se acepta H₀ porque las tasas observadas son diferentes.",
        "D. No se puede concluir nada porque los A/B Tests no aplican a marketing.",
    ]
else:
    interpretation_options = [
        "A. Se demuestra que A y B tienen exactamente la misma conversión.",
        "B. No existe evidencia estadística suficiente para rechazar H₀ con estos datos.",
        "C. Se acepta que B es peor que A.",
        "D. Se debe adoptar B porque su tasa observada es mayor.",
    ]

interpretation_selection = st.radio(
    "Con el nivel de significancia seleccionado, ¿cuál es la conclusión más adecuada?",
    interpretation_options,
    index=None,
    key=f"case_interpretation_radio_{alpha}",
)

if st.button("Verificar conclusión"):
    verify_interpretation(interpretation_selection)
elif st.session_state.get("case_interpretation_checked"):
    verify_interpretation(st.session_state.get("case_interpretation_selected"))

st.subheader("Paso 5. Traducir la evidencia en una decisión de marketing")
st.write(
    """
    El resultado estadístico es una parte de la decisión. Antes de adoptar la nueva
    landing page, el equipo también debe valorar si la mejora estimada justifica
    los costos de implementación, si el efecto es relevante para el negocio y si
    existen riesgos operativos o de experiencia de usuario.
    """
)

methodological_note(
    "Idea clave: Un A/B Test bien interpretado no solo responde si una diferencia "
    "observada puede atribuirse al azar; también ayuda a decidir si esa diferencia "
    "es suficientemente relevante para actuar."
)
