import math

def generar_productos_medios(semilla1: int, semilla2: int, cantidad: int, devolver_pasos: bool = False) -> tuple[list[float], list[dict]] | list[float]:
    """
    Genera una secuencia de números pseudoaleatorios utilizando el método de Productos Medios.

    Args:
        semilla1 (int): La primera semilla inicial (X_i-1).
        semilla2 (int): La segunda semilla inicial (X_i).
        cantidad (int): La cantidad de números a generar.
        devolver_pasos (bool): Si es True, devuelve también una lista con los pasos intermedios.

    Returns:
        list[float]: Una lista de números pseudoaleatorios entre 0 y 1.
        o
        tuple[list[float], list[dict]]: Lista de números y lista de diccionarios con los pasos.
    """
    if not isinstance(semilla1, int) or semilla1 < 0:
        raise ValueError("La semilla1 debe ser un entero no negativo.")
    if not isinstance(semilla2, int) or semilla2 < 0:
        raise ValueError("La semilla2 debe ser un entero no negativo.")
    if not isinstance(cantidad, int) or cantidad <= 0:
        raise ValueError("La cantidad debe ser un entero positivo.")

    numeros_generados = []
    pasos = []

    # Reordenamiento inicial para que X_i-1 sea semilla1 y X_i sea semilla2
    x_n_menos_1 = semilla1
    x_n = semilla2

    # D es el número de dígitos de la semilla más grande, fijo para todo el proceso
    d = max(len(str(semilla1)), len(str(semilla2)))

    for i in range(cantidad):
        producto = x_n * x_n_menos_1
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
                "Xi": (x_n_menos_1, x_n), # Guardar (X_i-1, X_i) para el paso
                "Yi": producto,
                "mid": x_n_mas_1_str, # El segmento central extraído, ya rellenado a D dígitos
                "X_next": x_n_mas_1,
                "ri": r_n
            })

        # Actualizar para la siguiente iteración
        x_n_menos_1 = x_n
        x_n = x_n_mas_1

        if x_n == 0 or x_n_menos_1 == 0: # Si alguna semilla se vuelve 0, el generador se estanca
            # Si se estanca, los números siguientes serán 0.0
            if devolver_pasos:
                for j in range(i + 1, cantidad):
                    pasos.append({
                        "i": j,
                        "Xi": (x_n_menos_1, x_n),
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
