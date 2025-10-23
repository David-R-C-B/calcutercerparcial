import numpy as np
from scipy.stats import norm

def realizar_prueba_medias(numeros: list[float], nivel_significancia: float) -> dict:
    """
    Realiza la prueba de medias para una secuencia de números pseudoaleatorios.
    Se asume que los números provienen de una distribución uniforme U(0,1),
    donde la media esperada (mu) es 0.5 y la varianza (sigma^2) es 1/12.

    Args:
        numeros (list[float]): La secuencia de números a probar.
        nivel_significancia (float): El nivel de significancia (alpha), por ejemplo, 0.05.

    Returns:
        dict: Un diccionario con los resultados de la prueba.
    """
    if not (0 < nivel_significancia < 1):
        raise ValueError("El nivel de significancia debe estar entre 0 y 1.")
    if not numeros or len(numeros) < 30: # Se recomienda n >= 30 para prueba Z
        raise ValueError("Se requieren al menos 30 números para realizar la prueba de medias.")

    n = len(numeros)
    media_muestral = np.mean(numeros)
    mu_esperada = 0.5
    # Varianza de una U(0,1) es (b-a)^2 / 12 = (1-0)^2 / 12 = 1/12
    sigma_cuadrada_esperada = 1/12
    sigma_esperada = np.sqrt(sigma_cuadrada_esperada)

    # Calcular el estadístico Z
    # Z = (media_muestral - mu_esperada) / (sigma_esperada / sqrt(n))
    try:
        estadistico_z = (media_muestral - mu_esperada) / (sigma_esperada / np.sqrt(n))
    except ZeroDivisionError:
        return {
            "error": "Error de división por cero. Asegúrate de que la cantidad de números sea suficiente."
        }

    # Calcular el valor crítico Z para una prueba bilateral
    # alpha/2 para cada cola
    valor_critico_z = norm.ppf(1 - nivel_significancia / 2)

    # Calcular el p-valor
    p_valor = 2 * (1 - norm.cdf(abs(estadistico_z)))

    # Conclusión
    conclusion = ""
    if abs(estadistico_z) < valor_critico_z:
        conclusion = f"No se rechaza la hipótesis nula (H0). La media muestral ({media_muestral:.4f}) no es significativamente diferente de la media esperada ({mu_esperada})."
    else:
        conclusion = f"Se rechaza la hipótesis nula (H0). La media muestral ({media_muestral:.4f}) es significativamente diferente de la media esperada ({mu_esperada})."

    return {
        "prueba": "Prueba de Medias",
        "n": n,
        "media_muestral": media_muestral,
        "mu_esperada": mu_esperada,
        "nivel_significancia": nivel_significancia,
        "estadistico_z": estadistico_z,
        "valor_critico_z": valor_critico_z,
        "p_valor": p_valor,
        "conclusion": conclusion
    }