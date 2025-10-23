## 📘 BASE DE CONOCIMIENTO DE LA CALCULADORA (v2)

### 🧩 Sección 1: Algoritmos de generación de números pseudoaleatorios

---

#### 🔢 1.1. Algoritmo de los **Cuadrados Medios**

**Nombre:** Método de los Cuadrados Medios (Mid-Square Method)
**Tipo:** Generador de números pseudoaleatorios determinístico
**Propósito:** Generar secuencias de números en el intervalo (0, 1) a partir de una semilla inicial.
**Autor original:** John von Neumann (1949)

---

### 📘 Descripción general

El método de los cuadrados medios se basa en **elevar la semilla al cuadrado** y luego **extraer los dígitos centrales** del resultado para formar el siguiente número.
Cada número generado depende completamente del anterior, lo que lo hace **determinístico y reproducible**.

---

### ⚙️ Parámetros

| Parámetro | Descripción                                    |
| --------- | ---------------------------------------------- |
| `X0`      | Semilla inicial con `D` dígitos (`D > 3`)      |
| `D`       | Número de dígitos de la semilla                |
| `Xi`      | Valor actual                                   |
| `Yi`      | Cuadrado del valor actual (`Xi²`)              |
| `ri`      | Número pseudoaleatorio resultante entre (0, 1) |

---

### 🧮 Pasos del algoritmo

1. Seleccionar la semilla inicial (`X₀`) con `D` dígitos (`D > 3`).
2. Elevar la semilla al cuadrado:
   `Y₀ = X₀²`
3. Extraer los `D` dígitos centrales del resultado → `X₁`.
4. Normalizar:
   **Fórmula:** `r₁ = X₁ / 10ᴰ`
5. Repetir el proceso:
   `Yᵢ = Xᵢ² → Xᵢ₊₁ = mid(Yᵢ, D) → rᵢ = 0.Xᵢ₊₁`

---

### 🔁 Ciclo de generación

* `Xᵢ₊₁ = mid(Xᵢ², D)`
* `rᵢ = Xᵢ / 10ᴰ`

---

### 🧠 Ejemplo paso a paso

| Iteración | Xᵢ   | Yᵢ = Xᵢ² | Dígitos centrales | Xᵢ₊₁ | rᵢ = 0.Xᵢ₊₁ |
| --------- | ---- | -------- | ----------------- | ---- | ----------- |
| 0         | 5735 | 32890225 | 8902              | 8902 | 0.8902      |
| 1         | 8902 | 79245604 | 2456              | 2456 | 0.2456      |
| 2         | 2456 | 6031936  | 0319              | 319  | 0.0319      |

---

### 🧰 Pseudocódigo

```python
def cuadrados_medios(semilla: int, D: int, n: int):
    resultados = []
    X = semilla
    for _ in range(n):
        Y = X ** 2
        Y_str = str(Y).zfill(2 * D)
        inicio = (len(Y_str) - D) // 2
        X = int(Y_str[inicio:inicio + D])
        r = X / (10 ** D)
        resultados.append(r)
    return resultados
```

---

---

#### 🔢 1.2. Algoritmo de los **Productos Medios**

**Nombre:** Método de los Productos Medios (Middle Product Method)
**Tipo:** Generador de números pseudoaleatorios determinístico
**Propósito:** Generar números pseudoaleatorios a partir del producto de dos semillas sucesivas.

---

### 📘 Descripción general

El método de los productos medios parte de **dos semillas iniciales**, `X₀` y `X₁`, ambas con `D` dígitos.
Cada nuevo número se obtiene multiplicando las dos semillas anteriores y extrayendo los **dígitos centrales** del resultado.
Este método fue diseñado para evitar los ciclos cortos del método de cuadrados medios.

---

### ⚙️ Parámetros

| Parámetro | Descripción                                       |
| --------- | ------------------------------------------------- |
| `X₀`      | Primera semilla inicial con `D` dígitos (`D > 3`) |
| `X₁`      | Segunda semilla inicial con `D` dígitos (`D > 3`) |
| `D`       | Cantidad de dígitos a conservar                   |
| `Yᵢ`      | Producto entre las dos semillas más recientes     |
| `rᵢ`      | Número pseudoaleatorio entre (0, 1)               |

---

### 🧮 Pasos del algoritmo

1. Seleccionar una semilla `X₀` con `D` dígitos (`D > 3`).
2. Seleccionar una segunda semilla `X₁` con `D` dígitos (`D > 3`).
3. Calcular el primer producto:
   `Y₀ = X₀ * X₁`
   Extraer los `D` dígitos centrales → `X₂`, y formar: `r₀ = 0.X₂`
4. Calcular el siguiente producto:
   `Y₁ = X₁ * X₂`
   Extraer los `D` dígitos centrales → `X₃`, y formar: `r₁ = 0.X₃`
5. Repetir el proceso para los siguientes valores.

---

### 🔁 Ciclo de generación

* `Yᵢ = Xᵢ * Xᵢ₋₁`
* `Xᵢ₊₁ = mid(Yᵢ, D)`
* `rᵢ = 0.Xᵢ₊₁`

---

### 🧠 Ejemplo paso a paso

| Iteración | Xᵢ₋₁ | Xᵢ   | Yᵢ = Xᵢ₋₁ * Xᵢ | Dígitos centrales | Xᵢ₊₁ | rᵢ = 0.Xᵢ₊₁ |
| --------- | ---- | ---- | -------------- | ----------------- | ---- | ----------- |
| 0         | 5735 | 2461 | 14113435       | 1134              | 1134 | 0.1134      |
| 1         | 2461 | 1134 | 2798574        | 9857              | 9857 | 0.9857      |
| 2         | 1134 | 9857 | 11181238       | 1812              | 1812 | 0.1812      |

---

### 🧰 Pseudocódigo

```python
def productos_medios(x0: int, x1: int, D: int, n: int):
    resultados = []
    Xi_minus_1, Xi = x0, x1
    for _ in range(n):
        Y = Xi_minus_1 * Xi
        Y_str = str(Y).zfill(2 * D)
        inicio = (len(Y_str) - D) // 2
        Xi_plus_1 = int(Y_str[inicio:inicio + D])
        r = Xi_plus_1 / (10 ** D)
        resultados.append(r)
        Xi_minus_1, Xi = Xi, Xi_plus_1
    return resultados
```

---

---

#### 🔢 1.3. Algoritmo del **Multiplicador Constante**

**Nombre:** Método del Multiplicador Constante (Constant Multiplier Method)
**Tipo:** Generador pseudoaleatorio determinístico
**Propósito:** Generar secuencias pseudoaleatorias usando una constante multiplicadora fija.

---

### 📘 Descripción general

Este método utiliza una **semilla inicial (`X₀`)** y una **constante multiplicadora (`a`)**.
En cada iteración se multiplica la semilla por la constante, se extraen los **dígitos centrales** del resultado, y se normaliza para obtener el número pseudoaleatorio.

---

### ⚙️ Parámetros

| Parámetro | Descripción                                        |
| --------- | -------------------------------------------------- |
| `X₀`      | Semilla inicial con `D` dígitos (`D > 3`)          |
| `a`       | Constante multiplicadora con `D` dígitos (`D > 3`) |
| `D`       | Cantidad de dígitos a conservar                    |
| `Yᵢ`      | Resultado de la multiplicación `a * Xᵢ`            |
| `rᵢ`      | Número pseudoaleatorio normalizado                 |

---

### 🧮 Pasos del algoritmo

1. Seleccionar una **semilla (`X₀`)** con `D` dígitos (`D > 3`).
2. Seleccionar una **constante multiplicadora (`a`)** con `D` dígitos (`D > 3`).
3. Calcular:
   `Y₀ = a * X₀`
   Extraer los `D` dígitos centrales → `X₁`
   Formar: `r₀ = 0.X₁`
4. Calcular el siguiente valor:
   `Y₁ = a * X₁`
   Extraer los `D` dígitos centrales → `X₂`
   Formar: `r₁ = 0.X₂`
5. Repetir los pasos para generar la secuencia deseada.

---

### 🔁 Ciclo de generación

* `Yᵢ = a * Xᵢ`
* `Xᵢ₊₁ = mid(Yᵢ, D)`
* `rᵢ = 0.Xᵢ₊₁`

---

### 🧠 Ejemplo paso a paso

| Iteración | Xᵢ   | Yᵢ = a * Xᵢ        | Dígitos centrales | Xᵢ₊₁ | rᵢ = 0.Xᵢ₊₁ |
| --------- | ---- | ------------------ | ----------------- | ---- | ----------- |
| 0         | 5735 | 2461×5735=14109535 | 1095              | 1095 | 0.1095      |
| 1         | 1095 | 2461×1095=2698395  | 6983              | 6983 | 0.6983      |
| 2         | 6983 | 2461×6983=17179763 | 1797              | 1797 | 0.1797      |

---

### 🧰 Pseudocódigo

```python
def multiplicador_constante(semilla: int, a: int, D: int, n: int):
    resultados = []
    X = semilla
    for _ in range(n):
        Y = a * X
        Y_str = str(Y).zfill(2 * D)
        inicio = (len(Y_str) - D) // 2
        X = int(Y_str[inicio:inicio + D])
        r = X / (10 ** D)
        resultados.append(r)
    return resultados
```

---

### 📈 Aplicación práctica en la calculadora

En la interfaz gráfica, el usuario podrá:

* Seleccionar el método deseado: **Cuadrados Medios**, **Productos Medios** o **Multiplicador Constante**.
* Ingresar los parámetros correspondientes (`semillas`, `constante`, `D`, `n`).
* Visualizar los resultados numéricos y gráficos.
* Exportar los datos a **CSV/Excel** o copiarlos al portapapeles.

---

## 🧪 Sección 2: Pruebas estadísticas para números pseudoaleatorios

> Supuesto base: los números `U₁, U₂, …, Uₙ` provienen de una **Uniforme(0, 1)** i.i.d.
> Bajo este supuesto:
> • `E[U] = μ₀ = 0.5`
> • `Var(U) = σ₀² = 1/12`

---

### 🧪 2.1 Prueba de **Medias** (Uniforme 0-1)

**Objetivo:** comprobar si la **media muestral** es consistente con `μ₀ = 0.5`.

**Hipótesis (bilateral):**

* H₀: μ = 0.5
* H₁: μ ≠ 0.5

**Estadístico (CLT):**

* Media muestral: `Ū = (1/n) Σ Uᵢ`
* Estadístico Z: `Z = √(12 · n) · (Ū − 0.5)`

Bajo H₀ y para n moderado, Z ≈ N(0, 1).

**Regla de decisión (nivel α, bilateral):**
Rechazar H₀ si `|Z| > z_(α/2)`
Valores típicos: `z₀.₀₂₅ = 1.96`, `z₀.₀₀₅ = 2.576`.

**Pasos:**

1. Elegir α (p.ej. 0.05).
2. Calcular `Ū` y `Z = √(12 · n) · (Ū − 0.5)`.
3. Obtener `z_(α/2)` y comparar `|Z|` vs `z_(α/2)`.
4. Concluir: Aceptar/Rechazar H₀.
5. (Opcional) p-valor: `p = 2 · (1 − Φ(|Z|))`.

**Pseudocódigo (Python):**

```python
import numpy as np
from math import sqrt
try:
    from scipy.stats import norm
    _has_scipy = True
except Exception:
    _has_scipy = False

def prueba_medias(u: np.ndarray, alpha: float = 0.05):
    n = len(u)
    ubar = float(np.mean(u))
    Z = sqrt(12 * n) * (ubar - 0.5)

    if _has_scipy:
        zcrit = norm.ppf(1 - alpha/2)
        pval = 2 * (1 - norm.cdf(abs(Z)))
    else:
        crits = {0.10: 1.645, 0.05: 1.96, 0.01: 2.576}
        zcrit = crits.get(alpha, 1.96)
        pval = None

    rechaza = abs(Z) > zcrit
    return {
        "media_muestral": ubar,
        "Z": Z,
        "z_critico": zcrit,
        "alpha": alpha,
        "rechaza_H0": rechaza,
        "pvalor": pval
    }
```

**Salida esperada (GUI/Reporte):**
• Media muestral `Ū`
• `Z`, `z_(α/2)`, decisión (Aceptar/Rechazar H₀)
• p-valor (si disponible)
• Gráfico: histograma de U y línea en 0.5 (opcional)

---

### 🧪 2.2 Prueba de **Varianza** (Uniforme 0-1)

**Objetivo:** verificar si la **varianza muestral** coincide con `σ₀² = 1/12`.

**Hipótesis (bilateral):**

* H₀: σ² = 1/12
* H₁: σ² ≠ 1/12

**Estadístico:**

* Varianza muestral: `S² = (1/(n−1)) · Σ (Uᵢ − Ū)²`
* Chi-cuadrado: `χ² = 12 · (n−1) · S²`
  (Bajo H₀, χ² ≈ χ²₍ₙ₋₁₎)

**Regla de decisión (nivel α):**
Calcular críticos:

* `χ²_L = χ²_(α/2, n−1)`
* `χ²_U = χ²_(1−α/2, n−1)`
  Rechazar H₀ si `χ² < χ²_L` o `χ² > χ²_U`.

**Pasos:**

1. Elegir α (p.ej. 0.05).
2. Calcular `S²` y `χ² = 12 · (n−1) · S²`.
3. Obtener `χ²_L`, `χ²_U` (grados de libertad ν = n−1).
4. Decidir: si χ² ∉ [χ²_L, χ²_U] ⇒ Rechazar H₀.
5. (Opcional) Calcular p-valor bilateral.

**Pseudocódigo (Python):**

```python
import numpy as np
try:
    from scipy.stats import chi2
    _has_scipy_chi2 = True
except Exception:
    _has_scipy_chi2 = False

def prueba_varianza(u: np.ndarray, alpha: float = 0.05):
    n = len(u)
    s2 = float(np.var(u, ddof=1))
    chi2_stat = 12 * (n - 1) * s2

    if _has_scipy_chi2:
        dof = n - 1
        chi2_L = chi2.ppf(alpha/2, dof)
        chi2_U = chi2.ppf(1 - alpha/2, dof)
        from math import isfinite
        cdf = chi2.cdf(chi2_stat, dof)
        pval = 2 * min(cdf, 1 - cdf)
        pval = max(0.0, min(1.0, pval)) if isfinite(pval) else None
    else:
        chi2_L = None
        chi2_U = None
        pval = None

    rechaza = (chi2_L is not None and chi2_stat < chi2_L) or \
              (chi2_U is not None and chi2_stat > chi2_U)

    return {
        "varianza_muestral": s2,
        "chi2": chi2_stat,
        "chi2_L": chi2_L,
        "chi2_U": chi2_U,
        "alpha": alpha,
        "gl": n - 1,
        "rechaza_H0": rechaza if (chi2_L is not None) else None,
        "pvalor": pval
    }
```

**Salida esperada (GUI/Reporte):**
• Varianza muestral `S²`
• `χ²`, `χ²_L`, `χ²_U`, decisión (Aceptar/Rechazar H₀)
• p-valor (si disponible)
• Gráfico: histograma de U con curva teórica opcional.

---

### 🖥️ Integración en la GUI (requerimientos del curso)

**Pestaña “Pruebas”**

* Entradas: `n`, `α`
* Botones: **Probar Medias**, **Probar Varianza**, **Exportar**
* Salidas: Estadísticos, críticos, decisión, p-valor, gráficos
* Exportación: CSV/Excel y reporte txt/md
* Menú principal: “Generar”, “Pruebas”, “Variables”, “Exportar”

**Cumplimiento:**

* Python 3.10+ con `tkinter`, `numpy`, `matplotlib`
* Resultados numéricos y gráficos
* Código propio documentado
* Operación offline para examen
* Incluye estas pruebas estadísticas (30 % de nota)

---

### ✅ Buenas prácticas y notas

* Para muestras chicas puede usarse t-test en media (backup).
* Registrar versión de Python y dependencias en `requirements.txt`.
* Guardar α, n, resultados y decisiones en JSON de sesión.

---

### 🧪 Sección 2: Pruebas estadísticas para números pseudoaleatorios

>Supuesto base: los números U₁, U₂, …, Uₙ provienen de una Uniforme(0, 1) i.i.d.
>
>Bajo este supuesto:
>* E[U] = μ₀ = 0.5
>* Var(U) = σ₀² = 1/12

---

#### 🧪 2.1 Prueba de **Medias** (Uniforme(0,1))

**Objetivo:** comprobar si la **media muestral** es consistente con ( \mu_0 = 0.5 ).

**Hipótesis (bilateral típica):**

* H₀: μ = 0.5
* H₁: μ ≠ 0.5

**Estadístico (basado en CLT):**

Media muestral: `Ū = (1/n) Σ Uᵢ`

Estadístico Z: `Z = √(12 · n) · (Ū − 0.5)`

Bajo H₀ y para n moderado, Z ≈ N(0, 1).

**Regla de decisión (nivel α, bilateral):**

Rechazar H₀ si `|Z| > z_(α/2)`

Valores típicos: `z₀.₀₂₅ = 1.96`, `z₀.₀₀₅ = 2.576`.

**Pasos:**

1. Elegir α (p.ej. 0.05).

2. Calcular `Ū`  y `Z = √(12 · n) · (Ū − 0.5)`.

3. Obtener `z_(α/2)` y comparar `|Z|` vs `z_(α/2)`.

4. Concluir: Aceptar/Rechazar H₀.

5. (Opcional) p-valor: `p = 2 · (1 − Φ(|Z|))`.

**Pseudocódigo (Python):**

```python
import numpy as np
from math import sqrt
try:
    from scipy.stats import norm
    _has_scipy = True
except Exception:
    _has_scipy = False

def prueba_medias(u: np.ndarray, alpha: float = 0.05):
    n = len(u)
    ubar = float(np.mean(u))
    Z = sqrt(12 * n) * (ubar - 0.5)

    if _has_scipy:
        zcrit = norm.ppf(1 - alpha/2)
        pval = 2 * (1 - norm.cdf(abs(Z)))
    else:
        # Tabla mínima para uso común:
        crits = {0.10: 1.645, 0.05: 1.96, 0.01: 2.576}
        zcrit = crits.get(alpha, 1.96)
        pval = None  # sin SciPy, p-valor no exacto

    rechaza = abs(Z) > zcrit
    return {
        "media_muestral": ubar,
        "Z": Z,
        "z_critico": zcrit,
        "alpha": alpha,
        "rechaza_H0": rechaza,
        "pvalor": pval
    }
```

**Salida esperada (GUI/Reporte):**

* Media muestral `Ū`
* `Z`, `z_(α/2)`, decisión (Aceptar/Rechazar H₀)
* p-valor (si disponible)
* **Gráfico**: histograma de (U) y línea vertical en 0.5 (opcional)

---

#### 🧪 2.2 Prueba de **Varianza** (Uniforme(0,1))

**Objetivo:** verificar si la varianza muestral coincide con `σ₀² = 1/12`.

**Hipótesis (bilateral):**

* `H₀: σ² = 1/12`

* `H₁: σ² ≠ 1/12`

**Estadístico:**
* Varianza muestral: `S² = (1/(n−1)) · Σ (Uᵢ − Ū)²`

* Chi-cuadrado: `χ² = 12 · (n−1) · S²`

(Bajo H₀, χ² ≈ χ²₍ₙ₋₁₎)

**Regla de decisión (nivel α, bilateral):**
Calcular los **críticos**:

* `χ²_L = χ²_(α/2, n−1)`

* `χ²_U = χ²_(1−α/2, n−1)`
Rechazar H₀ si `χ² < χ²_L` o `χ² > χ²_U`.

**Pasos:**

1. Elegir α (p. ej., 0.05).
2. Calcular `S²` y `χ² = 12 · (n−1) · S²`.
3. Obtener `χ²_L`, `χ²_U` (grados de libertad ν = n−1).
4. Decidir: si χ² ∉ [χ²_L, χ²_U] ⇒ Rechazar H₀.
5. (Opcional) Calcular p-valor bilateral.

**Pseudocódigo (Python):**

```python
import numpy as np
try:
    from scipy.stats import chi2
    _has_scipy_chi2 = True
except Exception:
    _has_scipy_chi2 = False

def prueba_varianza(u: np.ndarray, alpha: float = 0.05):
    n = len(u)
    s2 = float(np.var(u, ddof=1))
    chi2_stat = 12 * (n - 1) * s2  # (n-1)S^2 / (1/12)

    if _has_scipy_chi2:
        dof = n - 1
        chi2_L = chi2.ppf(alpha/2, dof)
        chi2_U = chi2.ppf(1 - alpha/2, dof)
        # p-valor bilateral:
        from math import isfinite
        cdf = chi2.cdf(chi2_stat, dof)
        # p bilateral: 2*min(CDF, 1-CDF) (acotado en [0,1])
        pval = 2 * min(cdf, 1 - cdf)
        pval = max(0.0, min(1.0, pval)) if isfinite(pval) else None
    else:
        # Sin SciPy no hay cuantiles generales de chi-cuadrado
        chi2_L = None
        chi2_U = None
        pval = None

    rechaza = (chi2_L is not None and chi2_stat < chi2_L) or \
              (chi2_U is not None and chi2_stat > chi2_U)

    return {
        "varianza_muestral": s2,
        "chi2": chi2_stat,
        "chi2_L": chi2_L,
        "chi2_U": chi2_U,
        "alpha": alpha,
        "gl": n - 1,
        "rechaza_H0": rechaza if (chi2_L is not None) else None,
        "pvalor": pval
    }
```

**Salida esperada (GUI/Reporte):**

* Varianza muestral `S²`
* `χ²`, `χ²_L`, `χ²_U`, decisión (Aceptar/Rechazar H₀)
* p-valor (si disponible)
* Gráfico: histograma de U con curva teórica opcional.

---

### 🖥️ Integración en la GUI (requerimientos del curso)

**Nueva pestaña “Pruebas”:**

* **Entradas:**

  * `n` (o se toma del tamaño de la muestra actual)
  * `α` (nivel de significancia)
* **Botones:** **Probar Medias**, **Probar Varianza**, **Exportar**
* **Salidas:**

  * Estadísticos, críticos, decisión, p-valor
  * Histogramas/ECDF (opcional)
* **Exportación:** CSV/Excel y **reporte** (txt/md) con: parámetros, estadísticos, decisión y fecha.
* **Menú principal:** atajos a “Generar”, “Pruebas”, “Variables”, “Exportar”.

**Nota de cumplimiento con el enunciado docente:**

* Python 3.10+, GUI en `tkinter`, uso de `numpy` y `matplotlib`.
* Resultados **numéricos y gráficos**.
* **Botones** Generar / Probar / Exportar.
* **Estructura + README** con instrucciones, capturas y bitácora.
* **Offline** para el examen.
* **Pruebas estadísticas y reportes** (30% de la nota) cubiertas con estas dos pruebas.

---

### ✅ Buenas prácticas y notas

* Para muestras chicas, puedes ofrecer opción **t-test** para la media (más conservador), aunque con Uniforme(0,1) y ( n ) moderado el Z-test es estándar.
* Documenta en el README: versión de Python, instalación (`requirements.txt`), ejemplos de uso y **capturas de la GUI**.
* Guarda toda **configuración y resultados** (incl. ( \alpha ), ( n )) para reproducibilidad en un JSON de sesión.

---


Perfecto ✅
Ya con las imágenes se identifican claramente las distribuciones del formulario.
Voy a integrarlas en tu **BASE DE CONOCIMIENTO DE LA CALCULADORA (v4)**, en una nueva sección:

---

## 🎲 Sección 3: Distribuciones continuas y discretas

*(todas usan los números pseudoaleatorios generados por los algoritmos anteriores)*

---

### 🔹 3.1 Distribuciones **continuas**

Cada distribución toma números `rᵢ` ∈ (0,1) generados por los algoritmos pseudoaleatorios (Cuadrados Medios, Productos Medios, Multiplicador Constante, etc.) para obtener una variable aleatoria `xᵢ` según su función inversa o fórmula de transformación.

---

#### **3.1.1 Distribución Uniforme U(a, b)**

**Fórmulas:**

* `xᵢ = a + (b − a) · rᵢ`
* Media: `(a + b) / 2`
* Varianza: `(b − a)² / 12`

**Pseudocódigo:**

```python
def uniforme(a: float, b: float, r: list[float]):
    return [a + (b - a) * ri for ri in r]
```

---

#### **3.1.2 Distribución Exponencial E(λ)**

**Fórmulas:**

* `xᵢ = −(1/λ) · ln(1 − rᵢ)`
* Media: `1/λ`
* Varianza: `1/λ²`

**Pseudocódigo:**

```python
import math
def exponencial(lmbda: float, r: list[float]):
    return [-(1/lmbda) * math.log(1 - ri) for ri in r]
```

---

#### **3.1.3 Distribución Erlang ER(k, λ)**

**Fórmulas:**

* `xᵢ = −(1/λ) · Σ ln(rⱼ)` para j = 1,…,k
* Media: `k/λ`
* Varianza: `k/λ²`

**Pseudocódigo:**

```python
import math
def erlang(k: int, lmbda: float, r: list[float]):
    xs = []
    for i in range(0, len(r), k):
        prod = 0
        for j in range(k):
            if i + j < len(r):
                prod += math.log(1 - r[i + j])
        xs.append(-(1/lmbda) * prod)
    return xs
```

---

#### **3.1.4 Distribución Gamma G(α, β)**

**Fórmulas:**

* `xᵢ = Σ_{j=1}^α (−β ln(rⱼ))`  (si α entero)
* Media: `αβ`
* Varianza: `αβ²`

**Pseudocódigo:**

```python
import math
def gamma(alpha: int, beta: float, r: list[float]):
    xs = []
    for i in range(0, len(r), alpha):
        suma = 0
        for j in range(alpha):
            if i + j < len(r):
                suma += -beta * math.log(1 - r[i + j])
        xs.append(suma)
    return xs
```

---

#### **3.1.5 Distribución Normal N(μ, σ)**

**Fórmulas (Box–Muller):**

* `z₁ = √(−2 ln(r₁)) · cos(2πr₂)`
* `z₂ = √(−2 ln(r₁)) · sin(2πr₂)`
* `xᵢ = μ + σ·zᵢ`
* Media: `μ`
* Varianza: `σ²`

**Pseudocódigo:**

```python
import math
def normal(mu: float, sigma: float, r: list[float]):
    xs = []
    for i in range(0, len(r)-1, 2):
        z1 = math.sqrt(-2 * math.log(r[i])) * math.cos(2 * math.pi * r[i+1])
        z2 = math.sqrt(-2 * math.log(r[i])) * math.sin(2 * math.pi * r[i+1])
        xs.extend([mu + sigma * z1, mu + sigma * z2])
    return xs
```

---

#### **3.1.6 Distribución Weibull W(γ, β, α)**

**Fórmulas:**

* `xᵢ = γ + β · (−ln(1 − rᵢ))^(1/α)`
* Media: `γ + β · Γ(1 + 1/α)`
* Varianza: `β² [Γ(1 + 2/α) − (Γ(1 + 1/α))²]`

**Pseudocódigo:**

```python
import math
def weibull(gamma_: float, beta: float, alpha: float, r: list[float]):
    return [gamma_ + beta * ((-math.log(1 - ri)) ** (1/alpha)) for ri in r]
```

---

### 🔹 3.2 Distribuciones **discretas**

Estas funciones también transforman los números pseudoaleatorios `rᵢ` ∈ (0,1) en valores enteros según la distribución deseada.

---

#### **3.2.1 Uniforme discreta U(a, b)**

**Fórmulas:**

* `xᵢ = a + int((b − a + 1) · rᵢ)`
* Media: `(a + b)/2`
* Varianza: `[(b − a + 1)² − 1]/12`

**Pseudocódigo:**

```python
def uniforme_discreta(a: int, b: int, r: list[float]):
    return [a + int((b - a + 1) * ri) for ri in r]
```

---

#### **3.2.2 Bernoulli(p)**

**Fórmulas:**

* `xᵢ = 1` si `rᵢ < p`, de lo contrario `0`
* Media: `p`
* Varianza: `p(1−p)`

**Pseudocódigo:**

```python
def bernoulli(p: float, r: list[float]):
    return [1 if ri < p else 0 for ri in r]
```

---

#### **3.2.3 Binomial(n, p)**

**Fórmulas:**

* `xᵢ = Σ_{j=1}^n B(p)` donde cada `B(p)` ~ Bernoulli(p)
* Media: `n·p`
* Varianza: `n·p·(1−p)`

**Pseudocódigo:**

```python
def binomial(n: int, p: float, r: list[float]):
    xs = []
    for i in range(0, len(r), n):
        suma = 0
        for j in range(n):
            if i + j < len(r) and r[i + j] < p:
                suma += 1
        xs.append(suma)
    return xs
```

---

#### **3.2.4 Poisson(λ)**

**Fórmulas (Knuth):**

* `xᵢ` = número de ocurrencias hasta que `Π rⱼ < e^(−λ)`
* Media: `λ`
* Varianza: `λ`

**Pseudocódigo:**

```python
import math
def poisson(lmbda: float, r: list[float]):
    xs = []
    L = math.exp(-lmbda)
    k = 0
    p = 1
    for ri in r:
        p *= ri
        if p <= L:
            xs.append(k)
            p = 1
            k = 0
        else:
            k += 1
    return xs
```

---

### 🧩 Integración con la calculadora

En la GUI (pestaña **Variables / Distribuciones**):

* Selector de distribución (Uniforme, Exponencial, Gamma, Normal, Weibull, Binomial, etc.)
* Parámetros según tipo (a, b, λ, μ, σ, α, β, etc.)
* Fuente de números: **algoritmo PRNG seleccionado**
* Botones: **Generar**, **Graficar**, **Exportar**
* Salidas: tabla numérica, media y varianza empíricas, histograma
* Exportación: CSV/Excel, imagen PNG, o copiar resultados al portapapeles.

---


## 🧬 SECCIÓN 4: EL JUEGO DE LA VIDA (CONWAY’S GAME OF LIFE)

---

### 📘 Descripción general

El **Juego de la Vida** es un **autómata celular bidimensional** creado por **John Horton Conway (1970)**.
A pesar de sus reglas extremadamente simples, este sistema puede producir **comportamientos complejos**, **autoorganización** y **patrones emergentes**.

Se utiliza ampliamente en **simulación y modelación** para estudiar sistemas que evolucionan en el tiempo con reglas locales.

---

### ⚙️ Componentes del modelo

| Elemento     | Descripción                                                           |
| ------------ | --------------------------------------------------------------------- |
| **Espacio**  | Rejilla 2D de tamaño finito (N×M).                                    |
| **Celdas**   | Cada celda puede estar **viva (1)** o **muerta (0)**.                 |
| **Vecindad** | Se usa la **vecindad de Moore** (8 celdas adyacentes).                |
| **Regla**    | Define el nuevo estado de una celda según su número de vecinos vivos. |
| **Tiempo**   | Evoluciona en pasos discretos (generaciones).                         |

---

### 🧩 Regla del Juego de la Vida (B3/S23)

**Regla formal:**
`B3/S23`

* **B3 (Birth):** una celda muerta **nace** si tiene exactamente **3 vecinos vivos**.
* **S23 (Survive):** una celda viva **sobrevive** si tiene **2 o 3 vecinos vivos**.
* En cualquier otro caso, la celda muere o permanece muerta.

---

### 🧮 Tabla de transición

| Estado actual | Vecinos vivos | Estado siguiente       |
| ------------- | ------------- | ---------------------- |
| Viva (1)      | < 2           | Muere (soledad)        |
| Viva (1)      | 2 o 3         | Sobrevive              |
| Viva (1)      | > 3           | Muere (superpoblación) |
| Muerta (0)    | = 3           | Nace (reproducción)    |

---

### 🔁 Ciclo de evolución

Cada generación se calcula aplicando la regla a **todas las celdas simultáneamente**.
El nuevo estado depende únicamente del estado anterior (no hay memoria).

Ejemplo (1 = viva, 0 = muerta):

**Generación 0:**

```
0 1 0
0 1 0
0 1 0
```

**Generación 1:**

```
0 0 0
1 1 1
0 0 0
```

**Generación 2:**

```
0 1 0
0 1 0
0 1 0
```

*(Este patrón es el famoso “Blinker”, un oscilador de periodo 2.)*

---

### 🧠 Tipos de patrones típicos

| Tipo              | Nombre                        | Descripción                                    |
| ----------------- | ----------------------------- | ---------------------------------------------- |
| **Estático**      | Block, Beehive                | No cambian con el tiempo.                      |
| **Oscilador**     | Blinker, Toad                 | Se repiten en ciclos de 2 o más generaciones.  |
| **Nave espacial** | Glider, Lightweight Spaceship | Se mueven por el tablero.                      |
| **Caótico**       | Random noise                  | Puede colapsar o generar estructuras estables. |

---

### ⚙️ Pseudocódigo en Python

```python
import numpy as np

def game_of_life_step(grid):
    """
    Calcula la siguiente generación del Juego de la Vida (B3/S23).
    grid: matriz 2D de 0 (muerta) y 1 (viva)
    """
    # Número de vecinos vivos usando vecindad de Moore
    neighbors = sum(np.roll(np.roll(grid, i, 0), j, 1)
                    for i in (-1, 0, 1)
                    for j in (-1, 0, 1)
                    if not (i == 0 and j == 0))

    # Aplicar regla B3/S23
    new_grid = ((neighbors == 3) | ((grid == 1) & (neighbors == 2))).astype(int)
    return new_grid
```

---

### 🔢 Ejemplo de uso

```python
import numpy as np
grid = np.array([
    [0, 1, 0],
    [0, 1, 0],
    [0, 1, 0]
])
for _ in range(4):
    print(grid)
    grid = game_of_life_step(grid)
```

Salida:

```
[[0 1 0]
 [0 1 0]
 [0 1 0]]

[[0 0 0]
 [1 1 1]
 [0 0 0]]
...
```

---

### 🎨 Representación visual en la GUI

**Pestaña:** “Juego de la Vida”
**Elementos:**

* **Canvas o área de visualización:** muestra el tablero (celdas vivas/muertas).
* **Controles:**

  * Tamaño del tablero (N×M)
  * Velocidad de actualización (ms)
  * Botones: **Iniciar / Pausar / Paso / Limpiar / Aleatorio / Exportar**
* **Inicialización aleatoria:**

  * Se genera usando los **números pseudoaleatorios** del proyecto (Sección 1).
* **Exportación:**

  * Guardar estados como imagen o CSV.
* **Indicadores:**

  * Generación actual, número de celdas vivas, tasa de cambio.

---

### 🔗 Integración con el resto del sistema

* El Juego de la Vida puede usar los **PRNG implementados** (Cuadrados Medios, Productos Medios, Multiplicador Constante) para inicializar el tablero con una probabilidad controlada de celdas vivas (`p`).
* Permite observar cómo distintos generadores afectan la **diversidad inicial** y la evolución del sistema.

**Ejemplo:**

```python
from core.rng import cuadrados_medios
import numpy as np

r = cuadrados_medios(semilla=5735, D=4, n=400)
tablero = np.array([1 if ri < 0.3 else 0 for ri in r]).reshape(20, 20)
```

---

### 🧮 Parámetros básicos

| Parámetro | Descripción                         | Valor típico |
| --------- | ----------------------------------- | ------------ |
| `N, M`    | Tamaño del tablero                  | 50×50        |
| `p`       | Probabilidad inicial de celda viva  | 0.2–0.3      |
| `ms`      | Tiempo por frame (ms)               | 100–500      |
| `modo`    | Toroidal (bordes conectados) o fijo | Toroidal     |

---

### 🧩 Propósito en la materia

* Representa un **modelo de simulación discreta**.
* Demuestra **emergencia** y **autoorganización**.
* Permite **visualizar evolución dinámica** con control de **aleatoriedad inicial**.
* Conecta teoría de **autómatas celulares** con práctica de **simulación computacional**.

---

## 🧬 SECCIÓN 5: AUTÓMATAS CELULARES (CON TODAS LAS REGLAS DISPONIBLES)

---

### 📘 Descripción general

Un **autómata celular** es un sistema discreto donde cada celda de una rejilla evoluciona en el tiempo según una **regla local** que depende de:

* Su **estado actual**, y
* El **estado de sus celdas vecinas**.

El comportamiento global del sistema emerge de la **aplicación simultánea** de estas reglas simples a todas las celdas.

---

### ⚙️ Componentes

| Elemento     | Descripción                                           |
| ------------ | ----------------------------------------------------- |
| **Espacio**  | Rejilla de celdas (1D o 2D).                          |
| **Estados**  | Generalmente binarios (0 = muerto, 1 = vivo).         |
| **Vecindad** | Grupo de celdas adyacentes que influyen en una celda. |
| **Regla**    | Determina el estado futuro de cada celda.             |
| **Tiempo**   | Discreto: las celdas se actualizan por generaciones.  |

---

## 🧩 TIPOS DE AUTÓMATAS Y REGLAS

---

### 🔹 1D — Reglas de Wolfram (256 reglas)

Los autómatas **unidimensionales (1D)** usan 3 celdas vecinas: la izquierda, la actual y la derecha.
Cada una puede tener 2 estados, así que existen **2⁸ = 256 reglas posibles**.

Cada regla se representa por un número entre **0 y 255**, conocido como **número de Wolfram**.

---

#### 📘 Ejemplo de codificación de reglas (Regla 30)

| Vecindad     | 111 | 110 | 101 | 100 | 011 | 010 | 001 | 000 |
| ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
| Nuevo estado | 0   | 0   | 0   | 1   | 1   | 1   | 1   | 0   |

Esto corresponde al número binario `00011110` → `30` en decimal.

---

#### ⚙️ Pseudocódigo (1D general)

```python
def automata_1d_step(linea, regla):
    """
    Aplica una regla 1D de Wolfram (0-255) a una línea binaria.
    """
    n = len(linea)
    nueva = [0] * n
    for i in range(n):
        izquierda = linea[(i - 1) % n]
        centro = linea[i]
        derecha = linea[(i + 1) % n]
        patron = (izquierda << 2) | (centro << 1) | derecha
        nueva[i] = (regla >> patron) & 1
    return nueva
```

---

#### 🔢 Reglas 1D destacadas (por comportamiento)

| Regla | Tipo de comportamiento | Descripción                              |
| ----- | ---------------------- | ---------------------------------------- |
| 0     | Muerte total           | Todo se apaga.                           |
| 30    | Caótico                | Comportamiento complejo (usado en PRNG). |
| 45    | Semicaótico            | Alternancia irregular.                   |
| 54    | Estructuras móviles    | Ondas regulares.                         |
| 60    | Simétrico              | Patrón triangular invertido.             |
| 90    | Autosemejante          | Genera patrón tipo Sierpinski.           |
| 102   | Reflejo de 90          | Patrón simétrico.                        |
| 110   | Universal              | Computacionalmente universal.            |
| 126   | Caótico fuerte         | Llenado denso de 1s y 0s.                |
| 150   | Lineal XOR             | Autosemejante simétrico.                 |
| 184   | Tráfico                | Simula movimiento y densidad.            |
| 232   | Estable                | Estructuras estáticas.                   |
| 250   | Patrón periódico       | Alternancia regular.                     |
| 255   | Saturación             | Todo se enciende (solo 1s).              |

👉 En la GUI podrás elegir cualquiera de las **256 reglas**, o seleccionar una de las **más comunes (arriba)** desde un menú predefinido.

---

### 🔹 2D — Reglas Life-like (basadas en B/S)

Los autómatas **bidimensionales (2D)** se definen mediante la notación **B/S**, donde:

* **B** (*Birth*): vecinos que hacen **nacer** una celda muerta.
* **S** (*Survive*): vecinos que hacen **sobrevivir** una celda viva.

Se usa la **vecindad de Moore (8 vecinos)**.

---

#### 📘 Regla general

```
B{nacimientos}/S{supervivencias}
```

Ejemplo:

* **B3/S23** → Nace con 3 vecinos, sobrevive con 2 o 3. (Juego de la Vida)
* **B36/S23** → Igual que Life, pero nace también con 6 (HighLife).
* **B2/S** → Seeds: toda celda muere salvo nuevos nacimientos con 2 vecinos.

---

### 🔢 Reglas 2D incluidas

| Nombre                 | Regla B/S     | Descripción breve                                         |
| ---------------------- | ------------- | --------------------------------------------------------- |
| **Game of Life**       | B3/S23        | Clásico; genera osciladores, gliders y patrones estables. |
| **HighLife**           | B36/S23       | Igual que Life, pero permite “replicadores”.              |
| **Seeds**              | B2/S          | Explosivo; solo nacen celdas, nunca sobreviven.           |
| **Day & Night**        | B3678/S34678  | Simétrica: se comporta igual al invertir vivos/muertos.   |
| **Life Without Death** | B3/S012345678 | Una vez viva, nunca muere.                                |
| **Diamoeba**           | B35678/S5678  | Patrones ameboides.                                       |
| **Coral Growth**       | B3/S45678     | Estructuras ramificadas.                                  |
| **Maze**               | B3/S12345     | Forma laberintos estáticos.                               |
| **Replicator**         | B1357/S1357   | Se autorreplica; genera estructuras repetitivas.          |
| **Amoeba**             | B357/S1358    | Estructuras de crecimiento suave.                         |
| **Serviettes**         | B234/S        | Explosivo; crece como manchas simétricas.                 |
| **Coagulations**       | B378/S235678  | Tiende a unir estructuras pequeñas.                       |
| **LongLife**           | B345/S5       | Lento; mantiene patrones por más tiempo.                  |
| **Assimilation**       | B345/S4567    | Simula absorción o dominancia entre regiones.             |
| **Stains**             | B3678/S235678 | Expande manchas densas.                                   |
| **WalledCities**       | B45678/S2345  | Genera estructuras cuadradas tipo “ciudad”.               |
| **Faders**             | B3678/S235678 | Tiende a patrones oscilantes suaves.                      |
| **Anneal**             | B4678/S35678  | Alternancia estable de densidades.                        |

> 💡 Todas las reglas anteriores son **Life-like** (binarias, con vecindad de Moore).
> En la GUI, podrás escribir tu propia regla (ej. “B36/S23”) o elegir una predefinida de la lista.

---

### ⚙️ Pseudocódigo (2D genérico con regla B/S)

```python
def automata_2d_step(grid, B, S, toroide=True):
    """
    Aplica una regla B/S en un autómata celular 2D binario.
    """
    n, m = len(grid), len(grid[0])

    def get(i, j):
        if toroide:
            return grid[i % n][j % m]
        if 0 <= i < n and 0 <= j < m:
            return grid[i][j]
        return 0

    nuevo = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            vecinos = 0
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if di or dj:
                        vecinos += get(i + di, j + dj)
            viva = grid[i][j] == 1
            nuevo[i][j] = 1 if ((not viva and vecinos in B) or (viva and vecinos in S)) else 0
    return nuevo
```

---

### 🎮 Integración en la GUI (Selector de Reglas)

**Pestaña:** “Autómatas Celulares”

**Controles:**

* **Tipo:** 1D / 2D
* **Selector de regla:**

  * Para 1D: deslizador o campo numérico (0–255).
  * Para 2D: menú desplegable (Life, HighLife, Seeds, Maze, etc.) o campo editable “B/S”.
* **Parámetros:**

  * Tamaño (N, M)
  * Iteraciones o pasos
  * Velocidad de simulación
* **Inicialización:**

  * Manual (matriz ingresada)
  * Aleatoria (usando **números pseudoaleatorios** generados por tus algoritmos)
* **Botones:**

  * **Iniciar / Pausar / Paso / Reiniciar / Limpiar / Exportar**
* **Visualización:**

  * Canvas o `matplotlib.imshow()`
  * Colores:

    * 1 → activo / vivo
    * 0 → inactivo / muerto
* **Exportación:**

  * CSV, PNG, o secuencia animada (GIF).

---

### 🔗 Integración con los PRNG del proyecto

Los números pseudoaleatorios de las secciones anteriores (Cuadrados Medios, Productos Medios, Multiplicador Constante, etc.) pueden usarse para:

* **Inicializar el tablero o línea inicial:**
  `celda = 1 si rᵢ < p else 0`
* **Asignar reglas aleatorias** (1D o B/S).
* **Simular ruido o perturbaciones controladas.**

---

### 🧠 Propósito académico

Permite visualizar cómo **reglas locales simples** producen **comportamientos globales complejos**, aplicando conceptos de:

* Modelos discretos de simulación
* Sistemas dinámicos
* Complejidad computacional
* Emergencia y autoorganización

---

### ✅ Reglas disponibles para el selector (resumen)

#### 🔸 1D

```
0–255 (Reglas de Wolfram)
```

#### 🔸 2D (Life-like)

```
B3/S23           → Game of Life  
B36/S23          → HighLife  
B2/S             → Seeds  
B3678/S34678     → Day & Night  
B3/S012345678    → Life Without Death  
B35678/S5678     → Diamoeba  
B3/S45678        → Coral Growth  
B3/S12345        → Maze  
B1357/S1357      → Replicator  
B357/S1358       → Amoeba  
B234/S           → Serviettes  
B378/S235678     → Coagulations  
B345/S5          → LongLife  
B345/S4567       → Assimilation  
B3678/S235678    → Stains  
B45678/S2345     → WalledCities  
B3678/S235678    → Faders  
B4678/S35678     → Anneal
```

---

