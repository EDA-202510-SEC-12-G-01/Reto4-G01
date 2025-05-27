
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
    data = logic.get_data(control, id)
    if data:
        print(f"\nInformación del domicilio {id}:")
        print("-" * 40)
        try:
            delivery_person = mp.get(data, 'delivery_person_id')
            origin = mp.get(data, 'origin')
            destination = mp.get(data, 'destination')
            time_taken = mp.get(data, 'time_taken')
            order_type = mp.get(data, 'order_type')
            
            print(f"Domiciliario: {delivery_person}")
            print(f"Origen: {origin}")
            print(f"Destino: {destination}")
            print(f"Tiempo: {time_taken} minutos")
            print(f"Tipo de orden: {order_type}")
        except:
            print("Error al mostrar detalles del domicilio")
    else:
        print(f"No se encontró información para el ID: {id}")

def print_req_1(control):
    """
    Función que imprime la solución del Requerimiento 1 en consola
    """
    pass
    
    
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


# main del ejercicio
def main():
    """
    Menu principal - VERSIÓN CORREGIDA
    """
    # ✅ SOLUCIÓN: Crear control localmente dentro de main()
    control = new_logic()
    
    working = True
    #ciclo del menu
    while working:
        print_menu()
        try:
            inputs = input('Seleccione una opción para continuar\n')
            option = int(inputs)
            
            if option == 1:
                print("Cargando información de los archivos ....\n")
                control = load_data(control)  # ✅ Ahora funciona correctamente

            elif option == 2:
                print_req_1(control)

            elif option == 3:
                print_req_2(control)

            elif option == 4:
                print_req_3(control)

            elif option == 5:
                print_req_4(control)

            elif option == 6:
                print_req_5(control)

            elif option == 7:
                print_req_6(control)

            elif option == 8:
                print_req_7(control)

            elif option == 9:
                print_req_8(control)

            elif option == 0:
                working = False
                print("\nGracias por utilizar el programa") 
            else:
                print("Opción errónea, vuelva a elegir.\n")
                
        except ValueError:
            print("Por favor ingrese un número válido.\n")
        except KeyboardInterrupt:
            print("\n\nPrograma terminado por el usuario")
            working = False
        except Exception as e:
            print(f"Error inesperado: {e}\n")
            
    sys.exit(0)