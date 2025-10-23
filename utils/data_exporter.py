import pandas as pd
import os

def exportar_a_csv(datos: list[float], nombre_archivo: str):
    """
    Exporta una lista de números a un archivo CSV.

    Args:
        datos (list[float]): La lista de números a exportar.
        nombre_archivo (str): El nombre del archivo CSV (sin extensión).
    """
    df = pd.DataFrame({"Numero_Generado": datos})
    ruta_completa = f"{nombre_archivo}.csv"
    df.to_csv(ruta_completa, index=False)
    return ruta_completa