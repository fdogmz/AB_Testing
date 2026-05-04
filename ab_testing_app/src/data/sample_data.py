import pandas as pd


def load_sample_ab_test_data() -> pd.DataFrame:
    """Genera un DataFrame pequeno para un caso ficticio de A/B Test."""
    return pd.DataFrame(
        {
            "group": ["Control", "Tratamiento"],
            "visitors": [1200, 1180],
            "conversions": [96, 118],
            "conversion_rate": [0.080, 0.100],
        }
    )
