from math import sqrt

from scipy.stats import norm


def conversion_rate(conversions: int, visitors: int) -> float:
    """Calcula la tasa de conversion de un grupo."""
    if visitors <= 0:
        raise ValueError("visitors debe ser mayor que cero.")
    return conversions / visitors


def absolute_difference(rate_treatment: float, rate_control: float) -> float:
    """Calcula la diferencia absoluta entre dos tasas."""
    return rate_treatment - rate_control


def relative_difference(rate_treatment: float, rate_control: float) -> float:
    """Calcula la diferencia relativa contra la tasa de control."""
    if rate_control == 0:
        raise ValueError("rate_control no puede ser cero.")
    return (rate_treatment - rate_control) / rate_control


def two_proportion_z_test(
    conversions_control: int,
    visitors_control: int,
    conversions_treatment: int,
    visitors_treatment: int,
) -> dict[str, float]:
    """Realiza una prueba z bilateral para dos proporciones."""
    if visitors_control <= 0 or visitors_treatment <= 0:
        raise ValueError("Los tamanos de muestra deben ser mayores que cero.")

    rate_control = conversion_rate(conversions_control, visitors_control)
    rate_treatment = conversion_rate(conversions_treatment, visitors_treatment)

    pooled_rate = (conversions_control + conversions_treatment) / (
        visitors_control + visitors_treatment
    )
    standard_error = sqrt(
        pooled_rate
        * (1 - pooled_rate)
        * ((1 / visitors_control) + (1 / visitors_treatment))
    )

    if standard_error == 0:
        raise ValueError("No es posible calcular la prueba z con error estandar cero.")

    z_score = (rate_treatment - rate_control) / standard_error
    p_value = 2 * (1 - norm.cdf(abs(z_score)))

    return {
        "rate_control": rate_control,
        "rate_treatment": rate_treatment,
        "z_score": z_score,
        "p_value": p_value,
    }
