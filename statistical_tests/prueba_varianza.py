import numpy as np
from scipy.stats import chi2

def realizar_prueba_varianza(numeros: list[float], nivel_significancia: float) -> dict:
    """
    Realiza la prueba de varianza para una secuencia de números pseudoaleatorios.
    Se asume que los números provienen de una distribución uniforme U(0,1),
    donde la varianza esperada (sigma^2) es 1/12.

    Args:
        numeros (list[float]): La secuencia de números a probar.
        nivel_significancia (float): El nivel de significancia (alpha), por ejemplo, 0.05.

    Returns:
        dict: Un diccionario con los resultados de la prueba.
    """
    if not (0 < nivel_significancia < 1):
        raise ValueError("El nivel de significancia debe estar entre 0 y 1.")
    if not numeros or len(numeros) < 2:
        raise ValueError("Se requieren al menos 2 números para realizar la prueba de varianza.")

    n = len(numeros)
    varianza_muestral = np.var(numeros, ddof=1) # ddof=1 para varianza muestral insesgada
    sigma_cuadrada_esperada = 1/12 # Varianza de una U(0,1)

    # Calcular el estadístico Chi-cuadrado
    # Chi^2 = (n-1) * varianza_muestral / sigma_cuadrada_esperada
    try:
        estadistico_chi2 = (n - 1) * varianza_muestral / sigma_cuadrada_esperada
    except ZeroDivisionError:
        return {
            "error": "Error de división por cero. La varianza esperada no puede ser cero."
        }

    grados_libertad = n - 1

    # Calcular los valores críticos Chi-cuadrado para una prueba bilateral
    # alpha/2 para cada cola
    valor_critico_inferior = chi2.ppf(nivel_significancia / 2, grados_libertad)
    valor_critico_superior = chi2.ppf(1 - nivel_significancia / 2, grados_libertad)

    # Calcular el p-valor
    p_valor = 2 * min(chi2.cdf(estadistico_chi2, grados_libertad), 1 - chi2.cdf(estadistico_chi2, grados_libertad))

    # Conclusión
    conclusion = ""
    if valor_critico_inferior < estadistico_chi2 < valor_critico_superior:
        conclusion = f"No se rechaza la hipótesis nula (H0). La varianza muestral ({varianza_muestral:.6f}) no es significativamente diferente de la varianza esperada ({sigma_cuadrada_esperada:.6f})."
    else:
        conclusion = f"Se rechaza la hipótesis nula (H0). La varianza muestral ({varianza_muestral:.6f}) es significativamente diferente de la varianza esperada ({sigma_cuadrada_esperada:.6f})."

    return {
        "prueba": "Prueba de Varianza",
        "n": n,
        "varianza_muestral": varianza_muestral,
        "sigma_cuadrada_esperada": sigma_cuadrada_esperada,
        "nivel_significancia": nivel_significancia,
        "estadistico_chi2": estadistico_chi2,
        "grados_libertad": grados_libertad,
        "valor_critico_inferior": valor_critico_inferior,
        "valor_critico_superior": valor_critico_superior,
        "p_valor": p_valor,
        "conclusion": conclusion
    }
