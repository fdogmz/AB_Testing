import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from scipy.stats import norm

from src.ui.layout import info_box, methodological_note, page_header
from src.ui.styles import apply_base_styles


def two_proportion_z_test(
    x_a: np.ndarray,
    n_a: int,
    x_b: np.ndarray,
    n_b: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Calcula z y valor p unilateral para H1: p_B > p_A."""
    p_a_hat = x_a / n_a
    p_b_hat = x_b / n_b
    pooled = (x_a + x_b) / (n_a + n_b)
    standard_error = np.sqrt(pooled * (1 - pooled) * ((1 / n_a) + (1 / n_b)))

    z_score = np.divide(
        p_b_hat - p_a_hat,
        standard_error,
        out=np.zeros_like(p_a_hat, dtype=float),
        where=standard_error > 0,
    )
    p_value = 1 - norm.cdf(z_score)
    return z_score, p_value


def run_ab_simulation(
    p_a: float,
    p_b: float,
    n_per_group: int,
    alpha: float,
    n_simulations: int,
    seed: int,
) -> pd.DataFrame:
    """Simula muchos experimentos A/B independientes."""
    rng = np.random.default_rng(seed)
    conversions_a = rng.binomial(n=n_per_group, p=p_a, size=n_simulations)
    conversions_b = rng.binomial(n=n_per_group, p=p_b, size=n_simulations)

    rate_a = conversions_a / n_per_group
    rate_b = conversions_b / n_per_group
    diff = rate_b - rate_a
    z_score, p_value = two_proportion_z_test(
        x_a=conversions_a,
        n_a=n_per_group,
        x_b=conversions_b,
        n_b=n_per_group,
    )

    return pd.DataFrame(
        {
            "conversiones_a": conversions_a,
            "conversiones_b": conversions_b,
            "tasa_a": rate_a,
            "tasa_b": rate_b,
            "diff": diff,
            "diff_pp": diff * 100,
            "z_score": z_score,
            "p_value": p_value,
            "significativo": p_value < alpha,
        }
    )


def summarize_simulation(
    results_df: pd.DataFrame,
    p_a: float,
    p_b: float,
    alpha: float,
) -> dict[str, float]:
    """Resume los resultados agregados de la simulacion."""
    return {
        "significant_rate": float(results_df["significativo"].mean()),
        "true_diff": p_b - p_a,
        "mean_observed_diff": float(results_df["diff"].mean()),
        "median_p_value": float(results_df["p_value"].median()),
        "alpha": alpha,
    }


def format_percent(value: float, decimals: int = 1) -> str:
    """Formatea proporciones como porcentajes."""
    return f"{value:.{decimals}%}"


def format_pp(value: float) -> str:
    """Formatea una diferencia de proporciones en puntos porcentuales."""
    return f"{value * 100:.2f} pp"


def add_vertical_line(fig, x_value: float, label: str, color: str) -> None:
    """Agrega una linea vertical y una anotacion a una grafica Plotly."""
    fig.add_vline(x=x_value, line_width=2, line_dash="dash", line_color=color)
    fig.add_annotation(
        x=x_value,
        y=1,
        yref="paper",
        text=label,
        showarrow=False,
        xanchor="left",
        font=dict(color=color),
    )


st.set_page_config(page_title="Simulador | A/B Testing", page_icon="🎛️", layout="wide")
apply_base_styles()

page_header(
    title="Simulador: ¿qué tan estable es un A/B Test?",
    subtitle="Exploración interactiva de variabilidad muestral, significancia y poder estadístico.",
)

st.write(
    """
    En el caso de estudio analizamos un experimento observado. En este simulador
    repetiremos muchos experimentos bajo condiciones conocidas para observar qué
    tan frecuente es detectar una diferencia estadísticamente significativa.
    """
)

info_box(
    title="¿Qué representa esta simulación?",
    body=(
        "Esta simulación equivale a repetir muchas veces el experimento de comparar "
        "dos landing pages. En cada repetición, el tráfico se asigna aleatoriamente "
        "entre la versión A y la versión B, y se observa cuántos usuarios convierten "
        "en cada grupo. Así podemos estudiar cómo cambian los resultados de un A/B "
        "Test debido al azar muestral. Un solo A/B Test muestra un resultado posible; "
        "la simulación permite observar muchos resultados posibles bajo las mismas "
        "condiciones."
    ),
    kind="info",
)

info_box(
    title="¿Por qué simular?",
    body=(
        "Un único A/B Test muestra un resultado posible. La simulación permite "
        "repetir el experimento muchas veces para observar la variabilidad de las "
        "tasas observadas, los valores p y las decisiones estadísticas."
    ),
    kind="method",
)

st.sidebar.header("Controles del simulador")
p_a = st.sidebar.slider(
    "Tasa real de conversión A",
    min_value=0.01,
    max_value=0.30,
    value=0.095,
    step=0.005,
    format="%.3f",
)
p_b = st.sidebar.slider(
    "Tasa real de conversión B",
    min_value=0.01,
    max_value=0.30,
    value=0.115,
    step=0.005,
    format="%.3f",
)
n_per_group = st.sidebar.slider(
    "Visitantes por grupo",
    min_value=100,
    max_value=10000,
    value=2000,
    step=100,
)
alpha = st.sidebar.selectbox(
    "Nivel de significancia alpha",
    options=[0.10, 0.05, 0.01],
    index=1,
    format_func=lambda value: f"{value:.2f}",
)
n_simulations = st.sidebar.slider(
    "Número de experimentos simulados",
    min_value=100,
    max_value=5000,
    value=1000,
    step=100,
)
seed = st.sidebar.number_input("Semilla aleatoria", value=42, step=1)
simulate_clicked = st.sidebar.button("Simular experimentos", type="primary")

if simulate_clicked or "simulator_results" not in st.session_state:
    st.session_state["simulator_results"] = run_ab_simulation(
        p_a=p_a,
        p_b=p_b,
        n_per_group=n_per_group,
        alpha=alpha,
        n_simulations=n_simulations,
        seed=int(seed),
    )
    st.session_state["simulator_params"] = {
        "p_a": p_a,
        "p_b": p_b,
        "n_per_group": n_per_group,
        "alpha": alpha,
        "n_simulations": n_simulations,
        "seed": int(seed),
    }

results_df = st.session_state["simulator_results"]
params = st.session_state["simulator_params"]
summary = summarize_simulation(
    results_df=results_df,
    p_a=params["p_a"],
    p_b=params["p_b"],
    alpha=params["alpha"],
)
true_diff = summary["true_diff"]

st.subheader("Resultados agregados")
metric_1, metric_2, metric_3, metric_4 = st.columns(4)
metric_1.metric("Experimentos significativos", format_percent(summary["significant_rate"]))
metric_2.metric("Diferencia real", format_pp(summary["true_diff"]))
metric_3.metric("Diferencia promedio observada", format_pp(summary["mean_observed_diff"]))
metric_4.metric("Valor p mediano", f"{summary['median_p_value']:.4f}")

if params["p_b"] > params["p_a"]:
    info_box(
        title="Interpretación",
        body=(
            "La proporción de experimentos significativos aproxima el poder "
            "estadístico: la probabilidad de detectar una mejora cuando la mejora "
            "realmente existe."
        ),
        kind="success",
    )
elif np.isclose(params["p_b"], params["p_a"], atol=1e-12) or abs(true_diff) < 0.001:
    info_box(
        title="Interpretación",
        body=(
            "Como no hay una mejora real, la proporción de experimentos "
            "significativos se interpreta como una aproximación a la tasa de "
            "falsos positivos."
        ),
        kind="warning",
    )
else:
    info_box(
        title="Interpretación",
        body=(
            "Como la prueba está planteada para detectar mejoras de B sobre A, "
            "una versión B peor debería producir pocos resultados significativos "
            "a favor de B."
        ),
        kind="warning",
    )

st.subheader("Visualizaciones")

diff_fig = px.histogram(
    results_df,
    x="diff_pp",
    nbins=40,
    title="Distribución de diferencias observadas",
    labels={"diff_pp": "Diferencia observada p_B_hat - p_A_hat (pp)", "count": "Frecuencia"},
)
add_vertical_line(diff_fig, 0, "0", "#6b7280")
add_vertical_line(diff_fig, true_diff * 100, "Diferencia real", "#2f6f8f")
diff_fig.update_layout(yaxis_title="Frecuencia", bargap=0.04)
st.plotly_chart(diff_fig, use_container_width=True)

pvalue_fig = px.histogram(
    results_df,
    x="p_value",
    nbins=40,
    title="Distribución de valores p",
    labels={"p_value": "Valor p", "count": "Frecuencia"},
)
add_vertical_line(pvalue_fig, params["alpha"], "alpha", "#c2410c")
pvalue_fig.update_layout(yaxis_title="Frecuencia", bargap=0.04)
st.plotly_chart(pvalue_fig, use_container_width=True)

decision_counts = (
    results_df["significativo"]
    .map({True: "Significativo", False: "No significativo"})
    .value_counts()
    .rename_axis("Decisión")
    .reset_index(name="Frecuencia")
)
decision_fig = px.bar(
    decision_counts,
    x="Decisión",
    y="Frecuencia",
    title="Decisiones estadísticas simuladas",
    text="Frecuencia",
    color="Decisión",
    color_discrete_map={"Significativo": "#2f6f8f", "No significativo": "#9ca3af"},
)
decision_fig.update_layout(showlegend=False)
st.plotly_chart(decision_fig, use_container_width=True)

st.subheader("Lectura guiada")

if params["p_b"] > params["p_a"] and params["n_per_group"] < 1000:
    st.write(
        "Aunque B sea realmente mejor en la simulación, un tamaño de muestra pequeño "
        "puede dificultar detectar la mejora."
    )
elif params["p_b"] > params["p_a"] and params["n_per_group"] >= 1000:
    st.write(
        "Con mayor tamaño de muestra, la prueba tiene más capacidad para detectar "
        "diferencias pequeñas."
    )

if np.isclose(params["p_a"], params["p_b"], atol=1e-12):
    st.write(
        "Cuando no hay diferencia real, algunos experimentos pueden resultar "
        "significativos por azar. Ese riesgo se relaciona con alpha."
    )

if params["alpha"] == 0.10:
    st.write(
        "Un alpha más alto hace la prueba menos exigente, pero aumenta el riesgo "
        "de falsos positivos."
    )
elif params["alpha"] == 0.01:
    st.write(
        "Un alpha más bajo hace la prueba más exigente, pero puede reducir la "
        "probabilidad de detectar mejoras reales pequeñas."
    )

st.subheader("Preguntas para explorar")

with st.expander("¿Qué ocurre si reduces el número de visitantes por grupo manteniendo las tasas reales?"):
    st.write(
        "La variabilidad aumenta y disminuye la proporción de experimentos "
        "significativos cuando la mejora real existe."
    )

with st.expander("¿Qué ocurre si igualas las tasas reales de A y B?"):
    st.write(
        "La proporción de resultados significativos se aproxima a la tasa de "
        "falsos positivos, que debería estar cerca del nivel de significancia "
        "seleccionado."
    )

with st.expander("¿Qué ocurre si la mejora real de B es muy pequeña?"):
    st.write(
        "Se requiere mayor tamaño de muestra para detectarla de forma confiable."
    )

methodological_note(
    "El resultado de un A/B Test depende tanto del efecto real como "
    "del tamaño de muestra y del nivel de significancia. Por eso, experimentar "
    "no es solo comparar tasas: también implica comprender la incertidumbre.",
    title="Idea clave",
    kind="success",
)
