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
src/generar_datos.py           genera caso_mediano.txt y caso_grande.txt
src/comparativa.py             ejecuta todas las técnicas, imprime tablas y genera gráficas en docs/
docs/                          documentos PDF y gráficas de cada entrega
```

## Cómo ejecutar

Requisitos: Python 3.10+ y `matplotlib` (`pip install matplotlib`).

```bash
python src/fuerza_bruta.py           # fuerza bruta (el caso grande tarda ~30-50 s)
python src/greedy.py
python src/backtracking.py
python src/comparativa.py            # comparativa completa (~1-2 min)
python src/comparativa.py --rapido   # omite la fuerza bruta del caso grande
```

## Entregas

| Entrega | Contenido | Documento |
|---|---|---|
| 1 | Definición del problema, fuerza bruta, análisis de complejidad | `docs/entrega1.pdf` |
| 2 | Greedy, backtracking y comparativa parcial | `docs/entrega2.pdf` |
