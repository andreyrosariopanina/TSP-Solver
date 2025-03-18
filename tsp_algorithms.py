from sys import maxsize
from itertools import permutations

INF = 100000000000

def tsp(mask, pos, n, distance_matrix, dp, initial_pos, parent):
    if (mask  == (1<<n)-1):
        dp[pos][mask] = distance_matrix[pos][initial_pos] # caso base
        return distance_matrix[pos][initial_pos]
    
    if dp[pos][mask] != -1:
        return dp[pos][mask] # devolvemos el valor si ya ha sido calculado
    
    ans = INF
    best = -1
    for i in range(n):
        if ((mask & (1<<i)) == 0): # comprobamos que a ciudad no ha sido visitada
            cost = tsp((mask | (1<<i)), i, n, distance_matrix, dp, initial_pos, parent) + distance_matrix[pos][i] # transición
            if cost < ans:
                ans = cost
                best = i
        
    dp[pos][mask] = ans # guardamos el valor para después no tener que recalcularlo
    parent[pos][mask] = best 
    return ans

def get_path(parent, initial_pos, n):
    # Devuelve el camino óptimo
    path = [initial_pos]
    mask = (1 << initial_pos)
    current = initial_pos
    while True:
        next_pos = parent[current][mask]
        if next_pos == -1:
            break
        path.append(next_pos)
        mask = mask | (1 << next_pos)
        current = next_pos
    return path

def solve_dp(distance_matrix, initial_pos=0):
    n = len(distance_matrix)
    dp = [[-1 for j in range((1<<n))] for i in range(n)]
    parent = [[-1 for _ in range(1 << n)] for _ in range(n)]
    min_cost = tsp((1<<initial_pos), initial_pos, n, distance_matrix, dp, initial_pos, parent)
    path = get_path(parent, initial_pos, n)
    return path, min_cost


def brute_force(distance_matrix, initial_pos=0):
    n = len(distance_matrix) # Numero de elementos/ciudades a tener en cuenta
    vertices = [i for i in range(n) if i != initial_pos]  # Elementos restantes distintos del inicial
    min_cost = maxsize  # Busca el valor minimo de los recogidos 
    best_path = []  
    
    for perm in permutations(vertices):  
        current_cost = 0
        k = initial_pos  
        current_path = [initial_pos]  # Iniciar con la posición inicial
        
        for j in perm:
            current_cost += distance_matrix[k][j]  
            current_path.append(j)
            k = j
        
        current_cost += distance_matrix[k][initial_pos]  # Volver al inicio
      
        if current_cost < min_cost:  # Busca el recorrido que menos cueste
            min_cost = current_cost
            best_path = current_path[:]
    
    return best_path, min_cost