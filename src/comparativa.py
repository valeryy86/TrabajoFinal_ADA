import os
import random
import time
from fuerza_bruta import Tarea, cargar_caso, fuerza_bruta_rec
import matplotlib.pyplot as plt


def generar_caso(n, capacidad):
    """Genera tareas aleatorias para construir la curva de crecimiento."""
    return [
        Tarea(i, random.randint(5, 30), random.randint(10, 100))
        for i in range(1, n + 1)
    ]


def medir_tiempo_tareas(tareas, capacidad):
    """Mide el tiempo de ejecución en segundos."""
    inicio = time.time()
    fuerza_bruta_rec(tareas, capacidad, 0)
    fin = time.time()
    return fin - inicio


# -------------------------------------------------------------
# 1. EVALUACIÓN DE LOS 3 ARCHIVOS REALES (Para la tabla del PDF)
# -------------------------------------------------------------
print("=== 1. EVALUACIÓN DE ARCHIVOS DE PRUEBA ===")
archivos = [
    "../datos/caso_pequeno.txt",
    "../datos/caso_mediano.txt",
    "../datos/caso_grande.txt",
]

# Ajuste de ruta por si se ejecuta desde raíz o desde src/
if not os.path.exists("../datos") and os.path.exists("datos"):
    archivos = [path.replace("../", "") for path in archivos]

resultados_archivos = []

for ruta in archivos:
    if os.path.exists(ruta):
        n, cap, tareas = cargar_caso(ruta)
        t_eje = medir_tiempo_tareas(tareas, cap)
        p_max, _ = fuerza_bruta_rec(tareas, cap, 0)
        resultados_archivos.append((n, t_eje))
        print(
            f"Archivo: {os.path.basename(ruta)} | n = {n:2d} | Capacidad = {cap:3d} | Prioridad = {p_max} | Tiempo = {t_eje:.6f} s"
        )
    else:
        print(f"Advertencia: No se encontró el archivo {ruta}")


# -------------------------------------------------------------
# 2. EXPERIMENTO PROGRESIVO (Para trazar la curva del gráfico)
# -------------------------------------------------------------
print("\n=== 2. GENERANDO DATOS PARA LA GRÁFICA (Tiempo vs n) ===")
tamanios_n = list(range(5, 26, 2))  # n desde 5 hasta 25
tiempos_curva = []

for n in tamanios_n:
    capacidad = n * 10
    tareas = generar_caso(n, capacidad)
    t_eje = medir_tiempo_tareas(tareas, capacidad)
    tiempos_curva.append(t_eje)
    print(f"n = {n:2d} | Tiempo: {t_eje:.6f} s")


# -------------------------------------------------------------
# 3. GENERACIÓN DE LA GRÁFICA COMPARATIVA
# -------------------------------------------------------------
plt.figure(figsize=(9, 5))

# Trazar la curva exponencial general
plt.plot(
    tamanios_n,
    tiempos_curva,
    marker="o",
    color="red",
    linewidth=2,
    label="Fuerza Bruta O(2^n)",
)

# Destacar los 3 casos reales si fueron ejecutados
for n_file, t_file in resultados_archivos:
    plt.scatter(
        n_file,
        t_file,
        color="blue",
        s=100,
        zorder=5,
        label=f"Caso real (n={n_file})",
    )

plt.title("Fuerza Bruta: Tiempo de Ejecución vs Tamaño de Entrada (n)")
plt.xlabel("Número de Tareas (n)")
plt.ylabel("Tiempo de Ejecución (segundos)")
plt.grid(True)

# Evitar etiquetas duplicadas en la leyenda
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())

# Guardar la gráfica en docs/
ruta_guardado = (
    "../docs/grafica_entrega1.png"
    if os.path.exists("../docs")
    else "docs/grafica_entrega1.png"
)
plt.savefig(ruta_guardado)
print(f"\n¡Gráfica guardada con éxito en: {ruta_guardado}!")