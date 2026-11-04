"""
Entrega 3 - Solución por Programación Dinámica

Observación clave: el problema tiene SUBPROBLEMAS SUPERPUESTOS. Muchas
ramas del árbol de la fuerza bruta terminan preguntando exactamente lo
mismo: "con las tareas i..n y c unidades de tiempo libres, ¿cuál es la
mejor prioridad?". La fuerza bruta lo recalcula cada vez; la programación
dinámica lo calcula UNA sola vez y lo guarda en una tabla.

Definición del subproblema:
    mejor[i][c] = máxima prioridad usando solo las primeras i tareas
                  con una capacidad de c unidades de tiempo.

Recurrencia (para la tarea i, con tiempo t_i y prioridad p_i):
    mejor[i][c] = mejor[i-1][c]                          si t_i > c
    mejor[i][c] = max( mejor[i-1][c],                    (no tomarla)
                       mejor[i-1][c - t_i] + p_i )       (tomarla)
Casos base: mejor[0][c] = 0 para todo c.
Respuesta:  mejor[n][T].

Implementación: se guarda solo la fila actual de valores (lista de T+1
números) recorriendo c de mayor a menor, para no usar la tarea dos veces.
Para reconstruir QUÉ tareas se eligieron se guarda, por cada tarea, una
fila de 0/1 (bytearray) que dice si convino tomarla con capacidad c.

Complejidad:
    Temporal: O(n * T)  -> n tareas x (T + 1) capacidades, O(1) cada celda.
    Espacial: O(n * T)  bits/bytes para reconstruir la solución
              (O(T) si solo se quisiera el valor óptimo).
    Es PSEUDO-POLINOMIAL: polinomial en n y en el VALOR de T, no en la
    cantidad de bits de T. Si T fuera enorme (ej. 10^12) sería inviable.

Garantiza la solución ÓPTIMA.
"""
import os
import time

from fuerza_bruta import cargar_caso


def programacion_dinamica(tareas, capacidad):
    """Retorna (prioridad_optima, ids_seleccionados, celdas_calculadas)."""
    mejor = [0] * (capacidad + 1)   # fila i-1 / i de la tabla
    tomada = []                     # tomada[i][c] = 1 si se tomó la tarea i

    for tarea in tareas:
        t, p = tarea.tiempo, tarea.prioridad
        fila = bytearray(capacidad + 1)
        # c de mayor a menor: mejor[c - t] todavía es el valor SIN esta tarea
        for c in range(capacidad, t - 1, -1):
            con_tarea = mejor[c - t] + p
            if con_tarea > mejor[c]:
                mejor[c] = con_tarea
                fila[c] = 1
        tomada.append(fila)

    # Reconstrucción: caminar la tabla desde la última tarea hacia atrás
    seleccionadas = []
    c = capacidad
    for i in range(len(tareas) - 1, -1, -1):
        if tomada[i][c]:
            seleccionadas.append(tareas[i].id)
            c -= tareas[i].tiempo

    celdas = len(tareas) * (capacidad + 1)
    return mejor[capacidad], sorted(seleccionadas), celdas


def resolver_dinamica(ruta_archivo):
    """Carga un caso, ejecuta PD y mide el tiempo."""
    n, capacidad, tareas = cargar_caso(ruta_archivo)
    inicio = time.perf_counter()
    prioridad, seleccionadas, celdas = programacion_dinamica(tareas, capacidad)
    fin = time.perf_counter()
    return n, capacidad, prioridad, seleccionadas, celdas, (fin - inicio)


if __name__ == "__main__":
    dir_actual = os.path.dirname(os.path.abspath(__file__))
    dir_datos = os.path.join(dir_actual, "..", "datos")

    archivos_prueba = [
        "caso_contraejemplo_greedy.txt",
        "caso_pequeno.txt",
        "caso_mediano.txt",
        "caso_grande.txt",
        "caso_n100.txt",
        "caso_n1000.txt",
    ]

    print("==================================================")
    print("        EJECUCION PROGRAMACION DINAMICA           ")
    print("==================================================\n")

    for nombre in archivos_prueba:
        ruta = os.path.join(dir_datos, nombre)
        if not os.path.exists(ruta):
            print(f"Error: No se encontró {nombre} en {dir_datos}\n")
            continue
        n, cap, p, sel, celdas, t = resolver_dinamica(ruta)
        print(f"--- ARCHIVO: {nombre} ---")
        print(f"- Tareas totales (n): {n}")
        print(f"- Capacidad del servidor (T): {cap}")
        print(f"- Prioridad maxima (optima): {p}")
        if n <= 30:
            print(f"- Tareas seleccionadas (IDs): {sel}")
        else:
            print(f"- Tareas seleccionadas: {len(sel)}")
        print(f"- Celdas de la tabla (n x (T+1)): {celdas:,}")
        print(f"- Tiempo de ejecucion: {t:.6f} segundos\n")

    print("==================================================")
