class GrafoLogistica:
    def __init__(self, archivo):
        self.grafo = {}
        self.leer_archivo(archivo)

    def leer_archivo(self, archivo):
        with open(archivo, 'r') as file:
            next(file)  # Saltar la primera línea (encabezado)
            for line in file:
                ciudad1, ciudad2, tiempo_normal, tiempo_lluvia, tiempo_nieve, tiempo_tormenta = line.strip().split()
                tiempo_normal, tiempo_lluvia, tiempo_nieve, tiempo_tormenta = map(int, [tiempo_normal, tiempo_lluvia, tiempo_nieve, tiempo_tormenta])
                self.agregar_conexion(ciudad1, ciudad2, tiempo_normal, tiempo_lluvia, tiempo_nieve, tiempo_tormenta)

    def agregar_conexion(self, ciudad1, ciudad2, tiempo_normal, tiempo_lluvia, tiempo_nieve, tiempo_tormenta):
        if ciudad1 not in self.grafo:
            self.grafo[ciudad1] = {}
        if ciudad2 not in self.grafo:
            self.grafo[ciudad2] = {}

        self.grafo[ciudad1][ciudad2] = {'normal': tiempo_normal, 'lluvia': tiempo_lluvia, 'nieve': tiempo_nieve, 'tormenta': tiempo_tormenta}

    def ruta_mas_corta(self, ciudad_origen, ciudad_destino):
        n = len(self.grafo)
        distancias = [[float('inf')] * n for _ in range(n)]
        intermedios = [[None] * n for _ in range(n)]

        for i in range(n):
            distancias[i][i] = 0
            for j in self.grafo.get(list(self.grafo.keys())[i], {}):
                distancias[i][list(self.grafo.keys()).index(j)] = self.grafo[list(self.grafo.keys())[i]][j]['normal']
                intermedios[i][list(self.grafo.keys()).index(j)] = list(self.grafo.keys())[i]

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if distancias[i][j] > distancias[i][k] + distancias[k][j]:
                        distancias[i][j] = distancias[i][k] + distancias[k][j]
                        intermedios[i][j] = intermedios[k][j]

        indice_origen = list(self.grafo.keys()).index(ciudad_origen)
        indice_destino = list(self.grafo.keys()).index(ciudad_destino)
        ruta = [ciudad_origen]
        while indice_origen != indice_destino:
            siguiente_ciudad = intermedios[indice_origen][indice_destino]
            if siguiente_ciudad in ruta:
                break
            ruta.append(siguiente_ciudad)
            indice_destino = list(self.grafo.keys()).index(siguiente_ciudad)

        # Agregar la ciudad de destino si no está presente en la ruta
        if ciudad_destino not in ruta:
            ruta.append(ciudad_destino)

        return ruta

    def centro_del_grafo(self):
        n = len(self.grafo)
        distancias = [[float('inf')] * n for _ in range(n)]

        for i in range(n):
            for j in range(n):
                if i == j:
                    distancias[i][j] = 0
                elif self.grafo.get(list(self.grafo.keys())[i], {}).get(list(self.grafo.keys())[j]):
                    distancias[i][j] = self.grafo[list(self.grafo.keys())[i]][list(self.grafo.keys())[j]]['normal']

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if distancias[i][j] > distancias[i][k] + distancias[k][j]:
                        distancias[i][j] = distancias[i][k] + distancias[k][j]

        sumas_distancias = [sum(distancias[i]) for i in range(n)]
        indice_centro = sumas_distancias.index(min(sumas_distancias))
        return list(self.grafo.keys())[indice_centro]

def menu():
    print("Opciones:")
    print("1. Calcular ruta más corta entre dos ciudades.")
    print("2. Mostrar ciudad en el centro del grafo.")
    print("3. Modificar el grafo.")
    print("4. Salir")

    while True:
        opcion = input("Seleccione una opción (1-4): ")
        if opcion in ["1", "2", "3", "4"]:
            return int(opcion)
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

def mostrar_ciudades_disponibles(grafo):
    ciudades = list(grafo.keys())
    print("Ciudades disponibles:")
    for idx, ciudad in enumerate(ciudades, start=1):
        print(f"{idx}. {ciudad}")
    return ciudades

def seleccionar_ciudad(ciudades):
    while True:
        try:
            opcion = int(input("Seleccione el número de la ciudad: "))
            if 1 <= opcion <= len(ciudades):
                return ciudades[opcion - 1]
            else:
                print("Número de ciudad inválido. Por favor, seleccione un número válido.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")

def main():
    grafo_logistica = GrafoLogistica("logistica.txt")
    while True:
        opcion = menu()

        if opcion == 1:
            ciudades = mostrar_ciudades_disponibles(grafo_logistica.grafo)
            ciudad_origen = seleccionar_ciudad(ciudades)
            ciudad_destino = seleccionar_ciudad(ciudades)
            ruta = grafo_logistica.ruta_mas_corta(ciudad_origen, ciudad_destino)
            print(f"La ruta más corta entre {ciudad_origen} y {ciudad_destino} es:")
            for idx, ciudad in enumerate(ruta):
                if idx != 0 and idx != len(ruta) - 1:
                    print(f"{ciudad} (ciudad intermedia)")
                else:
                    print(ciudad)
            print(f"La duración total del viaje es: {sum(grafo_logistica.grafo[ruta[i]][ruta[i + 1]]['normal'] for i in range(len(ruta) - 1))} horas\n")

        elif opcion == 2:
            centro = grafo_logistica.centro_del_grafo()
            print(f"La ciudad en el centro del grafo es: {centro}")

        elif opcion == 3:
            print("Opciones de modificación:")
            print("a. Interrupción de tráfico entre un par de ciudades.")
            print("b. Establecer una nueva conexión entre ciudades.")
            print("c. Indicar el clima entre un par de ciudades.")

            modificacion = input("Seleccione la opción de modificación (a, b, c): ")
            if modificacion == "a":
                ciudad1 = input("Ingrese el nombre de la primera ciudad: ")
                ciudad2 = input("Ingrese el nombre de la segunda ciudad: ")
                if ciudad1 in grafo_logistica.grafo and ciudad2 in grafo_logistica.grafo[ciudad1]:
                    del grafo_logistica.grafo[ciudad1][ciudad2]
                    print(f"Se ha interrumpido el tráfico entre {ciudad1} y {ciudad2}.")
                else:
                    print("No existe una conexión entre esas ciudades.")
            elif modificacion == "b":
                ciudad1 = input("Ingrese el nombre de la primera ciudad: ")
                ciudad2 = input("Ingrese el nombre de la segunda ciudad: ")
                tiempo_normal = int(input("Ingrese el tiempo normal entre las ciudades en horas: "))
                tiempo_lluvia = int(input("Ingrese el tiempo en caso de lluvia en horas: "))
                tiempo_nieve = int(input("Ingrese el tiempo en caso de nieve en horas: "))
                tiempo_tormenta = int(input("Ingrese el tiempo en caso de tormenta en horas: "))
                grafo_logistica.agregar_conexion(ciudad1, ciudad2, tiempo_normal, tiempo_lluvia, tiempo_nieve, tiempo_tormenta)
                print(f"Se ha establecido una nueva conexión entre {ciudad1} y {ciudad2}.")
            elif modificacion == "c":
                ciudad1 = input("Ingrese el nombre de la primera ciudad: ")
                ciudad2 = input("Ingrese el nombre de la segunda ciudad: ")
                clima = input("Ingrese el clima entre las ciudades (normal, lluvia, nieve, tormenta): ")
                if ciudad1 in grafo_logistica.grafo and ciudad2 in grafo_logistica.grafo[ciudad1]:
                    grafo_logistica.grafo[ciudad1][ciudad2][clima] = int(input(f"Ingrese el tiempo en caso de {clima} en horas: "))
                    print(f"Se ha actualizado el tiempo en caso de {clima} entre {ciudad1} y {ciudad2}.")
                else:
                    print("No existe una conexión entre esas ciudades.")
            else:
                print("Opción de modificación inválida.")

        elif opcion == 4:
            print("Saliendo del programa...")
            break

if __name__ == "__main__":
    main()

