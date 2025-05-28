import time
import sys
import os
import tabulate as tb
from datetime import datetime

default_limit=100000
sys.setrecursionlimit(default_limit*10)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DataStructures.List.list_iterator import iterator
from DataStructures.List import array_list as al
from App import logic
from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as lt

def new_logic():
    """
        Se crea una instancia del controlador
    """
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
    Carga los datos - MANTENER ORIGINAL
    """
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
    REQ 1 CORREGIDO: Función que imprime la solución del Requerimiento 1 en consola
    """
    print("\n" + "="*60)
    print("REQUERIMIENTO 1: CAMINO SIMPLE ENTRE UBICACIONES")
    print("="*60)
    
    try:
        print("Ingrese los IDs de las ubicaciones geográficas:")
        print("Formato esperado: 22.7446_75.8944")
        print("También puede usar coordenadas separadas como: 22.7446 75.8944")
        print()
        
        # Función auxiliar para validar y formatear coordenadas
        def process_input(user_input):
            user_input = user_input.strip()
            
            # Si ya viene en formato correcto (lat_lon)
            if '_' in user_input and len(user_input.split('_')) == 2:
                parts = user_input.split('_')
                try:
                    lat = float(parts[0])
                    lon = float(parts[1])
                    return f"{lat:.4f}_{lon:.4f}"
                except ValueError:
                    return user_input
            
            # Si viene como "lat lon" (separado por espacio)
            elif ' ' in user_input and len(user_input.split()) == 2:
                parts = user_input.split()
                try:
                    lat = float(parts[0])
                    lon = float(parts[1])
                    return f"{lat:.4f}_{lon:.4f}"
                except ValueError:
                    return user_input
            
            # Si viene como "lat,lon" (separado por coma)
            elif ',' in user_input and len(user_input.split(',')) == 2:
                parts = user_input.split(',')
                try:
                    lat = float(parts[0].strip())
                    lon = float(parts[1].strip())
                    return f"{lat:.4f}_{lon:.4f}"
                except ValueError:
                    return user_input
            
            # Devolver tal como está
            return user_input
        
        origin_input = input(" ID del punto geográfico de origen: ").strip()
        dest_input = input(" ID del punto geográfico de destino: ").strip()
        
        if not origin_input or not dest_input:
            print(" Los IDs no pueden estar vacíos")
            return
        
        # Procesar las entradas
        origin_id = process_input(origin_input)
        dest_id = process_input(dest_input)
        
        print(f"\n Procesando entradas:")
        print(f"   Origen: '{origin_input}' → '{origin_id}'")
        print(f"   Destino: '{dest_input}' → '{dest_id}'")
        print(f"\n Buscando camino...")
        
        # Ejecutar requerimiento
        resultado = logic.req_1(control, origin_id, dest_id)
        
        # Preparar tabla de resultados
        table_data = []
        
        # Agregar información básica
        table_data.append(["Tiempo de Ejecución (ms)", resultado['execution_time']])
        table_data.append(["Mensaje", resultado['message']])
        table_data.append(["Puntos en el camino", resultado['points_count']])
        
        if resultado['points_count'] > 0:
            # Convertir path a lista de strings para mostrar
            path_list = []
            path_al = resultado['path']
            for i in range(al.size(path_al)):
                path_list.append(str(al.get_element(path_al, i)))
            
            # Convertir domiciliarios a lista de strings
            dom_list = []
            doms_al = resultado['domiciliarios']
            for i in range(al.size(doms_al)):
                dom_list.append(str(al.get_element(doms_al, i)))
            
            # Convertir restaurantes a lista de strings
            rest_list = []
            rests_al = resultado['restaurants']
            for i in range(al.size(rests_al)):
                rest_list.append(str(al.get_element(rests_al, i)))
            
            # Mostrar información del camino
            table_data.append(["Estado", "✅ Camino encontrado"])
            table_data.append(["Longitud del camino (aristas)", len(path_list) - 1 if len(path_list) > 1 else 0])
            
            # Mostrar secuencia del camino (limitada si es muy larga)
            if len(path_list) <= 10:
                sequence_str = " → ".join(path_list)
            else:
                sequence_str = " → ".join(path_list[:5]) + " → ... → " + " → ".join(path_list[-5:])
            table_data.append(["Secuencia del Camino", sequence_str])
            
            # Mostrar domiciliarios
            table_data.append(["Domiciliarios únicos", len(dom_list)])
            if len(dom_list) <= 15:
                dom_display = ", ".join(dom_list) if dom_list else "Ninguno"
            else:
                dom_display = f"{', '.join(dom_list[:15])}... (+{len(dom_list)-15} más)"
            table_data.append(["Lista de Domiciliarios", dom_display])
            
            # Mostrar restaurantes
            table_data.append(["Restaurantes encontrados", len(rest_list)])
            rest_display = ", ".join(rest_list) if rest_list else "Ninguno"
            table_data.append(["Lista de Restaurantes", rest_display])
            
        else:
            table_data.append(["Estado", "❌ No se encontró camino"])
            table_data.append(["Longitud del camino", "N/A"])
            table_data.append(["Secuencia del Camino", "N/A"])
            table_data.append(["Domiciliarios únicos", "N/A"])
            table_data.append(["Restaurantes encontrados", "N/A"])
        
        print("\n--- Resultado Requerimiento 1 ---")
        print(tb.tabulate(table_data, headers=["Concepto", "Valor"], tablefmt="grid"))
        print()
        
        # Mostrar sugerencias si no se encontró camino
        if resultado['points_count'] == 0:
            print("💡 Sugerencias:")
            print("   - Verifique que las coordenadas sean correctas")
            print("   - Asegúrese de que los puntos existan en el dataset cargado") 
            print("   - Intente con otros puntos geográficos")
            print("   - Verifique que los datos estén correctamente cargados")
            print()
        
    except Exception as e:
        print(f" Error en requerimiento 1: {e}")
        print("\n🔍 Información de depuración:")
        import traceback
        traceback.print_exc()
        print("\n💡 Posibles soluciones:")
        print("   - Verifique que los datos estén cargados correctamente")
        print("   - Asegúrese de usar el formato correcto de coordenadas")
        print("   - Intente reiniciar el programa y cargar los datos nuevamente")
        print()

def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    print("\n--- Requerimiento 2 ---")
    print("🚧 Por implementar")
    print()

def print_req_3(control):
    """
    REQ 3: Función que imprime la solución del Requerimiento 3 en consola
    """
    print("\n" + "="*60)
    print("REQUERIMIENTO 3: DOMICILIARIO MÁS ACTIVO EN UN PUNTO")
    print("="*60)
    
    try:
        print("Ingrese el ID del punto geográfico:")
        print("Formato esperado: 22.7446_75.8944")
        print()
        
        point = input(" Punto geográfico: ").strip()
        
        if not point:
            print(" El ID del punto no puede estar vacío")
            return
        
        print(f"\n Analizando domiciliarios en el punto '{point}'...")
        
        resultado = logic.req_3(control, point)
        
        table = [
            ["Tiempo de Ejecución (ms)", resultado['tiempo_ms']],
            ["Domiciliario más activo", resultado['domiciliario']],
            ["Número de pedidos en el punto", resultado['pedidos']],
            ["Tipo de vehículo más usado", resultado['vehiculo']]
        ]
        
        print("\n--- Resultado Requerimiento 3 ---")
        print(tb.tabulate(table, headers=["Concepto", "Valor"], tablefmt="grid"))
        print()
        
    except Exception as e:
        print(f" Error en requerimiento 3: {e}")
        import traceback
        traceback.print_exc()

def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    print("\n--- Requerimiento 4 ---")
    print("🚧 Por implementar")
    print()

def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    print("\n--- Requerimiento 5 ---")
    print("🚧 Por implementar")
    print()

def print_req_6(control):
    """
    REQ 6: Función que imprime la solución del Requerimiento 6 en consola
    """
    print("\n" + "="*60)
    print("REQUERIMIENTO 6: CAMINOS DE COSTO MÍNIMO DESDE UN PUNTO")
    print("="*60)
    
    try:
        print("Ingrese el ID del punto geográfico de origen:")
        print("Formato esperado: 22.7446_75.8944")
        print()
        
        origen = input(" Punto geográfico de origen: ").strip()
        
        if not origen:
            print(" El ID del punto no puede estar vacío")
            return
        
        print(f"\n Calculando caminos de costo mínimo desde '{origen}'...")
        
        resultado = logic.req_6(control, origen)
        
        # Convertir lista de alcanzables a Python list para mostrar
        alcanzables_list = []
        alcanzables = resultado['alcanzables']
        for i in range(lt.size(alcanzables)):
            alcanzables_list.append(lt.get_element(alcanzables, i))
        
        # Convertir ruta más larga a Python list
        ruta_list = []
        ruta_max = resultado['ruta_mas_larga']
        for i in range(lt.size(ruta_max)):
            ruta_list.append(lt.get_element(ruta_max, i))
        
        # Mostrar alcanzables en grupos de 5
        print(f"\n RESULTADOS:")
        print(f"  Tiempo de ejecución: {resultado['tiempo_ms']} ms")
        print(f" Ubicaciones alcanzables: {resultado['cantidad_ubicaciones']}")
        print()
        
        print("  UBICACIONES ALCANZABLES:")
        if alcanzables_list:
            grupos = [alcanzables_list[i:i+5] for i in range(0, len(alcanzables_list), 5)]
            for grupo in grupos:
                print("     " + ", ".join(grupo))
        else:
            print("     Ninguna ubicación alcanzable")
        
        print(f"\n RUTA DE MAYOR TIEMPO MÍNIMO:")
        print(f"     Tiempo total: {resultado['tiempo_ruta_mas_larga']:.2f} minutos")
        if ruta_list:
            print(f"     Secuencia: {' → '.join(ruta_list)}")
        else:
            print("     No hay ruta disponible")
        
        print()
        
    except Exception as e:
        print(f" Error en requerimiento 6: {e}")
        import traceback
        traceback.print_exc()

def print_req_7(control):
    """
    REQ 7: Función que imprime la solución del Requerimiento 7 en consola
    """
    print("\n" + "="*60)
    print("REQUERIMIENTO 7: ÁRBOL DE RECUBRIMIENTO MÍNIMO PARA DOMICILIARIO")
    print("="*60)
    
    try:
        print("Ingrese los parámetros requeridos:")
        print("Formato de punto geográfico: 22.7446_75.8944")
        print()
        
        origen = input(" Punto geográfico de origen: ").strip()
        courier_id = input(" ID del domiciliario: ").strip()
        
        if not origen or not courier_id:
            print(" Ambos parámetros son requeridos")
            return
        
        print(f"\n Calculando árbol de recubrimiento mínimo...")
        print(f"    Origen: {origen}")
        print(f"    Domiciliario: {courier_id}")
        
        resultado = logic.req_7(control, origen, courier_id)
        
        # Convertir ubicaciones a Python list
        ubicaciones_list = []
        ubicaciones = resultado['ubicaciones']
        for i in range(lt.size(ubicaciones)):
            ubicaciones_list.append(lt.get_element(ubicaciones, i))
        
        # Crear tabla de resultados
        table = [
            ["Tiempo de Ejecución (ms)", resultado['tiempo_ms']],
            ["Cantidad de ubicaciones en sub-red", resultado['cantidad_ubicaciones']],
            ["Tiempo total del MST (minutos)", f"{resultado['tiempo_total_mst']:.2f}"],
            ["Domiciliario analizado", courier_id],
            ["Punto de origen", origen]
        ]
        
        print("\n--- Resultado Requerimiento 7 ---")
        print(tb.tabulate(table, headers=["Concepto", "Valor"], tablefmt="grid"))
        
        # Mostrar ubicaciones en grupos
        if ubicaciones_list:
            print(f"\n  UBICACIONES EN LA SUB-RED (ordenadas alfabéticamente):")
            grupos = [ubicaciones_list[i:i+5] for i in range(0, len(ubicaciones_list), 5)]
            for grupo in grupos:
                print("     " + ", ".join(grupo))
        else:
            print(f"\n  No se encontraron ubicaciones para el domiciliario {courier_id}")
        
        print()
        
    except Exception as e:
        print(f" Error en requerimiento 7: {e}")
        import traceback
        traceback.print_exc()

def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    print("\n--- Requerimiento 8 (Bono) ---")
    print("🚧 Por implementar")
    print()

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
        try:
            inputs = input('Seleccione una opción para continuar\n')
            option = int(inputs)
            
            if option == 1:
                print("Cargando información de los archivos ....\n")
                archivo = seleccionar_archivo()
                load_data(control, archivo)
                
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
                print("\n Gracias por utilizar el programa") 
            else:
                print(" Opción errónea, vuelva a elegir.\n")
                
        except ValueError:
            print(" Por favor ingrese un número válido.\n")
        except KeyboardInterrupt:
            print("\n\n Programa terminado por el usuario")
            working = False
        except Exception as e:
            print(f" Error inesperado: {e}\n")
    
    sys.exit(0)

def seleccionar_archivo():
    """
    MANTENER FUNCIÓN ORIGINAL DE SELECCIÓN DE ARCHIVOS
    """
    print("Escoja el archivo a cargar")
    print("0- deliverytime_min.csv")
    print("1- deliverytime_20.csv")
    print("2- deliverytime_40.csv")
    print("3- deliverytime_60.csv")
    print("4- deliverytime_80.csv")
    print("5- deliverytime_100.csv")
    
    while True:
        try:
            inputs = input('Seleccione una opción para continuar\n')
            option = int(inputs)
            
            if option == 0:
                return "deliverytime_min.csv"
            elif option == 1:
                return "deliverytime_20.csv"
            elif option == 2:
                return "deliverytime_40.csv"
            elif option == 3:
                return "deliverytime_60.csv"
            elif option == 4:
                return "deliverytime_80.csv"
            elif option == 5:
                return "deliverytime_100.csv"
            else:
                print(" Opción errónea, vuelva a elegir.\n")
        except ValueError:
            print(" Por favor ingrese un número válido.\n")
        except KeyboardInterrupt:
            print("\n Selección cancelada, usando archivo por defecto.")
            return "deliverytime_20.csv"