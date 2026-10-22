"""
Entrega 2 - Solución con Backtracking (con poda)

Explora el mismo árbol binario de decisiones que la fuerza bruta
(incluir / excluir cada tarea) pero corta ramas que no pueden llevar a una
solución válida o mejor que la ya encontrada.

Podas utilizadas:
    1. Poda por factibilidad (capacidad): no se abre la rama "incluir" si la
       tarea no cabe en la capacidad restante.
    2. Poda por cota (optimalidad): antes de seguir bajando se calcula una
       cota superior optimista de lo que todavía se puede ganar: se llenan
       las horas restantes con las tareas que faltan en orden de densidad,
       permitiendo tomar una FRACCIÓN de la última (relajación fraccional).
       Si  prioridad_actual + cota <= mejor_encontrada, la rama no puede
       mejorar el resultado y se descarta completa.
    3. Mejor solución inicial: se arranca con el resultado del greedy, de
       modo que la poda 2 empieza a cortar desde la raíz.

Complejidad:
    - Peor caso temporal: O(n * 2^n) (si ninguna poda actúa se visita todo
      el árbol y cada cota cuesta O(n)); en la práctica O(2^n) nodos.
    - Caso promedio (con poda): muchísimo menor; se mide contando nodos.
    - Espacial: O(n) (profundidad de recursión + solución actual).

Garantiza la solución ÓPTIMA (solo descarta ramas que no pueden mejorar).
"""
import os
import sys
import time

from fuerza_bruta import cargar_caso
from greedy import greedy

sys.setrecursionlimit(10000)


def backtracking(tareas, capacidad, usar_cota=True):
    """
    Retorna (prioridad_optima, ids_seleccionados, nodos_visitados).

    usar_cota=False deja solo la poda por capacidad (sirve para medir
    cuánto aporta la poda por cota).
    """
    # Ordenar por densidad: hace la cota más ajustada y encuentra buenas
    # soluciones temprano.
    orden = sorted(tareas, key=lambda t: t.prioridad / t.tiempo, reverse=True)
    n = len(orden)

    # Mejor solución conocida al inicio = la del greedy
    if usar_cota:
        p_greedy, ids_greedy, _ = greedy(tareas, capacidad)
        mejor = {"prioridad": p_greedy, "ids": list(ids_greedy)}
    else:
        mejor = {"prioridad": 0, "ids": []}

    nodos = [0]
    actual = []

    def cota_superior(indice, cap_restante):
        """Relajación fraccional sobre las tareas indice..n-1  -> O(n)."""
        cota = 0.0
        for k in range(indice, n):
            t = orden[k]
            if t.tiempo <= cap_restante:
                cap_restante -= t.tiempo
                cota += t.prioridad
            else:
                cota += t.prioridad * cap_restante / t.tiempo
                break
        return cota

    def explorar(indice, cap_restante, prioridad_actual):
        nodos[0] += 1

        # Registrar si la solución parcial es la mejor vista
        if prioridad_actual > mejor["prioridad"]:
            mejor["prioridad"] = prioridad_actual
            mejor["ids"] = list(actual)

        if indice == n or cap_restante == 0:
            return

        # PODA 2: la rama no puede superar a la mejor conocida
        if usar_cota and prioridad_actual + cota_superior(indice, cap_restante) <= mejor["prioridad"]:
            return

        tarea = orden[indice]

        # Rama INCLUIR (PODA 1: solo si cabe)
        if tarea.tiempo <= cap_restante:
            actual.append(tarea.id)
            explorar(indice + 1, cap_restante - tarea.tiempo,
                     prioridad_actual + tarea.prioridad)
            actual.pop()  # deshacer la decisión (backtrack)

        # Rama EXCLUIR
        explorar(indice + 1, cap_restante, prioridad_actual)

    explorar(0, capacidad, 0)
    return mejor["prioridad"], sorted(mejor["ids"]), nodos[0]


def resolver_backtracking(ruta_archivo, usar_cota=True):
    """Carga un caso, ejecuta backtracking y mide el tiempo."""
    n, capacidad, tareas = cargar_caso(ruta_archivo)

    inicio = time.perf_counter()
    prioridad, seleccionadas, nodos = backtracking(tareas, capacidad, usar_cota)
    fin = time.perf_counter()

    return n, capacidad, prioridad, seleccionadas, nodos, (fin - inicio)


if __name__ == "__main__":
    dir_actual = os.path.dirname(os.path.abspath(__file__))
    dir_datos = os.path.join(dir_actual, "..", "datos")

    archivos_prueba = [
        "caso_pequeno.txt",
        "caso_mediano.txt",
        "caso_grande.txt",
        "caso_contraejemplo_greedy.txt",
    ]

    print("==================================================")
    print("      EJECUCION BACKTRACKING (poda + cota)        ")
    print("==================================================\n")

    for nombre in archivos_prueba:
        ruta = os.path.join(dir_datos, nombre)
        if not os.path.exists(ruta):
            print(f"Error: No se encontró {nombre} en {dir_datos}\n")
            continue

        n, cap, p, sel, nodos, t = resolver_backtracking(ruta)
        print(f"--- ARCHIVO: {nombre} ---")
        print(f"- Tareas totales (n): {n}")
        print(f"- Capacidad del servidor (T): {cap}")
        print(f"- Prioridad maxima (optima): {p}")
        print(f"- Tareas seleccionadas (IDs): {sel}")
        print(f"- Nodos visitados: {nodos:,} de {2 ** (n + 1) - 1:,} posibles")
        print(f"- Tiempo de ejecucion: {t:.6f} segundos\n")

    print("==================================================")
