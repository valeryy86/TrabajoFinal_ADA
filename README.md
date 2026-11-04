# TrabajoFinal_ADA

Trabajo final de Análisis y Diseño de Algoritmos (2026-2).
**Caso de uso 3.4 — Optimización de Tareas en Servidores:** dado un servidor con capacidad de tiempo `T` y `n` tareas (tiempo, prioridad), elegir el subconjunto que maximiza la prioridad total sin superar `T` (mochila 0/1).

## Integrantes:
Valery Monsalve Correa
Samuel Uribe Salazar

## Estructura

```
datos/                         casos de prueba (formato: "n T" y luego "id tiempo prioridad")
src/fuerza_bruta.py            Entrega 1 - O(2^n)
src/greedy.py                  Entrega 2 - densidad prioridad/tiempo, O(n log n)
src/backtracking.py            Entrega 2 - poda por capacidad + cota fraccional
src/divide_y_venceras.py       Entrega 3 - mitades + frentes de Pareto, Theta(n^2) en nuestras instancias
src/dinamica.py                Entrega 3 - tabla O(n*T) con reconstrucción
src/comparativa.py             ejecuta las 5 técnicas, imprime la tabla final y genera gráficas en docs/
src/experimento_variabilidad.py  backtracking vs programación dinámica en 9 instancias n=1000
src/generar_datos.py           genera los casos mediano, grande, n100 y n1000
docs/                          documentos PDF y gráficas de cada entrega
presentacion/                  presentación final
```

## Cómo ejecutar

Requisitos: Python 3.10+ y `matplotlib` (`python -m pip install matplotlib`).

```bash
python src/fuerza_bruta.py              # el caso grande tarda ~30-50 s
python src/greedy.py
python src/backtracking.py
python src/divide_y_venceras.py         # n=1000 tarda ~30 s
python src/dinamica.py
python src/comparativa.py               # comparativa final completa (~3 min)
python src/comparativa.py --rapido      # versión para la demo (~20 s)
python src/experimento_variabilidad.py  # ~1-2 min
```

## Resultados principales (n = 1000)

| Técnica | ¿Óptima? | Tiempo |
|---|---|---|
| Fuerza bruta | Sí | inviable (~10^286 años, estimado) |
| Greedy | No (99.97 %) | 0.0004 s |
| Backtracking | Sí | 2.6 s (de 0.03 a 30 s según los datos) |
| Divide y vencerás | Sí | 30.6 s |
| Programación dinámica | Sí | 0.94 s |

**Técnica recomendada:** programación dinámica (óptima, tiempo predecible O(n·T) y < 1 s para 1000 tareas).

## Entregas

| Entrega | Contenido | Documento |
|---|---|---|
| 1 | Definición del problema, fuerza bruta, análisis de complejidad | `docs/entrega1.pdf` |
| 2 | Greedy, backtracking y comparativa parcial | `docs/entrega2.pdf` |
| 3 | Divide y vencerás, programación dinámica, comparativa final y conclusiones | `docs/entrega3_final.pdf` |
