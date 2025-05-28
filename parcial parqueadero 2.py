import time

MAP_ROWS = 14
MAP_COLS = 14
TARIFA_POR_SEGUNDO = 0.05

vehiculos = {}

def generar_mapa():
    mapa = []

    for i in range(MAP_ROWS):
        fila = []
        for j in range(MAP_COLS):
            if i % 3 == 0 or j % 3 == 0:
                fila.append("V")
            else:
                fila.append("L")
        mapa.append(fila)

    # Entrada y salida centradas
    mapa[0][MAP_COLS // 2] = "E"
    mapa[MAP_ROWS - 1][MAP_COLS // 2] = "S"
    return mapa

def imprimir_mapa(mapa):
    print("\nMAPA DEL PARQUEADERO:")
    for i, fila in enumerate(mapa):
        print(f"{i:2} {' '.join(fila)}")
    header = "    " + " ".join([f"{j:>2}" for j in range(MAP_COLS)])
    print(header)

def registrar_vehiculo(placa):
    if placa not in vehiculos:
        entrada = time.time()
        vehiculos[placa] = {"entrada": entrada}
        print(f"✅ Vehículo {placa} registrado.")
    else:
        print("⚠️ El vehículo ya está registrado.")

def elegir_lugar(mapa):
    while True:
        try:
            fila = int(input("Ingrese la fila del lugar de parqueo (0-13): "))
            col = int(input("Ingrese la columna del lugar de parqueo (0-13): "))
            if mapa[fila][col] == "L":
                return (fila, col)
            elif mapa[fila][col] == "V":
                print("🚧 Esa posición es una vía, no se puede parquear ahí.")
            else:
                print("❌ Lugar ocupado o no disponible.")
        except (ValueError, IndexError):
            print("❌ Coordenadas inválidas. Intente nuevamente.")

def asignar_lugar_manual(mapa, placa):
    fila, col = elegir_lugar(mapa)
    mapa[fila][col] = "X"
    vehiculos[placa]["posicion"] = (fila, col)
    print(f"🚗 Lugar asignado a {placa} en posición ({fila}, {col}).")

def mostrar_disponibilidad(mapa):
    libres = sum(row.count("L") for row in mapa)
    ocupados = sum(row.count("X") for row in mapa)
    print(f"📊 Libres: {libres} | Ocupados: {ocupados}")

def retirar_vehiculo(mapa, placa):
    if placa in vehiculos:
        salida = time.time()
        entrada = vehiculos[placa]["entrada"]
        tiempo = salida - entrada
        valor = tiempo * TARIFA_POR_SEGUNDO
        i, j = vehiculos[placa]["posicion"]
        mapa[i][j] = "L"
        del vehiculos[placa]
        print(f"💸 Vehículo {placa} retirado.")
        print(f"⏱ Tiempo: {tiempo:.2f} segundos.")
        print(f"💰 Valor a pagar: ${valor:.2f}")
    else:
        print("⚠️ Vehículo no encontrado.")

def menu():
    mapa = generar_mapa()
    while True:
        imprimir_mapa(mapa)
        mostrar_disponibilidad(mapa)
        print("\n--- MENÚ ---")
        print("1. Registrar entrada de vehículo")
        print("2. Retirar vehículo")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            placa = input("Ingrese la placa del vehículo: ").upper()
            registrar_vehiculo(placa)
            asignar_lugar_manual(mapa, placa)
        elif opcion == "2":
            placa = input("Ingrese la placa del vehículo: ").upper()
            retirar_vehiculo(mapa, placa)
        elif opcion == "3":
            print("👋 Saliendo del sistema.")
            break
        else:
            print("❌ Opción no válida.")

if __name__ == "__main__":
    menu()
