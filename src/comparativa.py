"""
Comparativa Entrega 2: Fuerza bruta vs Greedy vs Backtracking.

Ejecuta las tres soluciones sobre:
  1. Los archivos de prueba de datos/  -> tabla para el PDF
  2. Instancias aleatorias n = 5..25   -> gráfica de tiempos (escala log)
  3. Instancias grandes n = 50..1000   -> escalabilidad greedy vs backtracking
     (la fuerza bruta ya no termina en tiempo razonable)
  4. Calidad del greedy (% del óptimo) para cada n

Uso (desde la raíz del repo o desde src/):
    python src/comparativa.py
    python src/comparativa.py --rapido   (omite la fuerza bruta del caso grande)
"""
import os
import random
import sys
import time

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from backtracking import backtracking
from fuerza_bruta import Tarea, cargar_caso, fuerza_bruta_rec
from greedy import greedy

DIR_SRC = os.path.dirname(os.path.abspath(__file__))
DIR_DATOS = os.path.join(DIR_SRC, "..", "datos")
DIR_DOCS = os.path.join(DIR_SRC, "..", "docs")
RAPIDO = "--rapido" in sys.argv

random.seed(2026)  # resultados reproducibles


def generar_caso(n):
    """Tareas aleatorias con prioridad correlacionada con el tiempo (igual
    que generar_datos.py). Capacidad = 45 % de la suma de tiempos."""
    tareas = []
    for i in range(1, n + 1):
        t = random.randint(5, 30)
        tareas.append(Tarea(i, t, max(1, t + random.randint(-3, 12))))
    capacidad = int(sum(x.tiempo for x in tareas) * 0.45)
    return tareas, capacidad


def cronometrar(funcion, *args):
    inicio = time.perf_counter()
    resultado = funcion(*args)
    return resultado, time.perf_counter() - inicio


# -------------------------------------------------------------
# 1. ARCHIVOS DE PRUEBA
# -------------------------------------------------------------
print("=" * 96)
print("1. ARCHIVOS DE PRUEBA")
print("=" * 96)
print(f"{'Archivo':<32}{'n':>4}{'T':>6} | {'FB prio':>8}{'FB seg':>11} | "
      f"{'Greedy':>7}{'G seg':>10} | {'BT prio':>8}{'BT seg':>10}{'nodos BT':>10}")
print("-" * 96)

archivos = ["caso_contraejemplo_greedy.txt", "caso_pequeno.txt",
            "caso_mediano.txt", "caso_grande.txt"]

for nombre in archivos:
    ruta = os.path.join(DIR_DATOS, nombre)
    if not os.path.exists(ruta):
        print(f"Advertencia: no se encontró {ruta}")
        continue
    n, cap, tareas = cargar_caso(ruta)

    if RAPIDO and n > 22:
        fb_p, fb_t = None, None
    else:
        (fb_p, _), fb_t = cronometrar(fuerza_bruta_rec, tareas, cap, 0)
    (g_p, _, _), g_t = cronometrar(greedy, tareas, cap)
    (bt_p, _, nodos), bt_t = cronometrar(backtracking, tareas, cap)

    fb_txt = f"{fb_p:>8}{fb_t:>11.4f}" if fb_p is not None else f"{'-':>8}{'omitido':>11}"
    marca = "" if g_p == bt_p else " *"
    print(f"{nombre:<32}{n:>4}{cap:>6} | {fb_txt} | {g_p:>7}{g_t:>10.6f} | "
          f"{bt_p:>8}{bt_t:>10.6f}{nodos:>10,}{marca}")

print("(*) el greedy NO alcanzó el óptimo en ese caso\n")


# -------------------------------------------------------------
# 2. CURVA n = 5..25 CON LAS TRES TÉCNICAS
# -------------------------------------------------------------
print("=" * 96)
print("2. CURVA DE TIEMPOS n = 5..25 (fuerza bruta, backtracking sin/con cota, greedy)")
print("=" * 96)
tam_chicos = list(range(5, 26, 2))
t_fb, t_bt_cap, t_bt, t_g = [], [], [], []
calidad_chicos = []

for n in tam_chicos:
    tareas, cap = generar_caso(n)
    (p_fb, _), tf = cronometrar(fuerza_bruta_rec, tareas, cap, 0)
    (_, _, nodos_cap), tc = cronometrar(backtracking, tareas, cap, False)
    (p_bt, _, nodos), tb = cronometrar(backtracking, tareas, cap)
    (p_g, _, _), tg = cronometrar(greedy, tareas, cap)
    assert p_fb == p_bt, "El backtracking debe coincidir con la fuerza bruta"
    t_fb.append(tf); t_bt_cap.append(tc); t_bt.append(tb); t_g.append(tg)
    calidad_chicos.append(100 * p_g / p_bt)
    print(f"n={n:3d} | FB {tf:9.4f}s | BT solo capacidad {tc:9.4f}s ({nodos_cap:>9,} nodos) | "
          f"BT con cota {tb:.6f}s ({nodos:>5,} nodos) | Greedy {tg:.6f}s ({100*p_g/p_bt:5.1f}% del óptimo)")


# -------------------------------------------------------------
# 3. ESCALABILIDAD n = 50..1000 (greedy vs backtracking)
# -------------------------------------------------------------
print("\n" + "=" * 96)
print("3. ESCALABILIDAD n = 50..1000 (la fuerza bruta es inviable: 2^50 ~ 10^15 nodos)")
print("=" * 96)
tam_grandes = [50, 100, 200, 500, 1000]
t_bt_g, t_g_g, calidad_grandes = [], [], []

for n in tam_grandes:
    tareas, cap = generar_caso(n)
    (p_bt, _, nodos), tb = cronometrar(backtracking, tareas, cap)
    (p_g, _, _), tg = cronometrar(greedy, tareas, cap)
    t_bt_g.append(tb); t_g_g.append(tg)
    calidad_grandes.append(100 * p_g / p_bt)
    print(f"n={n:5d} | BT con cota {tb:9.4f}s ({nodos:>9,} nodos) | "
          f"Greedy {tg:.6f}s ({100*p_g/p_bt:6.2f}% del óptimo)")


# -------------------------------------------------------------
# 4. GRÁFICAS
# -------------------------------------------------------------
os.makedirs(DIR_DOCS, exist_ok=True)

fig, ax = plt.subplots(figsize=(9, 5.5))
ax.plot(tam_chicos, t_fb, "o-", color="red", lw=2, label="Fuerza bruta O(2^n)")
ax.plot(tam_chicos, t_bt_cap, "s--", color="orange", lw=2, label="Backtracking (solo poda por capacidad)")
ax.plot(tam_chicos, t_bt, "^-", color="green", lw=2, label="Backtracking (capacidad + cota)")
ax.plot(tam_chicos, t_g, "d-", color="blue", lw=2, label="Greedy O(n log n)")
ax.set_yscale("log")
ax.set_title("Tiempo de ejecución vs n (escala logarítmica)")
ax.set_xlabel("Número de tareas (n)")
ax.set_ylabel("Tiempo (segundos, log)")
ax.grid(True, which="both", alpha=0.3)
ax.legend()
fig.tight_layout()
ruta1 = os.path.join(DIR_DOCS, "grafica_entrega2_tiempos.png")
fig.savefig(ruta1, dpi=150)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
ax1.plot(tam_grandes, t_bt_g, "^-", color="green", lw=2, label="Backtracking (capacidad + cota)")
ax1.plot(tam_grandes, t_g_g, "d-", color="blue", lw=2, label="Greedy")
ax1.set_yscale("log")
ax1.set_title("Escalabilidad (n grande)")
ax1.set_xlabel("Número de tareas (n)")
ax1.set_ylabel("Tiempo (segundos, log)")
ax1.grid(True, which="both", alpha=0.3)
ax1.legend()

todos_n = tam_chicos + tam_grandes
todas_cal = calidad_chicos + calidad_grandes
ax2.plot(todos_n, todas_cal, "d-", color="blue", lw=2)
ax2.axhline(100, color="green", ls="--", label="Óptimo (FB / Backtracking)")
ax2.set_xscale("log")
ax2.set_title("Calidad del greedy (% de la prioridad óptima)")
ax2.set_xlabel("Número de tareas (n, log)")
ax2.set_ylabel("% del óptimo")
ax2.grid(True, which="both", alpha=0.3)
ax2.legend()
fig.tight_layout()
ruta2 = os.path.join(DIR_DOCS, "grafica_entrega2_escalabilidad.png")
fig.savefig(ruta2, dpi=150)

print(f"\nGráficas guardadas en:\n  {os.path.normpath(ruta1)}\n  {os.path.normpath(ruta2)}")
