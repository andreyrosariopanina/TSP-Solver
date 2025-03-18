import googlemaps

#API_KEY = 

def obtener_matriz_distancias(ciudades):
    gmaps = googlemaps.Client(key=API_KEY)
    matriz_distancias = [[0 for _ in range(len(ciudades))] for _ in range(len(ciudades))]
    
    for i in range(len(ciudades)):
        for j in range(i + 1, len(ciudades)):
            origen = ciudades[i]
            destino = ciudades[j]
            
            distancia = gmaps.distance_matrix(origen, destino, mode="driving")
            
            if distancia["rows"][0]["elements"][0]["status"] == "OK":
                distancia_km = distancia["rows"][0]["elements"][0]["distance"]["value"] / 1000  # Convertir a km
                matriz_distancias[i][j] = distancia_km
                matriz_distancias[j][i] = distancia_km  # Forzar simetría
            else:
                raise ValueError(f"No se puede calcular la distancia entre {origen} y {destino}. Verifica las ciudades ingresadas.")
    
    return matriz_distancias
