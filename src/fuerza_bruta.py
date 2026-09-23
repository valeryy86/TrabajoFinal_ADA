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
    # Caso base: no quedan más tareas por evaluar o no hay capacidad restante
    if indice == len(tareas) or capacidad <= 0:
        return 0, []

    tarea_actual = tareas[indice]

    # Opción 1: No incluir la tarea actual en la solución
    p_excluir, comb_excluir = fuerza_bruta_rec(tareas, capacidad, indice + 1)

    # Opción 2: Incluir la tarea actual si su tiempo no excede la capacidad disponible
    if tarea_actual.tiempo <= capacidad:
        p_incluir, comb_incluir = fuerza_bruta_rec(
            tareas, capacidad - tarea_actual.tiempo, indice + 1
        )
        p_incluir += tarea_actual.prioridad

        # Retornar la combinación de mayor valor/prioridad
        if p_incluir > p_excluir:
            return p_incluir, [tarea_actual.id] + comb_incluir

    return p_excluir, comb_excluir


def resolver_fuerza_bruta(ruta_archivo):
    """Función principal para cargar datos y medir la ejecución."""
    n, capacidad, tareas = cargar_caso(ruta_archivo)

    inicio = time.time()
    prioridad_maxima, seleccionadas = fuerza_bruta_rec(tareas, capacidad, 0)
    fin = time.time()

    return prioridad_maxima, seleccionadas, (fin - inicio)


if __name__ == "__main__":
    # Permite ejecutarlo directamente indicando la ruta del caso de prueba
    ruta = (
        sys.argv[1] if len(sys.argv) > 1 else "../datos/caso_pequeno.txt"
    )
    p_max, tareas_sel, t_ejec = resolver_fuerza_bruta(ruta)

    print("=== EJECUCIÓN FUERZA BRUTA ===")
    print(f"Archivo: {ruta}")
    print(f"Prioridad Máxima: {p_max}")
    print(f"Tareas Seleccionadas (IDs): {tareas_sel}")
    print(f"Tiempo de Ejecución: {t_ejec:.6f} segundos")