import maps
import tsp_algorithms
import os

def get_cities():
    ciudades = []
    print("Introduce las ciudades que deseas considerar (escribe 'fin' para terminar):")
    while True:
        ciudad = input("Ciudad: ")
        if ciudad.lower() == 'fin':
            break
        ciudades.append(ciudad)
            
    if len(ciudades) < 2:
        print("Debes ingresar al menos dos ciudades.")
        return None
    
    return ciudades
    
def show_results(permutation, distance, cities):
    print(f"El camino mínimo tiene coste: {distance} km\n")
    print("El camino de mínimo coste es:")
    for i in range(len(permutation)):
        print(f"{i+1}: {cities[permutation[i]]}")

def show_menu():
    print("¿Qué desea hacer?")
    print("1) Ingresar ciudades")
    print("2) Resolver problema fuerza bruta")
    print("3) Resolver problema DP")
    print("4) Salir")
    option = input("Ingrese una opción: ")
    while not option.isdigit():
        print("Debe ingresar una opción corrrecta")
        option = input("Ingrese una opción: ")
    return option

def main():
    cities = None
    distance_matrix = None
    clear = lambda: os.system('clear') #cls windows
    while True:
        print("\n----------Resolución del problema TSP----------\n")
        option = show_menu()
        clear()
        if option == '1':
            cities = get_cities()
            if cities != None:
                distance_matrix = maps.obtener_matriz_distancias(cities)
                
        elif option == '2':
            if distance_matrix != None:
                permutation, distance = tsp_algorithms.brute_force(distance_matrix)
                show_results(permutation, distance, cities)
            else:
                print("Debe introducir ciudades previamente")

        elif option == '3':
            if distance_matrix != None:
                permutation, distance = tsp_algorithms.brute_force(distance_matrix)
                show_results(permutation, distance, cities)
            else:
                print("Debe introducir ciudades previamente")

        elif option == '4':
            print("Gracias por usar el programa")
            break

        else:
            print("Debe introducir una opción válida")
        
        input("\nPresione Enter para continuar...") 
        clear()
main()