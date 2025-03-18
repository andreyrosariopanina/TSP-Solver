import numpy as np
from python_tsp.exact import solve_tsp_dynamic_programming
from python_tsp.heuristics import solve_tsp_local_search
import tsp_algorithms
import random
import os
import tsplib95
import time
import matplotlib.pyplot as plt
from tabulate import tabulate

def plot_avg_time_by_size(d):
    # Generar la gráfica del tiempo medio por tamaño de la muestra
    plt.figure(figsize=(10, 6))
    for algo, results in d.items():
        size_to_times = {} 
        for size, t in results:
            if size not in size_to_times:
                size_to_times[size] = []  
            size_to_times[size].append(t)
        sizes = sorted(size_to_times.keys())
        avg_times = [np.mean(size_to_times[size]) for size in sizes]
        plt.plot(sizes, avg_times, marker='o', label=algo)
    
    plt.title("Tiempo medio de ejecución por número de ciudades", fontsize=16)
    plt.xlabel("Número de ciudades", fontsize=14)
    plt.ylabel("Tiempo medio (s)", fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.yscale('log') 
    plt.tight_layout()
    plt.legend(title="Algoritmos", fontsize=12)
    plt.savefig("tsp_avg_time_by_size.png")
    
def mostrar_tabla_por_tamano(d):
    # Mostrar por consola la tabla del tiempo medio por tamaño de la muestra
    todos_los_tamanos = sorted({size for resultados in d.values() for size, _ in resultados})

    tiempos_por_tamano = {n: {algoritmo: [] for algoritmo in d} for n in todos_los_tamanos}
    
    for algoritmo, resultados in d.items():
        for n, tiempo in resultados:
            tiempos_por_tamano[n][algoritmo].append(tiempo)
    
    headers = ["Tamaño (n)"] + list(d.keys())
    tabla = []
    for n in todos_los_tamanos:
        fila = [n]
        for algoritmo in d.keys():
            tiempos = tiempos_por_tamano[n][algoritmo]
            if tiempos:
                media = round(np.mean(tiempos), 5)
                fila.append(media)
            else:
                fila.append("-")
        tabla.append(fila)

    print("\n========= Tiempo medio por tamaño y algoritmo =========")
    print(tabulate(tabla, headers=headers, tablefmt="fancy_grid"))

def parse_file(folder_path, filename, n):
    # Obtener la matriz de distancia dado un archivo .tsp
    file_path = os.path.join(folder_path, filename)
    print(f"Procesando archivo: {filename}")
    try:
        problem = tsplib95.load(file_path)
        nodes = list(problem.get_nodes())
        if len(nodes) >= n:
            nodes = random.sample(nodes, n)
        else:
            n = len(nodes)

        distance_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i != j:
                    distance_matrix[i][j] = problem.get_weight(nodes[i], nodes[j])
    
        return distance_matrix
    except Exception as e:
        print(f"Error {filename}: {e}")
        return None

def test_tsplib(folder_path, max_nodes=20):
    # Comprobar la precisión y el tiempo de los algoritmos
    algorithms = {
        'Programación dinámica': tsp_algorithms.solve_dp,
        'Heuristic': solve_tsp_local_search,
        'Fuerza fruta': tsp_algorithms.brute_force, 
        'tsp-dp':solve_tsp_dynamic_programming
    }
    d = {algorithm : [] for algorithm in algorithms}
    errors = 0
    for filename in os.listdir(folder_path):
        if filename.endswith('.tsp'):
            n = np.random.randint(1, max_nodes)
            distance_matrix = parse_file(folder_path, filename, n)
            if distance_matrix is not None:
                distances = []
                for algo_name, algorithm in algorithms.items():
                    start = time.time()
                    permutation, distance = algorithm(distance_matrix)
                    time_taken = time.time()-start
                    if algo_name != 'Heuristic':
                        distances.append(distance)
                    d[algo_name].append((n, time_taken))
                    print(f"Algoritmo {algo_name}: {n} vértices, Tiempo: {time_taken}")

                # Comprobamos que todas las distancias de los algoritmos exactos son iguales
                if distances.count(distances[0]) != len(distances):
                    print("ERROR", distance_matrix)
                    error += 1
    return d, errors

if __name__ == '__main__':
    d, errors = test_tsplib('tsplib', 10)
    print(errors)
    plot_avg_time_by_size(d)
    mostrar_tabla_por_tamano(d)
   