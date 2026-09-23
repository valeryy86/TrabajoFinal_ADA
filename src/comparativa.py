import random
import time
import matplotlib.pyplot as plt
from fuerza_bruta import resolver_fuerza_bruta
from tarea import Tarea


def generar_caso(n, capacidad):
    return [
        Tarea(i, random.randint(5, 30), random.randint(10, 100))
        for i in range(1, n + 1)
    ]


tamanios = list(range(5, 25, 2))
tiempos = []

for n in tamanios:
    capacidad = n * 10
    tareas = generar_caso(n, capacidad)
    _, _, t_eje = resolver_fuerza_bruta(tareas, capacidad)
    tiempos.append(t_eje)

plt.figure(figsize=(8, 5))
plt.plot(tamanios, tiempos, marker="o", color="red", label="Fuerza Bruta O(2^n)")
plt.title("Tiempo de Ejecución vs Tamaño de Entrada (n)")
plt.xlabel("Número de Tareas (n)")
plt.ylabel("Tiempo (segundos)")
plt.grid(True)
plt.legend()
plt.savefig("docs/grafica_entrega1.png")
print("Gráfica generada en docs/grafica_entrega1.png")