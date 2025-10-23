# 🧮 Calculadora de Simulación y Modelación

Este proyecto implementa una calculadora multifuncional para simulación y modelación, desarrollada en Python. Incluye generadores de números pseudoaleatorios, pruebas estadísticas, autómatas celulares y distribuciones de probabilidad, todo ello a través de una interfaz gráfica de usuario moderna y funcional.

## 🚀 1. Desarrollo en Python

**Lenguaje:** Python 3.10+

**Librerías utilizadas:**
*   `numpy`: Para operaciones numéricas y generación de arrays.
*   `matplotlib`: Para la visualización gráfica de resultados (histogramas, autómatas).
*   `tkinter` (estándar) y `tkinter.ttk`: Para la construcción de la interfaz gráfica de usuario (GUI).
*   `pandas`: Para la exportación de datos a formatos como CSV/Excel.

### Estructura del Proyecto

```
Calculadora/
├── main.py
├── requirements.txt
├── BASEDECONOCIMIENTODELACALCULADORA.md
├── cellular_automata/
│   ├── __init__.py
│   ├── automata_1d_2d.py
│   └── game_of_life.py
├── distributions/
│   ├── __init__.py
│   └── continuous_discrete.py
├── gui/
│   ├── __init__.py
│   ├── automata_main_tab.py
│   ├── cellular_automata_subtab.py
│   ├── distributions_tab.py
│   ├── game_of_life_subtab.py
│   ├── generators_tab.py
│   ├── main_window.py
│   └── tests_tab.py
├── rng_algorithms/
│   ├── __init__.py
│   ├── cuadrados_medios.py
│   ├── multiplicador_constante.py
│   └── productos_medios.py
├── statistical_tests/
│   ├── __init__.py
│   ├── prueba_medias.py
│   └── prueba_varianza.py
└── utils/
    ├── __init__.py
    ├── data_exporter.py
    └── plotting.py
```

## 🖥️ 2. Interfaz Gráfica (GUI)

La aplicación cuenta con una interfaz gráfica implementada con `tkinter` y `ttk`, organizada en pestañas para facilitar la navegación entre las diferentes funcionalidades:

*   **Generadores:** Permite seleccionar y configurar algoritmos de generación de números pseudoaleatorios (Cuadrados Medios, Productos Medios, Multiplicador Constante).
*   **Pruebas:** Ofrece herramientas para realizar pruebas estadísticas sobre los números generados (Prueba de Medias, Prueba de Varianza).
*   **Autómatas / Juego de la Vida:** Contiene simulaciones de autómatas celulares 1D y 2D, incluyendo el clásico Juego de la Vida de Conway.
*   **Distribuciones:** Permite generar números aleatorios a partir de diversas distribuciones continuas y discretas, utilizando los PRNGs del proyecto.

Cada pestaña incluye campos de entrada para parámetros (`n`, semillas, reglas, etc.), botones de acción (`Generar`, `Probar`, `Exportar`) y áreas de visualización para resultados numéricos y gráficos (histogramas, estados de autómatas).

### Estilo Visual

La interfaz ha sido diseñada con un estilo **cyberpunk**, utilizando una paleta de colores oscuros con acentos de neón vibrantes para una estética moderna y distintiva, asegurando al mismo tiempo la legibilidad y visibilidad de todos los elementos.

## 🚀 Requisitos y Pasos de Instalación/Ejecución

### Requisitos

*   Python 3.10 o superior.
*   Las librerías `numpy`, `matplotlib`, `pandas`.

### Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone [ENLACE_DEL_REPOSITORIO]
    cd Calculadora
    ```
2.  **Crear y activar un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```
3.  **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

### Ejecución

1.  **Activar el entorno virtual** (si no lo has hecho ya).
2.  **Ejecutar el script principal:**
    ```bash
    python main.py
    ```

## 📸 Capturas de Pantalla de la GUI

*(Por favor, inserta aquí las capturas de pantalla de las diferentes pestañas de la GUI para mostrar su funcionamiento y estilo visual.)*

## 📝 Bitácora de Avances por Clase

*(Este espacio está reservado para documentar los avances específicos realizados en cada clase, según lo requiera el docente.)*

## 🤝 Agradecimientos y Colaboración Externa

Este proyecto ha sido desarrollado con la asistencia de **Gemini**, un modelo de lenguaje grande de Google, que proporcionó orientación en la implementación de funcionalidades, depuración de errores y refinamiento del código y la interfaz de usuario. Su ayuda fue fundamental para alcanzar los objetivos del proyecto.

## 👨‍🏫 Docente

M.Sc Ing. Neddy Etman Choque Flores

## 📚 Materia

Simulación y modelación
