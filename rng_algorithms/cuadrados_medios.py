import math

def generar_cuadrados_medios(semilla: int, cantidad: int, devolver_pasos: bool = False) -> tuple[list[float], list[dict]] | list[float]:
    """
    Genera una secuencia de números pseudoaleatorios utilizando el método de Cuadrados Medios.

    Args:
        semilla (int): La semilla inicial (debe ser un número par de dígitos).
        cantidad (int): La cantidad de números a generar.
        devolver_pasos (bool): Si es True, devuelve también una lista con los pasos intermedios.

    Returns:
        list[float]: Una lista de números pseudoaleatorios entre 0 y 1.
        o
        tuple[list[float], list[dict]]: Lista de números y lista de diccionarios con los pasos.
    """
    if not isinstance(semilla, int) or semilla < 0:
        raise ValueError("La semilla debe ser un entero no negativo.")
    if not isinstance(cantidad, int) or cantidad <= 0:
        raise ValueError("La cantidad debe ser un entero positivo.")

    numeros_generados = []
    pasos = []
    x_n = semilla
    d = len(str(semilla)) # Número de dígitos de la semilla, fijo para todo el proceso

    if d % 2 != 0:
        raise ValueError("La semilla para Cuadrados Medios debe tener un número par de dígitos.")

    for i in range(cantidad):
        x_n_cuadrado = x_n * x_n
        str_x_n_cuadrado = str(x_n_cuadrado)
        
        # Longitud real del número cuadrado
        len_cuadrado = len(str_x_n_cuadrado)

        # Calcular inicio y fin para extraer D dígitos centrales
        # Si len_cuadrado es 2*d-1, (len_cuadrado - d) // 2 será diferente a si fuera 2*d
        inicio = (len_cuadrado - d) // 2
        fin = inicio + d
        
        # Asegurarse de que la extracción no exceda los límites y que siempre se obtengan D dígitos
        # Si el número cuadrado es muy pequeño, puede que no haya suficientes dígitos para extraer D
        if fin > len_cuadrado:
            # Esto ocurre si el número cuadrado es demasiado pequeño (ej. 0)
            x_n_str = "0" * d
        else:
            x_n_str = str_x_n_cuadrado[inicio:fin]
            # Rellenar con ceros a la izquierda si el segmento extraído tiene menos de D dígitos
            # Esto puede ocurrir si el segmento extraído empieza con ceros, y str() los omite
            x_n_str = x_n_str.zfill(d)

        x_next = int(x_n_str)

        r_n = x_next / (10**d)
        numeros_generados.append(r_n)

        if devolver_pasos:
            pasos.append({
                "i": i,
                "Xi": x_n,
                "Yi": x_n_cuadrado,
                "mid": x_n_str, # El segmento central extraído, ya rellenado a D dígitos
                "X_next": x_next,
                "ri": r_n
            })

        x_n = x_next

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
