"""
Entrega 3 - Solución por Divide y Vencerás

Idea: en vez de decidir tarea por tarea (como la fuerza bruta), se parte la
lista de tareas en dos mitades, se resuelve cada mitad por separado y luego
se combinan los resultados.

¿Qué devuelve cada subproblema?
    No basta con "la mejor prioridad de la mitad", porque al combinar no
    sabríamos cuánto tiempo deja libre para la otra mitad. Por eso cada
    subproblema devuelve su FRENTE DE PARETO: la lista de opciones
    (tiempo, prioridad) que vale la pena considerar. Una opción se descarta
    si existe otra que usa igual o menos tiempo y da igual o más prioridad
    (está "dominada"). Así el frente queda ordenado por tiempo y con
    prioridad estrictamente creciente.

Fases:
    1. DIVIDIR:  partir las tareas en dos mitades (izquierda / derecha).
    2. VENCER:   resolver recursivamente cada mitad -> dos frentes.
                 Caso base: una sola tarea -> {no tomarla, tomarla si cabe}.
    3. COMBINAR: sumar cada opción de la izquierda con cada opción de la
                 derecha que quepa en T y quedarse solo con las no dominadas.

Las dos mitades son INDEPENDIENTES: lo que se elija en una no cambia las
tareas de la otra; solo comparten la capacidad T, que se respeta al combinar.

Complejidad (S = tamaño máximo de un frente, S <= T + 1):
    Recurrencia: C(n) = 2 C(n/2) + O(S^2)
    Teorema Maestro: a = 2, b = 2, n^(log_b a) = n. Si el costo de combinar
    se acota por la constante S^2 (no crece con n), f(n) = O(n^(1-e)) ->
    Caso 1 -> C(n) = Theta(n) combinaciones -> O(n * T^2) en el peor caso.
    Sin la cota de capacidad el frente puede tener hasta 2^(n/2) opciones y
    el algoritmo es exponencial; la poda por dominancia y por T es lo que lo
    vuelve pseudo-polinomial.
    Espacial: O(n * S) para los frentes y la reconstrucción.

Garantiza la solución ÓPTIMA (nunca descarta una opción que pueda servir).
"""
import os
import sys
import time

from fuerza_bruta import cargar_caso

sys.setrecursionlimit(10000)

# Cada opción del frente es una tupla:
#   (tiempo, prioridad, origen)
# origen permite reconstruir qué tareas se eligieron sin copiar listas:
#   None                -> conjunto vacío
#   ("tarea", id)       -> una sola tarea (caso base)
#   ("par", op_izq, op_der) -> suma de una opción de cada mitad


def caso_base(tarea, capacidad):
    """Frente de una sola tarea: no tomarla, o tomarla si cabe."""
    frente = [(0, 0, None)]
    if tarea.tiempo <= capacidad:
        frente.append((tarea.tiempo, tarea.prioridad, ("tarea", tarea.id)))
    return frente


def combinar(izq, der, capacidad):
    """
    COMBINAR: mezcla dos frentes en uno.
    Prueba cada opción izquierda con cada opción derecha que quepa en T
    (der está ordenado por tiempo, así que se corta al primer 'no cabe').
    Luego deja solo las opciones no dominadas.
    """
    mejor_por_tiempo = {}
    for a in izq:
        limite = capacidad - a[0]
        for b in der:
            if b[0] > limite:
                break  # el resto de der ocupa todavía más tiempo
            tiempo = a[0] + b[0]
            prioridad = a[1] + b[1]
            actual = mejor_por_tiempo.get(tiempo)
            if actual is None or prioridad > actual[1]:
                mejor_por_tiempo[tiempo] = (tiempo, prioridad, ("par", a, b))

    # Filtrar dominadas: recorrer por tiempo creciente y quedarse solo con
    # las opciones que mejoran la prioridad de todas las anteriores.
    frente = []
    mejor_prioridad = -1
    for tiempo in sorted(mejor_por_tiempo):
        opcion = mejor_por_tiempo[tiempo]
        if opcion[1] > mejor_prioridad:
            frente.append(opcion)
            mejor_prioridad = opcion[1]
    return frente


def resolver_frente(tareas, inicio, fin, capacidad):
    """Devuelve el frente de Pareto de tareas[inicio:fin]."""
    if fin - inicio == 0:
        return [(0, 0, None)]
    if fin - inicio == 1:                       # caso base
        return caso_base(tareas[inicio], capacidad)

    medio = (inicio + fin) // 2                 # 1. DIVIDIR
    izq = resolver_frente(tareas, inicio, medio, capacidad)   # 2. VENCER
    der = resolver_frente(tareas, medio, fin, capacidad)
    return combinar(izq, der, capacidad)        # 3. COMBINAR


def reconstruir(origen):
    """Recorre los orígenes para recuperar los IDs de las tareas elegidas."""
    ids = []
    pila = [origen]
    while pila:
        o = pila.pop()
        if o is None:
            continue
        if o[0] == "tarea":
            ids.append(o[1])
        else:  # ("par", opcion_izq, opcion_der)
            pila.append(o[1][2])
            pila.append(o[2][2])
    return sorted(ids)


def divide_y_venceras(tareas, capacidad):
    """Retorna (prioridad_optima, ids_seleccionados, tamano_frente_final)."""
    frente = resolver_frente(tareas, 0, len(tareas), capacidad)
    # El frente tiene prioridad creciente: la última opción es la mejor.
    tiempo, prioridad, origen = frente[-1]
    return prioridad, reconstruir(origen), len(frente)


def resolver_divide_y_venceras(ruta_archivo):
    """Carga un caso, ejecuta D&V y mide el tiempo."""
    n, capacidad, tareas = cargar_caso(ruta_archivo)
    inicio = time.perf_counter()
    prioridad, seleccionadas, tam_frente = divide_y_venceras(tareas, capacidad)
    fin = time.perf_counter()
    return n, capacidad, prioridad, seleccionadas, tam_frente, (fin - inicio)


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
    print("          EJECUCION DIVIDE Y VENCERAS             ")
    print("==================================================\n")

    for nombre in archivos_prueba:
        ruta = os.path.join(dir_datos, nombre)
        if not os.path.exists(ruta):
            print(f"Error: No se encontró {nombre} en {dir_datos}\n")
            continue
        n, cap, p, sel, tam, t = resolver_divide_y_venceras(ruta)
        print(f"--- ARCHIVO: {nombre} ---")
        print(f"- Tareas totales (n): {n}")
        print(f"- Capacidad del servidor (T): {cap}")
        print(f"- Prioridad maxima (optima): {p}")
        if n <= 30:
            print(f"- Tareas seleccionadas (IDs): {sel}")
        else:
            print(f"- Tareas seleccionadas: {len(sel)}")
        print(f"- Opciones en el frente final: {tam}")
        print(f"- Tiempo de ejecucion: {t:.6f} segundos\n")

    print("==================================================")
