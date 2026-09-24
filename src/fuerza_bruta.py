import os
import sys
import time


class Tarea:

    def __init__(self, id_tarea, tiempo, prioridad):
        self.id = id_tarea
        self.tiempo = tiempo
        self.prioridad = prioridad


def cargar_caso(ruta_archivo):
    """Lee un archivo de entrada con el formato especificado."""
    with open(ruta_archivo, "r") as f:
        lineas = [linea.strip() for linea in f.readlines() if linea.strip()]

    n, capacidad = map(int, lineas[0].split())
    tareas = []
    for linea in lineas[1:]:
        id_t, t, p = map(int, linea.split())
        tareas.append(Tarea(id_t, t, p))

    return n, capacidad, tareas


def fuerza_bruta_rec(tareas, capacidad, indice):
    """Algoritmo recursivo que evalúa todas las combinaciones posibles (2^n)."""
    if indice == len(tareas) or capacidad <= 0:
        return 0, []

    tarea_actual = tareas[indice]

    # Opción 1: No incluir la tarea actual
    p_excluir, comb_excluir = fuerza_bruta_rec(tareas, capacidad, indice + 1)

    # Opción 2: Incluir la tarea actual si cabe
    if tarea_actual.tiempo <= capacidad:
        p_incluir, comb_incluir = fuerza_bruta_rec(
            tareas, capacidad - tarea_actual.tiempo, indice + 1
        )
        p_incluir += tarea_actual.prioridad

        if p_incluir > p_excluir:
            return p_incluir, [tarea_actual.id] + comb_incluir

    return p_excluir, comb_excluir


def resolver_fuerza_bruta(ruta_archivo):
    """Función principal para cargar datos y medir la ejecución."""
    n, capacidad, tareas = cargar_caso(ruta_archivo)

    inicio = time.time()
    prioridad_maxima, seleccionadas = fuerza_bruta_rec(tareas, capacidad, 0)
    fin = time.time()

    return n, capacidad, prioridad_maxima, seleccionadas, (fin - inicio)


if __name__ == "__main__":
    # Obtiene la ruta absoluta de la carpeta datos/ independiente de dónde ejecutes la terminal
    dir_actual = os.path.dirname(os.path.abspath(__file__))
    dir_datos = os.path.join(dir_actual, "..", "datos")

    # Lista con los 3 archivos de prueba
    archivos_prueba = [
        "caso_pequeno.txt",
        "caso_mediano.txt",
        "caso_grande.txt",
    ]

    print("==================================================")
    print("      EJECUCION DE FUERZA BRUTA DE LOS 3 CASOS         ")
    print("==================================================\n")

    for nombre_archivo in archivos_prueba:
        ruta_completa = os.path.join(dir_datos, nombre_archivo)

        if os.path.exists(ruta_completa):
            n, cap, p_max, tareas_sel, t_ejec = resolver_fuerza_bruta(
                ruta_completa
            )

            print(f"--- ARCHIVO: {nombre_archivo} ---")
            print(f"- Tareas totales (n): {n}")
            print(f"- Capacidad del servidor (T): {cap}")
            print(f"- Prioridad Maxima Obtenida: {p_max}")
            print(f"- Tareas Seleccionadas (IDs): {tareas_sel}")
            print(f"- Tiempo de Ejecucion: {t_ejec:.6f} segundos\n")
        else:
            print(
                f"Error: No se encontró el archivo {nombre_archivo} en {dir_datos}\n"
            )

    print("==================================================")