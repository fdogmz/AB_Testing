import sqlite3
import uuid
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.ui.layout import info_box, methodological_note, page_header
from src.ui.styles import apply_base_styles


APP_DIR = Path(__file__).resolve().parents[1]
DB_DIR = APP_DIR / "data"
DB_PATH = DB_DIR / "ab_testing_app.db"
ASSETS_DIR = APP_DIR / "assets"

DECISION_OPTIONS = [
    "Adoptar la nueva página porque a la directora de marketing digital le agrada más.",
    "Adoptar la nueva página porque el equipo creativo considera que comunica mejor la propuesta de valor.",
    "Preguntar a algunos clientes o colegas cuál versión prefieren y elegir la más votada.",
    "Mostrar aleatoriamente ambas versiones a usuarios reales y comparar sus resultados.",
    "Mantener la página actual para evitar riesgos.",
]

OPTION_LABELS = {
    DECISION_OPTIONS[0]: "Preferencia directiva",
    DECISION_OPTIONS[1]: "Criterio creativo",
    DECISION_OPTIONS[2]: "Consulta informal",
    DECISION_OPTIONS[3]: "Comparación experimental",
    DECISION_OPTIONS[4]: "Mantener versión actual",
}

FEEDBACK_BY_OPTION = {
    DECISION_OPTIONS[0]: (
        "Intuición directiva",
        "La intuición directiva puede ser valiosa, especialmente cuando se basa en experiencia de mercado. "
        "Sin embargo, también puede introducir sesgos: lo que agrada internamente no necesariamente mejora "
        "la conversión de los usuarios reales.",
    ),
    DECISION_OPTIONS[1]: (
        "Criterio creativo",
        "Una mejor estética o una narrativa más clara no siempre se traducen en mejores resultados comerciales. "
        "La calidad percibida de una pieza debe contrastarse con datos de comportamiento.",
    ),
    DECISION_OPTIONS[2]: (
        "Preferencias declaradas",
        "Preguntar preferencias puede aportar información útil, pero lo que las personas dicen preferir no siempre "
        "coincide con su comportamiento real de compra, registro o clic.",
    ),
    DECISION_OPTIONS[3]: (
        "Enfoque experimental",
        "Esta opción se aproxima al enfoque experimental: asignar usuarios a versiones A y B, definir una métrica "
        "y comparar resultados. Esa es la lógica central de un A/B Test.",
    ),
    DECISION_OPTIONS[4]: (
        "Riesgo de no cambiar",
        "Evitar cambios puede reducir riesgos inmediatos, pero también puede impedir descubrir mejoras relevantes. "
        "No experimentar también tiene un costo de oportunidad.",
    ),
}


def init_db() -> None:
    """Crea la base SQLite local y la tabla de encuesta si no existen."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS intro_poll (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                opcion TEXT,
                session_id TEXT
            )
            """
        )
        conn.commit()


def get_or_create_session_id() -> str:
    """Obtiene o crea un identificador anonimo para la sesion actual."""
    if "intro_poll_session_id" not in st.session_state:
        st.session_state["intro_poll_session_id"] = str(uuid.uuid4())
    return st.session_state["intro_poll_session_id"]


def has_session_responded(session_id: str) -> bool:
    """Indica si la sesion actual ya registro una respuesta."""
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute(
            "SELECT 1 FROM intro_poll WHERE session_id = ? LIMIT 1",
            (session_id,),
        ).fetchone()
    return result is not None


def save_response(option: str, session_id: str) -> None:
    """Guarda una respuesta de la encuesta."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO intro_poll (timestamp, opcion, session_id)
            VALUES (?, ?, ?)
            """,
            (datetime.now().isoformat(timespec="seconds"), option, session_id),
        )
        conn.commit()


def load_poll_data() -> pd.DataFrame:
    """Carga todas las respuestas registradas."""
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(
            "SELECT id, timestamp, opcion, session_id FROM intro_poll ORDER BY id",
            conn,
        )


def summarize_poll(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula frecuencia y porcentaje por opcion."""
    base = pd.DataFrame({"opcion": DECISION_OPTIONS})

    if df.empty:
        base["frecuencia"] = 0
    else:
        counts = df["opcion"].value_counts().rename_axis("opcion").reset_index(name="frecuencia")
        base = base.merge(counts, on="opcion", how="left").fillna({"frecuencia": 0})

    base["frecuencia"] = base["frecuencia"].astype(int)
    total = int(base["frecuencia"].sum())
    base["porcentaje"] = 0.0 if total == 0 else base["frecuencia"] / total
    base["porcentaje_texto"] = base["porcentaje"].map(lambda value: f"{value:.1%}")
    base["opcion_corta"] = base["opcion"].map(OPTION_LABELS)
    return base


def plot_poll_results(summary_df: pd.DataFrame):
    """Construye una grafica de barras con los resultados acumulados."""
    fig = px.bar(
        summary_df,
        x="opcion_corta",
        y="frecuencia",
        text="porcentaje_texto",
        hover_data={"opcion": True, "porcentaje_texto": True, "opcion_corta": False},
        labels={
            "opcion_corta": "Opción",
            "frecuencia": "Frecuencia",
            "porcentaje_texto": "Porcentaje",
        },
    )
    fig.update_traces(textposition="outside", marker_color="#2f6f8f")
    fig.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=30, b=20),
        yaxis=dict(dtick=1, rangemode="tozero"),
        xaxis_tickangle=-20,
        showlegend=False,
    )
    return fig


def reset_poll() -> None:
    """Elimina las respuestas actuales de la encuesta."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM intro_poll")
        conn.execute("DELETE FROM sqlite_sequence WHERE name = 'intro_poll'")
        conn.commit()


def get_session_response(session_id: str) -> str | None:
    """Consulta SQLite y devuelve la opcion registrada por la sesion actual."""
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute(
            """
            SELECT opcion
            FROM intro_poll
            WHERE session_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (session_id,),
        ).fetchone()

    if result is None:
        return None
    return str(result[0])


def render_majority_interpretation(summary_df: pd.DataFrame) -> None:
    """Muestra una lectura didactica de la respuesta mayoritaria."""
    if summary_df["frecuencia"].sum() == 0:
        return

    leading_option = str(summary_df.sort_values("frecuencia", ascending=False).iloc[0]["opcion"])

    if leading_option == DECISION_OPTIONS[3]:
        interpretation = (
            "La mayoría del grupo se aproxima al razonamiento experimental propio del A/B Testing: "
            "comparar versiones bajo condiciones equivalentes y con una métrica definida."
        )
    elif leading_option == DECISION_OPTIONS[4]:
        interpretation = (
            "La mayoría está privilegiando la reducción del riesgo inmediato. Esta postura puede ser prudente, "
            "pero también puede implicar un costo de oportunidad si la nueva versión hubiera mejorado el desempeño."
        )
    else:
        interpretation = (
            "La mayoría está privilegiando criterios útiles, como intuición, autoridad, criterio creativo o consulta "
            "informal, pero insuficientes para establecer evidencia causal sobre el impacto de la nueva landing page."
        )

    info_box(title="Interpretación de la respuesta mayoritaria", body=interpretation)


def display_landing_card(title: str, image_path: str, description: str) -> None:
    """Renderiza una tarjeta visual para una variante de landing page."""
    path = Path(image_path)
    if not path.is_absolute():
        path = APP_DIR / path

    with st.container(border=True):
        st.subheader(title)
        if path.exists():
            try:
                st.image(str(path), use_container_width=True)
            except TypeError:
                st.image(str(path), use_column_width=True)
        else:
            st.warning(f"No se encontró la imagen {image_path}")
        st.caption(description)


st.set_page_config(page_title="Introduccion | A/B Testing", page_icon="📘", layout="wide")
apply_base_styles()
init_db()
session_id = get_or_create_session_id()

page_header(
    title="¿Cambiar o no cambiar una landing page?",
    subtitle="Una primera aproximación al A/B Testing desde una decisión real de marketing.",
)

st.subheader("Planteamiento del caso")
st.write(
    """
    Una empresa lanzó una campaña digital para captar prospectos. Actualmente usa
    una landing page A. El equipo de marketing diseñó una nueva landing page B,
    más moderna y visualmente atractiva. La directora de marketing digital
    considera que la versión B debería reemplazar inmediatamente a la versión A.

    Sin embargo, antes de tomar la decisión, el equipo de analítica propone
    evaluar si la nueva página realmente mejora la conversión.
    """
)

st.subheader("Las dos versiones en comparación")
st.write(
    "Observa ambas versiones antes de responder cómo consideras que debería tomarse la decisión."
)

landing_a_col, landing_b_col = st.columns(2)

with landing_a_col:
    display_landing_card(
        title="Versión A: landing page actual",
        image_path="assets/landing_a.svg",
        description="Esta es la versión que actualmente se utiliza como referencia o control.",
    )

with landing_b_col:
    display_landing_card(
        title="Versión B: nueva landing page",
        image_path="assets/landing_b.svg",
        description="Esta es la nueva propuesta diseñada por el equipo de marketing.",
    )

st.markdown("### **¿Cómo deberíamos decidir si conviene adoptar la nueva landing page?**")

submitted_option = get_session_response(session_id)
has_submitted = submitted_option is not None

if has_submitted:
    st.session_state["selected_option_submitted"] = submitted_option
else:
    st.session_state.pop("selected_option_submitted", None)

if not has_submitted:
    selected_decision = st.radio(
        "Selecciona la alternativa que te parezca más razonable:",
        DECISION_OPTIONS,
        index=None,
    )

    if st.button("Enviar respuesta", type="primary"):
        if selected_decision is None:
            st.warning("Selecciona una opción antes de enviar tu respuesta.")
        else:
            save_response(selected_decision, session_id)
            st.session_state["selected_option_submitted"] = selected_decision
            submitted_option = selected_decision
            has_submitted = True
            st.success("Tu respuesta fue registrada.")
else:
    st.success("Tu respuesta ya fue registrada.")
    selected_decision = st.radio(
        "Selecciona la alternativa que te parezca más razonable:",
        DECISION_OPTIONS,
        index=DECISION_OPTIONS.index(submitted_option) if submitted_option in DECISION_OPTIONS else None,
        disabled=True,
    )

if has_submitted and submitted_option is not None:
    feedback_title, feedback_body = FEEDBACK_BY_OPTION[submitted_option]
    info_box(title=feedback_title, body=feedback_body)

    poll_df = load_poll_data()
    summary_df = summarize_poll(poll_df)

    if not poll_df.empty:
        st.subheader("Resultados acumulados")
        st.metric("Total de respuestas", int(summary_df["frecuencia"].sum()))
        st.dataframe(
            summary_df[["opcion", "frecuencia", "porcentaje_texto"]].rename(
                columns={
                    "opcion": "Opción",
                    "frecuencia": "Frecuencia",
                    "porcentaje_texto": "Porcentaje",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )
        st.plotly_chart(plot_poll_results(summary_df), use_container_width=True)
        render_majority_interpretation(summary_df)


# Sección de herramientas para el docente: reiniciar la encuesta  
# with st.expander("Herramientas para el docente"):
#     st.warning("Reiniciar la encuesta borrará las respuestas actuales.")
#     if st.session_state.pop("intro_poll_reset_done", False):
#         st.success("La encuesta fue reiniciada correctamente.")

#     confirm_reset = st.checkbox("Confirmo que deseo borrar las respuestas de esta encuesta")

#     if st.button("Reiniciar encuesta"):
#         if confirm_reset:
#             reset_poll()
#             st.session_state.pop("selected_option_submitted", None)
#             st.session_state["intro_poll_reset_done"] = True
#             st.rerun()
#         else:
#             st.error("Marca la casilla de confirmación antes de reiniciar la encuesta.")

