import sys
from App import logic
from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as lt


def new_logic():
    return logic.new_logic()

def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8 (Bono)")
    print("0- Salir")

def load_data(control):
    """
    Carga los datos
    """
    # Realizar la carga de datos
    print("Seleccionando archivo de datos...")
    
    # Mostrar opciones de archivos
    print("\nArchivos disponibles:")
    print("1. deliverytime_20.csv  (~15,200 registros)")
    print("2. deliverytime_40.csv  (~30,400 registros)")  
    print("3. deliverytime_60.csv  (~45,600 registros)")
    print("4. deliverytime_80.csv  (~60,800 registros)")
    print("5. deliverytime_100.csv (~76,000 registros)")
    
    # Permitir selección del usuario
    while True:
        try:
            choice = input("Selecciona una opción (1-5): ").strip()
            
            files = {
                '1': 'Data/deliverytime_20.csv',
                '2': 'Data/deliverytime_40.csv',
                '3': 'Data/deliverytime_60.csv',
                '4': 'Data/deliverytime_80.csv', 
                '5': 'Data/deliverytime_100.csv'
            }
            
            if choice in files:
                filename = files[choice]
                break
            else:
                print("Opción inválida. Por favor selecciona 1-5.")
                
        except KeyboardInterrupt:
            print("\nOperación cancelada.")
            return control
    
    # Cargar los datos usando la función de logic
    updated_control = logic.load_data(control, filename)
    
    if updated_control:
        print("¡Datos cargados exitosamente!")
        return updated_control
    else:
        print("Error al cargar los datos.")
        return control


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    print("\n" + "="*80)
    print("REQUERIMIENTO 1: CAMINO SIMPLE ENTRE DOS UBICACIONES")
    print("="*80)
    print("Algoritmo utilizado: BFS (Breadth-First Search)")
    print("="*80)
    print("\n¿Deseas ver algunos nodos disponibles como referencia? (s/n): ", end="")
    show_nodes = input().strip().lower()
    if show_nodes == 's':
        print("\nMuestra de nodos disponibles en el grafo:")
        print("-" * 60)
        sample_nodes = logic.get_available_nodes_sample(control, 15)
        if lt.size(sample_nodes) > 0:
            print(f"{'No.':<3} {'ID del Nodo':<25} {'Tipo':<12} {'Coordenadas':<20}")
            print("-" * 60)
            for i in range(min(15, lt.size(sample_nodes))):
                node = lt.get_element(sample_nodes, i)
                node_id = mp.get(node, 'id')
                node_type = mp.get(node, 'type')
                lat = mp.get(node, 'latitude')
                lon = mp.get(node, 'longitude')
                coords = f"({lat}, {lon})"
                print(f"{i+1:<3} {node_id:<25} {node_type:<12} {coords:<20}")
        else:
            print("No se encontraron nodos en el grafo.")
        print("-" * 60)
    print("\nIngresa los datos para la búsqueda:")
    print("Formato del ID: latitud_longitud (ejemplo: 22.7446_75.8943)")
    while True:
        origin_id = input("\nID del punto de origen: ").strip()
        if origin_id:
            break
        print("El ID de origen no puede estar vacío.")
    while True:
        dest_id = input("ID del punto de destino: ").strip()
        if dest_id:
            break
        print("El ID de destino no puede estar vacío.")
    if origin_id == dest_id:
        print("El origen y destino no pueden ser iguales.")
        return
    print(f"\n Buscando camino desde '{origin_id}' hasta '{dest_id}'...")
    print("Ejecutando algoritmo BFS...")
    try:
        result = logic.req_1(control, origin_id, dest_id)
        if mp.contains(result, 'error'):
            error_msg = mp.get(result, 'error')
            execution_time = mp.get(result, 'execution_time')
            print(f"\n ERROR: {error_msg}")
            print(f"Tiempo de ejecución: {execution_time:.2f} ms")
            return
        path_exists = mp.get(result, 'path_exists')
        execution_time = mp.get(result, 'execution_time')
        print(f"\nTiempo de ejecución: {execution_time:.2f} ms")
        if not path_exists:
            message = mp.get(result, 'message')
            print(f"\n{message}")
            return
        path_length = mp.get(result, 'path_length')
        path_sequence = mp.get(result, 'path_sequence')
        deliverers = mp.get(result, 'deliverers')
        restaurants = mp.get(result, 'restaurants')
        total_deliverers = mp.get(result, 'total_deliverers')
        total_restaurants = mp.get(result, 'total_restaurants')
        print("\n" + "="*80)
        print("CAMINO ENCONTRADO")
        print("="*80)
        print(f"Origen: {origin_id}")
        print(f"Destino: {dest_id}")
        print(f"Cantidad de puntos en el camino: {path_length}")
        print(f"Domiciliarios únicos en el camino: {total_deliverers}")
        print(f"Restaurantes en el camino: {total_restaurants}")
        print(f"\nSECUENCIA DEL CAMINO:")
        print("-" * 50)
        print(f"{'Paso':<5} {'ID del Nodo':<25} {'Coordenadas':<20}")
        print("-" * 50)
        for i in range(lt.size(path_sequence)):
            node_id = lt.get_element(path_sequence, i)
            coords = node_id.replace('_', ', ')
            print(f"{i+1:<5} {node_id:<25} ({coords})")
        if total_deliverers > 0:
            print(f"\nDOMICILIARIOS EN EL CAMINO ({total_deliverers}):")
            print("-" * 40)
            deliverers_per_line = 5
            for i in range(lt.size(deliverers)):
                deliverer_id = lt.get_element(deliverers, i)
                print(f"{deliverer_id:<15}", end="")
                if (i + 1) % deliverers_per_line == 0:
                    print()
            if lt.size(deliverers) % deliverers_per_line != 0:
                print() 
        else:
            print(f"\nNo se encontraron domiciliarios en el camino.")
        if total_restaurants > 0:
            print(f"\n RESTAURANTES EN EL CAMINO ({total_restaurants}):")
            print("-" * 70)
            print(f"{'No.':<3} {'ID del Restaurante':<25} {'Coordenadas':<20}")
            print("-" * 70)
            for i in range(lt.size(restaurants)):
                restaurant = lt.get_element(restaurants, i)
                rest_id = mp.get(restaurant, 'id')
                lat = mp.get(restaurant, 'latitude')
                lon = mp.get(restaurant, 'longitude')
                coords = f"({lat}, {lon})" 
                print(f"{i+1:<3} {rest_id:<25} {coords:<20}")
        else:
            print(f"\nNo se encontraron restaurantes en el camino.")
        print("\n" + "="*80)
        print("Búsqueda completada exitosamente")
        print("="*80)
    except Exception as e:
        print(f"\nError inesperado: {str(e)}")
        print("Por favor, verifica que los datos estén correctamente cargados.")

def show_sample_nodes_for_testing(control):
    print("\n NODOS DISPONIBLES PARA TESTING:")
    print("="*70)
    sample_nodes = logic.get_available_nodes_sample(control, 20)
    if lt.size(sample_nodes) > 0:
        print(f"{'No.':<3} {'ID del Nodo':<30} {'Tipo':<12} {'Coordenadas':<25}")
        print("-" * 70)
        restaurants_count = 0
        delivery_count = 0
        for i in range(lt.size(sample_nodes)):
            node = lt.get_element(sample_nodes, i)
            node_id = mp.get(node, 'id')
            node_type = mp.get(node, 'type')
            lat = mp.get(node, 'latitude')
            lon = mp.get(node, 'longitude')
            coords = f"({lat}, {lon})"
            if node_type == 'restaurant':
                restaurants_count += 1
                type_symbol = ""
            else:
                delivery_count += 1
                type_symbol = ""
            
            print(f"{i+1:<3} {node_id:<30} {type_symbol} {node_type:<10} {coords:<25}")
        print("-" * 70)
        print(f"Total: {lt.size(sample_nodes)} nodos ({restaurants_count} restaurantes, {delivery_count} destinos)")
        print("\n Copia y pega los IDs para probar el requerimiento.")
    else:
        print("No se encontraron nodos en el grafo.")
        print("Asegúrate de haber cargado los datos primero (Opción 1 del menú).")
    print("="*70)
    
    
def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    pass


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
