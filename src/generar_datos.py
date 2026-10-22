"""
Generador reproducible de casos de prueba (Entrega 2).

Las tareas tienen la prioridad CORRELACIONADA con el tiempo
(p = t + ruido), que es lo realista (una tarea larga suele importar más)
y además es el tipo de instancia donde el greedy por densidad se equivoca
con más frecuencia. La capacidad T es el 45 % de la suma de tiempos, lo
que deja muchas combinaciones posibles (peor caso para la fuerza bruta).

Las semillas fijas se escogieron porque el greedy NO llega al óptimo en
esos casos, así la comparación entre técnicas es visible.

Uso (desde la raíz del repo o desde src/):
    python src/generar_datos.py
"""
import os
import random

CASOS = {
    # nombre_archivo: (n, semilla)
    "caso_mediano.txt": (20, 202),
    "caso_grande.txt": (28, 391),
}

FRACCION_CAPACIDAD = 0.45


def generar(n, semilla):
    rnd = random.Random(semilla)
    tareas = []
    for i in range(1, n + 1):
        tiempo = rnd.randint(5, 30)
        prioridad = max(1, tiempo + rnd.randint(-3, 12))
        tareas.append((i, tiempo, prioridad))
    capacidad = int(sum(t for _, t, _ in tareas) * FRACCION_CAPACIDAD)
    return capacidad, tareas


def escribir(ruta, capacidad, tareas):
    with open(ruta, "w") as f:
        f.write(f"{len(tareas)} {capacidad}\n")
        f.write("\n".join(f"{i} {t} {p}" for i, t, p in tareas))
        f.write("\n")


if __name__ == "__main__":
    dir_datos = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "datos")
    for nombre, (n, semilla) in CASOS.items():
        capacidad, tareas = generar(n, semilla)
        escribir(os.path.join(dir_datos, nombre), capacidad, tareas)
        print(f"{nombre}: n={n}, T={capacidad} (semilla {semilla})")
