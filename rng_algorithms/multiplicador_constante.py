import math

def generar_multiplicador_constante(semilla: int, constante: int, cantidad: int, devolver_pasos: bool = False) -> tuple[list[float], list[dict]] | list[float]:
    """
    Genera una secuencia de números pseudoaleatorios utilizando el método del Multiplicador Constante.

    Args:
        semilla (int): La semilla inicial.
        constante (int): La constante multiplicadora.
        cantidad (int): La cantidad de números a generar.
        devolver_pasos (bool): Si es True, devuelve también una lista con los pasos intermedios.

    Returns:
        list[float]: Una lista de números pseudoaleatorios entre 0 y 1.
        o
        tuple[list[float], list[dict]]: Lista de números y lista de diccionarios con los pasos.
    """
    if not isinstance(semilla, int) or semilla < 0:
        raise ValueError("La semilla debe ser un entero no negativo.")
    if not isinstance(constante, int) or constante < 0:
        raise ValueError("La constante debe ser un entero no negativo.")
    if not isinstance(cantidad, int) or cantidad <= 0:
        raise ValueError("La cantidad debe ser un entero positivo.")

    numeros_generados = []
    pasos = []
    x_n = semilla
    d = len(str(semilla)) # Número de dígitos de la semilla, fijo para todo el proceso

    for i in range(cantidad):
        producto = constante * x_n
        str_producto = str(producto)
        
        # Longitud real del número producto
        len_producto = len(str_producto)

        # Calcular inicio y fin para extraer D dígitos centrales
        inicio = (len_producto - d) // 2
        fin = inicio + d
        
        # Asegurarse de que la extracción no exceda los límites y que siempre se obtengan D dígitos
        if fin > len_producto:
            x_n_mas_1_str = "0" * d
        else:
            x_n_mas_1_str = str_producto[inicio:fin]
            # Rellenar con ceros a la izquierda si el segmento extraído tiene menos de D dígitos
            x_n_mas_1_str = x_n_mas_1_str.zfill(d)

        x_n_mas_1 = int(x_n_mas_1_str)

        r_n = x_n_mas_1 / (10**d)
        numeros_generados.append(r_n)

        if devolver_pasos:
            pasos.append({
                "i": i,
                "Xi": x_n,
                "Yi": producto,
                "mid": x_n_mas_1_str, # El segmento central extraído, ya rellenado a D dígitos
                "X_next": x_n_mas_1,
                "ri": r_n
            })

        x_n = x_n_mas_1

        if x_n == 0: # Si la semilla se vuelve 0, el generador se estanca
            # Si se estanca, los números siguientes serán 0.0
            if devolver_pasos:
                for j in range(i + 1, cantidad):
                    pasos.append({
                        "i": j,
                        "Xi": 0,
                        "Yi": 0,
                        "mid": "0" * d,
                        "X_next": 0,
                        "ri": 0.0
                    })
            numeros_generados.extend([0.0] * (cantidad - len(numeros_generados)))
            break

    if devolver_pasos:
        return numeros_generados, pasos
    return numeros_generados
