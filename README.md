# 🧩 Pokémon Image Processing Pipeline  
**Versión optimizada con paralelismo y concurrencia**  


---

## 📘 Descripción general

Este proyecto implementa un **pipeline de procesamiento de imágenes de Pokémon** con dos fases principales:

1. **Descarga concurrente** de imágenes desde un repositorio remoto.  
2. **Procesamiento paralelo** de las imágenes aplicando transformaciones gráficas.

El objetivo fue **mejorar el rendimiento** del código base (baseline) mediante la aplicación de **paralelismo** y **concurrencia**, reduciendo el tiempo total de ejecución utilizando hasta **8 núcleos** del procesador.

---

## ⚙️ Tecnologías utilizadas

- **Python 3.10+**
- Librerías principales:
  - `concurrent.futures` (para concurrencia y paralelismo)
  - `requests` (para descargas HTTP)
  - `Pillow (PIL)` (para procesamiento de imágenes)
  - `tqdm` (para barras de progreso)
  - `os`, `time` (para manejo de archivos y medición de tiempos)

---

## 🚀 Estrategias de optimización aplicadas

### 1️⃣ Descarga concurrente (I/O Bound)

**Problema:**  
La descarga secuencial de imágenes genera cuellos de botella debido a la latencia de red.

**Solución:**  
Se implementó **descarga concurrente** utilizando `ThreadPoolExecutor` con 10 hilos.  
Cada hilo descarga una imagen de forma independiente, aprovechando los tiempos de espera de la red para ejecutar otras descargas simultáneamente.

**Ventajas:**
- Aprovechamiento eficiente del tiempo de I/O.
- Reducción drástica del tiempo total de descarga.

---

### 2️⃣ Procesamiento paralelo (CPU Bound)

**Problema:**  
El procesamiento de imágenes (filtros, contraste, resizing, inversión, etc.) es intensivo en CPU.

**Solución:**  
Se aplicó **procesamiento paralelo** con `ProcessPoolExecutor` usando 8 procesos (uno por núcleo disponible).  
Cada proceso trabaja sobre una imagen de manera independiente.

**Ventajas:**
- Aceleración casi lineal respecto al número de núcleos.  
- Evita bloqueos del GIL (Global Interpreter Lock).  
- Reducción significativa del tiempo de procesamiento.

---

## 🧠 Arquitectura general del programa

```text
main.py
├── Descarga concurrente de imágenes (ThreadPoolExecutor)
│     └── download_single_pokemon()
│
├── Procesamiento paralelo de imágenes (ProcessPoolExecutor)
│     └── process_single_image()
│
└── Resumen de tiempos y resultados finales
