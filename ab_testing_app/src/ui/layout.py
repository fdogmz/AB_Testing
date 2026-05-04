from html import escape

import streamlit as st


def page_header(title: str, subtitle: str | None = None) -> None:
    """Renderiza un encabezado consistente para cada pagina."""
    st.title(title)
    if subtitle:
        st.markdown(f"<p class='page-subtitle'>{subtitle}</p>", unsafe_allow_html=True)


def styled_box(title: str, body: str, kind: str = "info") -> None:
    """Renderiza una caja de contenido con variantes visuales reutilizables."""
    st.markdown(
        f"""
        <div class="styled-box styled-box-{escape(kind)}">
            <strong>{escape(title)}</strong>
            <p>{escape(body)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_box(title: str, body: str, kind: str = "info") -> None:
    """Renderiza una caja informativa reutilizable."""
    styled_box(title=title, body=body, kind=kind)


def methodological_note(
    body: str,
    title: str = "Nota metodologica",
    kind: str = "method",
) -> None:
    """Renderiza una nota metodologica o advertencia breve."""
    styled_box(title=title, body=body, kind=kind)
