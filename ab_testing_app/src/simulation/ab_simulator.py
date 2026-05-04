import numpy as np


def simulate_ab_conversions(
    n_control: int,
    p_control: float,
    n_treatment: int,
    p_treatment: float,
    random_state: int | None = None,
) -> dict[str, int]:
    """Simula conversiones binomiales para grupos control y tratamiento."""
    rng = np.random.default_rng(random_state)

    conversions_control = rng.binomial(n=n_control, p=p_control)
    conversions_treatment = rng.binomial(n=n_treatment, p=p_treatment)

    return {
        "n_control": n_control,
        "conversions_control": int(conversions_control),
        "n_treatment": n_treatment,
        "conversions_treatment": int(conversions_treatment),
    }
