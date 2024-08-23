Aquí tienes un ejemplo de un README para tu proyecto en GitHub:

---

# Proyecto de Reconocimiento y Conteo de Ejercicios con OpenCV y MediaPipe

Este proyecto consiste en una serie de scripts que utilizan las bibliotecas OpenCV y MediaPipe para detectar y contar repeticiones de ejercicios físicos. Incluye la detección de abdominales, dominadas, y vueltas durante una carrera.

## Características

- **Abdominales**: Detección y conteo automático de abdominales utilizando la posición de la nariz.
- **Dominadas**: Detección y conteo automático de dominadas utilizando la posición de los hombros, codos, y muñecas.
- **Vueltas (Correr)**: Detección y conteo de vueltas completadas utilizando la posición de un punto de referencia en el cuerpo.
- **Interfaz Gráfica**: Una interfaz gráfica simple construida con Tkinter para seleccionar y ejecutar las distintas actividades.

## Requisitos

Asegúrate de tener instaladas las siguientes bibliotecas:

```bash
pip install opencv-python mediapipe matplotlib pillow
```

## Uso

### 1. Abdominales

Ejecuta el script `abdominales_cont.py` para iniciar la detección y conteo de abdominales. Se mostrará el número de abdominales realizados en una ventana de video en tiempo real.

```bash
python abdominales_cont.py
```

### 2. Dominadas

Ejecuta el script `barras_cont.py` para iniciar la detección y conteo de dominadas. Se mostrará el número de dominadas correctas en una ventana de video en tiempo real.

```bash
python barras_cont.py
```

### 3. Vueltas (Correr)

Ejecuta el script `correr_cont.py` para iniciar la detección y conteo de vueltas. Se mostrará el número de vueltas completadas en una ventana de video en tiempo real.

```bash
python correr_cont.py
```

### 4. Interfaz Gráfica

Para utilizar la interfaz gráfica, ejecuta el script principal `main.py`. Desde la interfaz, podrás seleccionar y ejecutar cualquiera de los ejercicios mencionados anteriormente.

```bash
python main.py
```

## Resultados

Los resultados de cada ejercicio se guardan en archivos CSV, que incluyen el nombre del usuario y el número de repeticiones o tiempos de vuelta:

- `resultados_abdominales.csv`
- `resultados_dominadas.csv`
- `vueltasprueba.csv`

Además, se generan gráficas de los resultados al finalizar cada sesión.

## Créditos

Este proyecto utiliza las siguientes bibliotecas:

- [OpenCV](https://opencv.org/)
- [MediaPipe](https://mediapipe.dev/)
- [Matplotlib](https://matplotlib.org/)
- [Tkinter](https://wiki.python.org/moin/TkInter)
