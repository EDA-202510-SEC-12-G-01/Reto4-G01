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

def print_req_1(catalog):
    """
    Ejecuta el requerimiento 1: Encontrar camino entre dos ubicaciones
    """
    print("\n" + "="*60)
    print("REQUERIMIENTO 1: CAMINO ENTRE UBICACIONES")
    print("="*60)
    
    if catalog is None:
        print("ERROR: Debe cargar los datos primero")
        return
    
    try:
        # Mostrar nodos de ejemplo
        show_sample_nodes(catalog)
        
        # Solicitar puntos de origen y destino
        print("\nIngrese los IDs de las ubicaciones (formato: latitud_longitud)")
        print("Ejemplo: 0.0000_0.0000")
        
        origin_id = input("\nPunto de origen: ").strip()
        if not origin_id:
            print("Operación cancelada")
            return
        
        dest_id = input("Punto de destino: ").strip()
        if not dest_id:
            print("Operación cancelada")
            return
        
        print(f"\nBuscando camino desde {origin_id} hasta {dest_id}...")
        
        # Ejecutar requerimiento
        result = logic.req_1(catalog, origin_id, dest_id)
        
        # Mostrar resultados
        print_req_1_results(result)
        
    except Exception as e:
        print(f"ERROR: Error ejecutando requerimiento 1: {str(e)}")

def print_req_1_results(result):
    """
    Imprime los resultados del requerimiento 1
    """
    print("\n" + "="*60)
    print("RESULTADOS DEL REQUERIMIENTO 1")
    print("="*60)
    
    # Tiempo de ejecución
    execution_time = result.get('execution_time', 0)
    print(f"Tiempo de ejecución: {execution_time:.2f} ms")
    
    if not result.get('path_exists', False):
        # No hay camino
        message = result.get('message', 'No existe camino')
        print(f"\nRESULTADO: {message}")
        
        if 'error' in result:
            print(f"Error: {result['error']}")
        return
    
    # Hay camino - mostrar información detallada
    print("\nRESULTADO: Se encontró un camino válido")
    print("-" * 60)
    
    # Cantidad de puntos geográficos
    path_length = result.get('path_length', 0)
    print(f"Cantidad de puntos geográficos en el camino: {path_length}")
    
    # Secuencia de ubicaciones
    if 'path_sequence' in result:
        path_sequence = result['path_sequence']
        print(f"\nSecuencia de ubicaciones:")
        for i in range(lt.size(path_sequence)):
            node_id = lt.get_element(path_sequence, i)
            coords = node_id.replace('_', ', ')
            print(f"  {i+1}. ({coords})")
    
    # Domiciliarios únicos
    if 'unique_deliverers' in result:
        deliverers = result['unique_deliverers']
        deliverers_count = lt.size(deliverers)
        print(f"\nDomiciliarios que componen el camino (sin repetir): {deliverers_count}")
        
        if deliverers_count > 0:
            print("IDs de domiciliarios:")
            for i in range(lt.size(deliverers)):
                deliverer_id = lt.get_element(deliverers, i)
                print(f"  - {deliverer_id}")
    
    # Restaurantes encontrados
    if 'restaurants_found' in result:
        restaurants = result['restaurants_found']
        restaurants_count = lt.size(restaurants)
        print(f"\nRestaurantes encontrados en el camino: {restaurants_count}")
        
        if restaurants_count > 0:
            print("Ubicaciones de restaurantes:")
            for i in range(lt.size(restaurants)):
                restaurant_id = lt.get_element(restaurants, i)
                coords = restaurant_id.replace('_', ', ')
                print(f"  - ({coords})")

def show_sample_nodes(catalog):
    """
    Muestra algunos nodos de ejemplo del catálogo para facilitar las pruebas
    """
    if catalog is None:
        return
    
    try:
        # Mostrar algunos restaurantes
        restaurants = logic.get_restaurants_list(catalog)
        if lt.size(restaurants) > 0:
            print("\nEjemplos de restaurantes disponibles:")
            for i in range(min(3, lt.size(restaurants))):
                restaurant_id = lt.get_element(restaurants, i)
                coords = restaurant_id.replace('_', ', ')
                print(f"  - {restaurant_id} (coordenadas: {coords})")
        
        # Mostrar algunas ubicaciones de entrega
        delivery_locations = logic.get_delivery_locations_list(catalog)
        if lt.size(delivery_locations) > 0:
            print("\nEjemplos de ubicaciones de entrega disponibles:")
            for i in range(min(3, lt.size(delivery_locations))):
                location_id = lt.get_element(delivery_locations, i)
                coords = location_id.replace('_', ', ')
                print(f"  - {location_id} (coordenadas: {coords})")
                
    except Exception as e:
        print(f"No se pudieron obtener ejemplos: {e}")
    
    
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
            control = load_data(control)  # Actualizar la variable control
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