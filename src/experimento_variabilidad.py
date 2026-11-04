"""
Experimento complementario (Entrega 3): ¿qué tan predecible es cada técnica?

Ejecuta backtracking y programación dinámica sobre 9 instancias distintas
con el MISMO tamaño (n = 1000), todas generadas con generar_datos.generar.
Muestra que el tiempo del backtracking depende mucho de los datos (su
complejidad es exponencial en el peor caso), mientras que la programación
dinámica siempre hace n x (T+1) operaciones y su tiempo casi no cambia.

Uso:  python src/experimento_variabilidad.py      (~1-2 minutos)
"""
import time

from backtracking import backtracking
from dinamica import programacion_dinamica
from fuerza_bruta import Tarea
from generar_datos import generar

SEMILLAS = [1001, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1011]
N = 1000

print(f"{'Semilla':>8}{'T':>7} | {'BT nodos':>12}{'BT tiempo':>12} | {'PD tiempo':>10}")
print("-" * 56)
tiempos_bt, tiempos_pd = [], []
for semilla in SEMILLAS:
    capacidad, datos = generar(N, semilla)
    tareas = [Tarea(*d) for d in datos]

    inicio = time.perf_counter()
    p_bt, _, nodos = backtracking(tareas, capacidad)
    t_bt = time.perf_counter() - inicio

    inicio = time.perf_counter()
    p_pd, _, _ = programacion_dinamica(tareas, capacidad)
    t_pd = time.perf_counter() - inicio

    assert p_bt == p_pd
    tiempos_bt.append(t_bt)
    tiempos_pd.append(t_pd)
    print(f"{semilla:>8}{capacidad:>7} | {nodos:>12,}{t_bt:>11.3f}s | {t_pd:>9.3f}s", flush=True)

print("-" * 56)
print(f"Backtracking:          min {min(tiempos_bt):.3f} s  max {max(tiempos_bt):.3f} s "
      f"(x{max(tiempos_bt) / min(tiempos_bt):.0f})")
print(f"Programación dinámica: min {min(tiempos_pd):.3f} s  max {max(tiempos_pd):.3f} s "
      f"(x{max(tiempos_pd) / min(tiempos_pd):.1f})")
