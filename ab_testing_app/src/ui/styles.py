import streamlit as st


def apply_base_styles() -> None:
    """Aplica estilos CSS base para mejorar la presentacion de la app."""
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 2.2rem;
                padding-bottom: 3rem;
                max-width: 1120px;
            }

            h1 {
                color: #123047;
                letter-spacing: 0;
            }

            .page-subtitle {
                color: #536471;
                font-size: 1.08rem;
                margin-top: -0.5rem;
                margin-bottom: 1.5rem;
            }

            .styled-box {
                border-radius: 10px;
                padding: 1rem 1.15rem;
                margin: 1rem 0;
                border: 1.5px solid;
                box-shadow: 0 2px 8px rgba(18, 48, 71, 0.06);
            }

            .styled-box strong {
                display: block;
                font-weight: 800;
                margin-bottom: 0.25rem;
            }

            .styled-box p {
                margin: 0.35rem 0 0;
                color: #243746;
                line-height: 1.55;
            }

            .styled-box-info {
                background: #eaf4ff;
                border-color: #7fb3e6;
            }

            .styled-box-info strong {
                color: #1f4e79;
            }

            .styled-box-method {
                background: #fff4db;
                border-color: #e7c66b;
            }

            .styled-box-method strong {
                color: #8a5a00;
            }

            .styled-box-success {
                background: #eaf8ef;
                border-color: #7bc096;
            }

            .styled-box-success strong {
                color: #1f6b3d;
            }

            .styled-box-warning {
                background: #fff1e6;
                border-color: #f0ad6d;
            }

            .styled-box-warning strong {
                color: #9a4d00;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
