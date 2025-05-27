import time
import sys
import os
import tabulate as tb
from datetime import datetime
import tabulate as tb


default_limit=100000
sys.setrecursionlimit(default_limit*10)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DataStructures.List.list_iterator import iterator
from DataStructures.List import array_list as al
from App import logic

def new_logic():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función de la lógica donde se crean las estructuras de datos
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

def load_data(control, archivo):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    print()
    print("INICIANDO LA CARGA DE DATOS")
    print("========================================================================================================")
    domicilios_total, domiciliarios_total, nodos_total, arcos_total, restaurantes_total, destinos_total, tiempo_promedio, tiempo_carga_ms = logic.load_data(control, archivo)
    print("SE CARGARON LOS DATOS CORRECTAMENTE")
    print("Tiempo de ejecución en ms: ", tiempo_carga_ms)
    print("Número total de domicilios procesados: ", domicilios_total)
    print("Número total de domiciliarios identificados: ", domiciliarios_total)
    print("Número total de nodos en el grafo creado: ", nodos_total)
    print("Número de arcos en el grafo creado: ", arcos_total)
    print("Número de restaurantes identificados por su ubicación geográfica: ", restaurantes_total)
    print("Número de ubicaciones donde han llegado los domiciliarios: ", destinos_total)
    print("Promedio de tiempo de entrega de todos los domicilios procesados: ", round(tiempo_promedio, 3))    
    print()
    

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
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
            archivo = seleccionar_archivo()
            load_data(control, archivo)
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

def seleccionar_archivo():
    print("Escoja el archivo a cargar")
    print("0- deliverytime_min.csv")
    print("1- deliverytime_20.csv")
    print("2- deliverytime_40.csv")
    print("3- deliverytime_60.csv")
    print("4- deliverytime_80.csv")
    print("5- deliverytime_100.csv")
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs) == 0:
        return "deliverytime_min.csv"
    elif int(inputs) == 1:
        return "deliverytime_20.csv"
    elif int(inputs) == 2:
        return "deliverytime_40.csv"
    elif int(inputs) == 3:
        return "deliverytime_60.csv"
    elif int(inputs) == 4:
        return "deliverytime_80.csv"
    elif int(inputs) == 5:
        return "deliverytime_100.csv"
    else:
        print("Opción errónea, vuelva a elegir.\n")
        seleccionar_archivo()