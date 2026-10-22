"""
Entrega 2 - Solución Greedy (voraz)

Problema: seleccionar un subconjunto de tareas para un servidor con capacidad
de tiempo T, maximizando la prioridad total (mochila 0/1).

Decisión local óptima: tomar primero la tarea con mayor "densidad"
prioridad / tiempo, es decir, la que más prioridad entrega por cada unidad
de tiempo de servidor que consume. Si cabe en la capacidad restante se
incluye; si no, se descarta y se pasa a la siguiente. Nunca se reconsidera
una decisión ya tomada.

Complejidad:
    - Temporal: O(n log n)  (ordenar domina; el recorrido es O(n))
    - Espacial: O(n)        (lista ordenada + lista de seleccionadas)

NO garantiza el óptimo para la versión 0/1 (ver contraejemplo en
datos/caso_contraejemplo_greedy.txt).
"""
import os
import time

from fuerza_bruta import cargar_caso


def greedy(tareas, capacidad):
    """Retorna (prioridad_total, ids_seleccionados, tiempo_usado)."""
    # 1. Ordenar por densidad prioridad/tiempo de mayor a menor -> O(n log n)
    ordenadas = sorted(tareas, key=lambda t: t.prioridad / t.tiempo, reverse=True)

    prioridad_total = 0
    tiempo_usado = 0
    seleccionadas = []

    # 2. Recorrer una sola vez tomando lo que quepa -> O(n)
    for tarea in ordenadas:
        if tiempo_usado + tarea.tiempo <= capacidad:
            seleccionadas.append(tarea.id)
            tiempo_usado += tarea.tiempo
            prioridad_total += tarea.prioridad

    return prioridad_total, sorted(seleccionadas), tiempo_usado


def resolver_greedy(ruta_archivo):
    """Carga un caso, ejecuta el greedy y mide el tiempo."""
    n, capacidad, tareas = cargar_caso(ruta_archivo)

    inicio = time.perf_counter()
    prioridad, seleccionadas, tiempo_usado = greedy(tareas, capacidad)
    fin = time.perf_counter()

    return n, capacidad, prioridad, seleccionadas, tiempo_usado, (fin - inicio)


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
    print("        EJECUCION GREEDY (prioridad/tiempo)       ")
    print("==================================================\n")

    for nombre in archivos_prueba:
        ruta = os.path.join(dir_datos, nombre)
        if not os.path.exists(ruta):
            print(f"Error: No se encontró {nombre} en {dir_datos}\n")
            continue

        n, cap, p, sel, usado, t = resolver_greedy(ruta)
        print(f"--- ARCHIVO: {nombre} ---")
        print(f"- Tareas totales (n): {n}")
        print(f"- Capacidad del servidor (T): {cap}")
        print(f"- Prioridad obtenida: {p}")
        print(f"- Tiempo usado: {usado}/{cap}")
        print(f"- Tareas seleccionadas (IDs): {sel}")
        print(f"- Tiempo de ejecucion: {t:.6f} segundos\n")

    print("==================================================")
