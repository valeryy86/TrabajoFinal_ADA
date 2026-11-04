"""
Comparativa FINAL (Entrega 3): las 5 técnicas sobre el mismo problema.

    FB  = Fuerza bruta              (Entrega 1)
    G   = Greedy                    (Entrega 2)
    BT  = Backtracking con poda     (Entrega 2)
    DV  = Divide y vencerás         (Entrega 3)
    PD  = Programación dinámica     (Entrega 3)

Partes:
  1. Archivos de prueba de datos/ (incluye n=100 y n=1000)
     -> verifica que FB, BT, DV y PD den la MISMA prioridad óptima.
  2. Tabla comparativa final (complejidades + tiempos reales n=100, n=1000).
  3. Curva de tiempos vs n para las 5 técnicas (gráfica principal).
  4. Gráficas guardadas en docs/.

Uso (desde la raíz del repo o desde src/):
    python src/comparativa.py            # completo (~3 min)
    python src/comparativa.py --rapido   # para la demo (~20 s): omite FB n=28
                                         # y DV con n > 400
"""
import os
import sys
import time

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from backtracking import backtracking
from dinamica import programacion_dinamica
from divide_y_venceras import divide_y_venceras
from fuerza_bruta import Tarea, cargar_caso, fuerza_bruta_rec
from generar_datos import generar
from greedy import greedy

DIR_SRC = os.path.dirname(os.path.abspath(__file__))
DIR_DATOS = os.path.join(DIR_SRC, "..", "datos")
DIR_DOCS = os.path.join(DIR_SRC, "..", "docs")
RAPIDO = "--rapido" in sys.argv

LIMITE_FB = 25 if RAPIDO else 28     # n máximo en que se ejecuta la fuerza bruta
LIMITE_DV = 400 if RAPIDO else 1000  # n máximo en que se ejecuta divide y vencerás

NOMBRES = {"FB": "Fuerza bruta", "G": "Greedy", "BT": "Backtracking",
           "DV": "Divide y vencerás", "PD": "Programación dinámica"}
COLORES = {"FB": "#d62728", "G": "#1f77b4", "BT": "#2ca02c",
           "DV": "#9467bd", "PD": "#ff7f0e"}
MARCAS = {"FB": "o", "G": "d", "BT": "^", "DV": "s", "PD": "v"}


def cronometrar(funcion, *args):
    inicio = time.perf_counter()
    resultado = funcion(*args)
    return resultado, time.perf_counter() - inicio


def ejecutar_todas(tareas, capacidad, limite_fb=LIMITE_FB, limite_dv=LIMITE_DV):
    """Ejecuta las 5 técnicas. Devuelve {clave: (prioridad, segundos)}.
    Una técnica que no se ejecuta por tamaño queda como (None, None)."""
    n = len(tareas)
    r = {}
    if n <= limite_fb:
        (p, _), t = cronometrar(fuerza_bruta_rec, tareas, capacidad, 0)
        r["FB"] = (p, t)
    else:
        r["FB"] = (None, None)
    (p, _, _), t = cronometrar(greedy, tareas, capacidad)
    r["G"] = (p, t)
    (p, _, _), t = cronometrar(backtracking, tareas, capacidad)
    r["BT"] = (p, t)
    if n <= limite_dv:
        (p, _, _), t = cronometrar(divide_y_venceras, tareas, capacidad)
        r["DV"] = (p, t)
    else:
        r["DV"] = (None, None)
    (p, _, _), t = cronometrar(programacion_dinamica, tareas, capacidad)
    r["PD"] = (p, t)

    # Las técnicas exactas deben coincidir entre sí
    exactas = {r[k][0] for k in ("FB", "BT", "DV", "PD") if r[k][0] is not None}
    assert len(exactas) == 1, f"Las técnicas exactas no coinciden: {r}"
    return r


def fmt_t(t):
    return "      -     " if t is None else f"{t:11.6f}s"


def fmt_p(p):
    return "    -" if p is None else f"{p:>5}"


# -------------------------------------------------------------
# 1. ARCHIVOS DE PRUEBA
# -------------------------------------------------------------
print("=" * 104)
print("1. ARCHIVOS DE PRUEBA  (prioridad obtenida | tiempo)")
print("=" * 104)
print(f"{'Archivo':<30}{'n':>5}{'T':>6} | {'FB':^19} | {'Greedy':^19} | "
      f"{'Backtracking':^19} | {'Divide y V.':^19} | {'P. dinámica':^19}")
print("-" * 140)

archivos = ["caso_contraejemplo_greedy.txt", "caso_pequeno.txt", "caso_mediano.txt",
            "caso_grande.txt", "caso_n100.txt", "caso_n1000.txt"]
resultados_archivos = {}

for nombre in archivos:
    ruta = os.path.join(DIR_DATOS, nombre)
    if not os.path.exists(ruta):
        print(f"Advertencia: no se encontró {ruta}")
        continue
    n, cap, tareas = cargar_caso(ruta)
    r = ejecutar_todas(tareas, cap)
    resultados_archivos[n] = r
    optimo = r["PD"][0]
    linea = f"{nombre:<30}{n:>5}{cap:>6}"
    for k in ("FB", "G", "BT", "DV", "PD"):
        linea += f" | {fmt_p(r[k][0])} {fmt_t(r[k][1])}"
    if r["G"][0] < optimo:
        linea += f"   greedy = {100 * r['G'][0] / optimo:.2f}% del óptimo"
    print(linea)
print("(-) no se ejecuta: tamaño inviable o modo --rapido")


# -------------------------------------------------------------
# 2. TABLA COMPARATIVA FINAL
# -------------------------------------------------------------
# Estimación de la fuerza bruta para n grande: su tiempo se DUPLICA por cada
# tarea adicional (O(2^n)), así que se extrapola desde el n más grande medido.
n_fb_max = max(n for n, r in resultados_archivos.items() if r["FB"][1] is not None)
t_fb_max = resultados_archivos[n_fb_max]["FB"][1]


def estimar_fb(n):
    segundos = t_fb_max * 2 ** (n - n_fb_max)
    anios = segundos / (3600 * 24 * 365)
    return f"inviable (~10^{len(str(int(anios))) - 1} años)"


complejidades = {
    "FB": ("O(2^n)", "O(n)", "Sí"),
    "G": ("O(n log n)", "O(n)", "No"),
    "BT": ("O(n·2^n) peor caso", "O(n)", "Sí"),
    "DV": ("O(n²) aquí; O(n·T²) peor", "O(n·T)", "Sí"),
    "PD": ("O(n·T)", "O(n·T)", "Sí"),
}

print("\n" + "=" * 104)
print("2. TABLA COMPARATIVA FINAL")
print("=" * 104)
print(f"{'Técnica':<23}{'Temporal':<27}{'Espacial':<10}{'¿Óptima?':<10}"
      f"{'Tiempo n=100':<26}{'Tiempo n=1000':<26}")
print("-" * 122)
for k in ("FB", "G", "BT", "DV", "PD"):
    temporal, espacial, optima = complejidades[k]
    celdas = []
    for n in (100, 1000):
        r = resultados_archivos.get(n)
        if r is None:
            celdas.append("-")
        elif r[k][1] is not None:
            celdas.append(f"{r[k][1]:.6f} s")
        elif k == "FB":
            celdas.append(estimar_fb(n))
        else:
            celdas.append("omitido (--rapido)")
    print(f"{NOMBRES[k]:<23}{temporal:<27}{espacial:<10}{optima:<10}"
          f"{celdas[0]:<26}{celdas[1]:<26}")
print(f"T = capacidad del servidor (n=100 -> T=775; n=1000 -> T=7636). "
      f"FB extrapolada desde n={n_fb_max} ({t_fb_max:.2f} s) duplicando por tarea.")


# -------------------------------------------------------------
# 3. CURVA DE TIEMPOS vs n (las 5 técnicas)
# -------------------------------------------------------------
print("\n" + "=" * 104)
print("3. CURVA DE TIEMPOS vs n  (instancias generadas con semilla 5000+n)")
print("=" * 104)
tamanios = [5, 9, 13, 17, 21, 25, 50, 100, 200, 400, 700, 1000]
curva = {k: ([], []) for k in NOMBRES}

for n in tamanios:
    capacidad, datos = generar(n, 5000 + n)
    tareas = [Tarea(*d) for d in datos]
    r = ejecutar_todas(tareas, capacidad, limite_fb=25)
    texto = f"n={n:5d} T={capacidad:5d} |"
    for k in ("FB", "G", "BT", "DV", "PD"):
        if r[k][1] is not None:
            curva[k][0].append(n)
            curva[k][1].append(max(r[k][1], 1e-7))
        texto += f" {k} {fmt_t(r[k][1])} |"
    print(texto)


# -------------------------------------------------------------
# 4. GRÁFICAS
# -------------------------------------------------------------
os.makedirs(DIR_DOCS, exist_ok=True)

# Figura 1: tiempo vs n de las 5 técnicas (log-log)
fig, ax = plt.subplots(figsize=(10, 6))
for k in ("FB", "BT", "DV", "PD", "G"):
    xs, ys = curva[k]
    ax.plot(xs, ys, marker=MARCAS[k], color=COLORES[k], lw=2, label=NOMBRES[k])
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_title("Tiempo de ejecución vs número de tareas (5 técnicas, escala log-log)")
ax.set_xlabel("Número de tareas (n)")
ax.set_ylabel("Tiempo (segundos)")
ax.grid(True, which="both", alpha=0.3)
ax.legend()
fig.tight_layout()
ruta1 = os.path.join(DIR_DOCS, "grafica_entrega3_tiempos.png")
fig.savefig(ruta1, dpi=150)

# Figura 2: barras con los tiempos en n=28, n=100 y n=1000
fig, axes = plt.subplots(1, 3, figsize=(14, 4.8))
for ax, n in zip(axes, (28, 100, 1000)):
    r = resultados_archivos.get(n)
    if r is None:
        continue
    claves = [k for k in ("FB", "G", "BT", "DV", "PD") if r[k][1] is not None]
    valores = [max(r[k][1], 1e-7) for k in claves]
    barras = ax.bar([NOMBRES[k].replace(" ", "\n", 1) for k in claves], valores,
                    color=[COLORES[k] for k in claves])
    ax.set_yscale("log")
    ax.set_title(f"n = {n}")
    ax.set_ylabel("Tiempo (s, log)")
    ax.tick_params(axis="x", labelsize=8)
    for b, v in zip(barras, valores):
        ax.text(b.get_x() + b.get_width() / 2, v, f"{v:.2g}s",
                ha="center", va="bottom", fontsize=8)
fig.suptitle("Tiempo real en los archivos de prueba (las técnicas omitidas son inviables)")
fig.tight_layout()
ruta2 = os.path.join(DIR_DOCS, "grafica_entrega3_barras.png")
fig.savefig(ruta2, dpi=150)

print(f"\nGráficas guardadas en:\n  {os.path.normpath(ruta1)}\n  {os.path.normpath(ruta2)}")
