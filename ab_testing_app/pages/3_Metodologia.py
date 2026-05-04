import streamlit as st

from src.ui.layout import methodological_note, page_header
from src.ui.styles import apply_base_styles


st.set_page_config(page_title="Metodologia | A/B Testing", page_icon="🧪", layout="wide")
apply_base_styles()

page_header(
    title="Metodología general del A/B Testing",
    subtitle="Del diseño experimental a la decisión basada en evidencia.",
)

st.write(
    """
    Un A/B Test no se reduce a comparar dos porcentajes. Implica definir una
    decisión de marketing, diseñar un experimento controlado, recolectar evidencia
    e interpretar los resultados para apoyar la toma de decisiones.
    """
)

st.subheader("Flujo general de trabajo")
st.write(
    "El proceso puede entenderse en cuatro grandes momentos. Después se detalla "
    "cada fase metodológica."
)

st.markdown(
    """
    <style>
        .ab-flow {
            display: flex;
            flex-direction: column;
            gap: 0.45rem;
            margin: 1rem 0 1.5rem;
        }

        .ab-flow-step {
            display: flex;
            align-items: center;
            gap: 1rem;
            background: #f7fafc;
            border: 1px solid #d7e3ea;
            border-radius: 8px;
            padding: 0.9rem 1rem;
            box-shadow: 0 2px 8px rgba(18, 48, 71, 0.06);
        }

        .ab-flow-number {
            width: 2.35rem;
            height: 2.35rem;
            border-radius: 999px;
            background: #2f6f8f;
            color: #ffffff;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            flex: 0 0 auto;
        }

        .ab-flow-title {
            color: #243746;
            font-weight: 700;
            font-size: 1.02rem;
        }

        .ab-flow-text {
            color: #536471;
            font-size: 0.96rem;
            margin-top: 0.25rem;
        }

        .ab-flow-content {
            display: flex;
            flex-direction: column;
        }

        .ab-flow-arrow {
            color: #6d7b87;
            text-align: center;
            font-size: 1.3rem;
            line-height: 1;
        }
    </style>

    <div class="ab-flow">
        <div class="ab-flow-step">
            <span class="ab-flow-number">1</span>
            <span class="ab-flow-content">
                <span class="ab-flow-title">Preparar la prueba</span>
                <span class="ab-flow-text">Decisión, hipótesis, métrica y diseño experimental.</span>
            </span>
        </div>
        <div class="ab-flow-arrow">↓</div>
        <div class="ab-flow-step">
            <span class="ab-flow-number">2</span>
            <span class="ab-flow-content">
                <span class="ab-flow-title">Ejecutar la prueba</span>
                <span class="ab-flow-text">Asignación de usuarios, exposición a versiones y recolección de datos.</span>
            </span>
        </div>
        <div class="ab-flow-arrow">↓</div>
        <div class="ab-flow-step">
            <span class="ab-flow-number">3</span>
            <span class="ab-flow-content">
                <span class="ab-flow-title">Analizar la evidencia</span>
                <span class="ab-flow-text">Comparación de métricas, incertidumbre y relevancia comercial.</span>
            </span>
        </div>
        <div class="ab-flow-arrow">↓</div>
        <div class="ab-flow-step">
            <span class="ab-flow-number">4</span>
            <span class="ab-flow-content">
                <span class="ab-flow-title">Decidir y aprender</span>
                <span class="ab-flow-text">Decisión final, documentación y aprendizajes para futuras pruebas.</span>
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("Detalle de cada fase")
st.write("Las macroetapas anteriores se concretan en las siguientes fases de trabajo.")

with st.expander("1. Definir la decisión de marketing"):
    st.markdown(
        """
        **Explicación.** Antes de experimentar, se debe definir con claridad qué
        decisión se desea tomar. El A/B Test debe responder a una decisión
        concreta, no a una curiosidad general.

        **Ejemplo aplicado.** Decidir si la landing page B debe reemplazar a la
        landing page A.

        **Pregunta guía.** ¿Qué decisión se tomará al finalizar el experimento?
        """
    )

with st.expander("2. Formular hipótesis y elegir la métrica"):
    st.markdown(
        """
        **Explicación.** La prueba debe vincularse con una hipótesis verificable
        y una métrica principal. En marketing, las métricas pueden ser conversión,
        clics, apertura, compras, ingreso promedio o abandono.

        **Ejemplo aplicado.** Evaluar si la landing page B incrementa la tasa de
        conversión respecto a la landing page A.

        **Pregunta guía.** ¿Qué indicador permitirá decidir si la variante B es
        mejor?
        """
    )

with st.expander("3. Diseñar el experimento"):
    st.markdown(
        """
        **Explicación.** Se define cómo se asignarán los usuarios a cada versión,
        cuántos usuarios se necesitan y durante cuánto tiempo se observará el
        comportamiento. La asignación aleatoria es esencial para que los grupos
        sean comparables.

        **Ejemplo aplicado.** Asignar aleatoriamente a los visitantes para que
        algunos vean la landing page A y otros la landing page B.

        **Advertencia metodológica.** Sin asignación comparable, las diferencias
        observadas pueden deberse a características de los usuarios y no al diseño
        de la página.
        """
    )

with st.expander("4. Ejecutar y recolectar datos"):
    st.markdown(
        """
        **Explicación.** Durante la ejecución, se deben registrar exposiciones,
        conversiones y cualquier información necesaria para interpretar el
        resultado. Es importante no modificar el experimento a mitad del proceso
        sin una razón justificada.

        **Ejemplo aplicado.** Registrar cuántos usuarios visitaron cada versión y
        cuántos completaron el formulario.

        **Advertencia metodológica.** No conviene detener el experimento apenas
        aparece una diferencia favorable; hacerlo puede aumentar el riesgo de
        conclusiones equivocadas.
        """
    )

with st.expander("5. Analizar los resultados"):
    st.markdown(
        """
        **Explicación.** Se comparan las métricas observadas entre los grupos y se
        evalúa si la diferencia es suficientemente clara para apoyar una decisión.
        Esta fase puede incluir intervalos de confianza, valor p o medidas de
        efecto.

        **Ejemplo aplicado.** Comparar la tasa de conversión de A contra la tasa
        de conversión de B.

        **Pregunta guía.** ¿La diferencia observada es suficientemente grande y
        confiable para orientar la decisión?
        """
    )

with st.expander("6. Tomar una decisión"):
    st.markdown(
        """
        **Explicación.** La decisión no debe basarse solo en la significancia
        estadística. También se debe valorar la relevancia comercial, los costos
        de implementación, el impacto esperado y los riesgos.

        **Ejemplo aplicado.** Adoptar B si mejora la conversión de forma
        estadísticamente confiable y comercialmente relevante.

        **Advertencia metodológica.** Un resultado significativo puede ser
        demasiado pequeño para justificar un cambio; un resultado no significativo
        puede requerir más datos o una mejor variante.
        """
    )

with st.expander("7. Documentar y aprender"):
    st.markdown(
        """
        **Explicación.** Cada experimento debe dejar aprendizaje para futuras
        decisiones. Documentar el diseño, los resultados y la decisión tomada
        evita repetir pruebas innecesarias y construye conocimiento acumulativo.

        **Ejemplo aplicado.** Registrar qué se probó, con qué métrica, cuáles
        fueron los resultados y qué decisión tomó el equipo.

        **Pregunta guía.** ¿Qué aprendió la organización aunque la variante B no
        haya ganado?
        """
    )

st.divider()

methodological_note(
    "Idea clave: Un buen A/B Test no empieza con la prueba estadística; empieza "
    "con una decisión de marketing bien formulada, una métrica clara y un diseño "
    "experimental capaz de producir evidencia confiable."
)
