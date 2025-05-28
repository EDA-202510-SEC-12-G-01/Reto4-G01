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
    Carga los datos 
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
    Función que imprime la solución del Requerimiento 1 en consola
    """
    print("\n" + "="*60)
    print("REQUERIMIENTO 1: CAMINO SIMPLE ENTRE UBICACIONES")
    print("="*60)
    try:
        print("Ingrese los IDs de las ubicaciones geográficas:")
        print("Formato esperado: 22.7446_75.8944")
        print("También puede usar coordenadas separadas como: 22.7446 75.8944")
        print()
        def process_input(user_input):
            user_input = user_input.strip()
            if '_' in user_input and len(user_input.split('_')) == 2:
                parts = user_input.split('_')
                try:
                    lat = float(parts[0])
                    lon = float(parts[1])
                    return f"{lat:.4f}_{lon:.4f}"
                except ValueError:
                    return user_input
            elif ' ' in user_input and len(user_input.split()) == 2:
                parts = user_input.split()
                try:
                    lat = float(parts[0])
                    lon = float(parts[1])
                    return f"{lat:.4f}_{lon:.4f}"
                except ValueError:
                    return user_input
            elif ',' in user_input and len(user_input.split(',')) == 2:
                parts = user_input.split(',')
                try:
                    lat = float(parts[0].strip())
                    lon = float(parts[1].strip())
                    return f"{lat:.4f}_{lon:.4f}"
                except ValueError:
                    return user_input
            return user_input
        origin_input = input(" ID del punto geográfico de origen: ").strip()
        dest_input = input(" ID del punto geográfico de destino: ").strip()
        if not origin_input or not dest_input:
            print(" Los IDs no pueden estar vacíos")
            return
        origin_id = process_input(origin_input)
        dest_id = process_input(dest_input)
        print(f"\n Procesando entradas:")
        print(f"   Origen: '{origin_input}' → '{origin_id}'")
        print(f"   Destino: '{dest_input}' → '{dest_id}'")
        print(f"\n Buscando camino...")
        resultado = logic.req_1(control, origin_id, dest_id)
        table_data = []
        table_data.append(["Tiempo de Ejecución (ms)", resultado['execution_time']])
        table_data.append(["Mensaje", resultado['message']])
        table_data.append(["Puntos en el camino", resultado['points_count']])
        if resultado['points_count'] > 0:
            path_list = []
            path_al = resultado['path']
            for i in range(al.size(path_al)):
                path_list.append(str(al.get_element(path_al, i)))
            dom_list = []
            doms_al = resultado['domiciliarios']
            for i in range(al.size(doms_al)):
                dom_list.append(str(al.get_element(doms_al, i)))
            rest_list = []
            rests_al = resultado['restaurants']
            for i in range(al.size(rests_al)):
                rest_list.append(str(al.get_element(rests_al, i)))
            table_data.append(["Estado", " Camino encontrado"])
            table_data.append(["Longitud del camino (aristas)", len(path_list) - 1 if len(path_list) > 1 else 0])
            if len(path_list) <= 10:
                sequence_str = " → ".join(path_list)
            else:
                sequence_str = " → ".join(path_list[:5]) + " → ... → " + " → ".join(path_list[-5:])
            table_data.append(["Secuencia del Camino", sequence_str])
            table_data.append(["Domiciliarios únicos", len(dom_list)])
            if len(dom_list) <= 15:
                dom_display = ", ".join(dom_list) if dom_list else "Ninguno"
            else:
                dom_display = f"{', '.join(dom_list[:15])}... (+{len(dom_list)-15} más)"
            table_data.append(["Lista de Domiciliarios", dom_display])
            table_data.append(["Restaurantes encontrados", len(rest_list)])
            rest_display = ", ".join(rest_list) if rest_list else "Ninguno"
            table_data.append(["Lista de Restaurantes", rest_display])
        else:
            table_data.append(["Estado", " No se encontró camino"])
            table_data.append(["Longitud del camino", "N/A"])
            table_data.append(["Secuencia del Camino", "N/A"])
            table_data.append(["Domiciliarios únicos", "N/A"])
            table_data.append(["Restaurantes encontrados", "N/A"])
        print("\n--- Resultado Requerimiento 1 ---")
        print(tb.tabulate(table_data, headers=["Concepto", "Valor"], tablefmt="fancy_grid"))
        print()
        if resultado['points_count'] == 0:
            print(" Sugerencias:")
            print("   - Verifique que las coordenadas sean correctas")
            print("   - Asegúrese de que los puntos existan en el dataset cargado") 
            print("   - Intente con otros puntos geográficos")
            print("   - Verifique que los datos estén correctamente cargados")
            print()
    except Exception as e:
        print(f" Error en requerimiento 1: {e}")
        print("\n Información de depuración:")
        import traceback
        traceback.print_exc()
        print("\n Posibles soluciones:")
        print("   - Verifique que los datos estén cargados correctamente")
        print("   - Asegúrese de usar el formato correcto de coordenadas")
        print("   - Intente reiniciar el programa y cargar los datos nuevamente")
        print()



def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    print("\n--- Requerimiento 2 ---")
    print(" Por implementar")
    print()


def print_req_3(control):
    """
    Función que imprime la solución del Requerimiento 3 en consola
    """
    print("\n" + "="*60)
    print("REQUERIMIENTO 3: DOMICILIARIO MÁS ACTIVO EN UN PUNTO")
    print("="*60)
    try:
        print("Ingrese el ID del punto geográfico:")
        print("Formato esperado: 22.7446_75.8944")
        print("También puede usar coordenadas separadas como: 22.7446 75.8944")
        print()
        def process_input(user_input):
            user_input = user_input.strip()
            if '_' in user_input and len(user_input.split('_')) == 2:
                parts = user_input.split('_')
                try:
                    lat = float(parts[0])
                    lon = float(parts[1])
                    return f"{lat:.4f}_{lon:.4f}"
                except ValueError:
                    return user_input
            elif ' ' in user_input and len(user_input.split()) == 2:
                parts = user_input.split()
                try:
                    lat = float(parts[0])
                    lon = float(parts[1])
                    return f"{lat:.4f}_{lon:.4f}"
                except ValueError:
                    return user_input
            elif ',' in user_input and len(user_input.split(',')) == 2:
                parts = user_input.split(',')
                try:
                    lat = float(parts[0].strip())
                    lon = float(parts[1].strip())
                    return f"{lat:.4f}_{lon:.4f}"
                except ValueError:
                    return user_input
            return user_input
        point_input = input(" Punto geográfico: ").strip()
        if not point_input:
            print(" El ID del punto no puede estar vacío")
            return
        point_id = process_input(point_input)
        print(f"\n Procesando entrada:")
        print(f"   Punto: '{point_input}' → '{point_id}'")
        print(f"\n Analizando domiciliarios en el punto '{point_id}'...")
        resultado = logic.req_3(control, point_id)
        table_data = []
        table_data.append(["Tiempo de Ejecución (ms)", resultado['tiempo_ms']])
        if resultado['error'] is None:
            table_data.append(["Estado", " Análisis completado"])
            table_data.append(["Punto analizado", resultado.get('punto_analizado', point_id)])
            table_data.append(["Domiciliario más activo", resultado['domiciliario'] or "No encontrado"])
            table_data.append(["Número de pedidos", resultado['pedidos']])
            table_data.append(["Tipo de vehículo principal", resultado['vehiculo'] or "No determinado"])
            if 'total_domiciliarios_unicos' in resultado:
                table_data.append(["Total domiciliarios únicos", resultado['total_domiciliarios_unicos']])
        else:
            table_data.append(["Estado", " Error en el análisis"])
            table_data.append(["Motivo", resultado['error']])
            table_data.append(["Domiciliario más activo", "N/A"])
            table_data.append(["Número de pedidos", "N/A"])
            table_data.append(["Tipo de vehículo", "N/A"])
        print("\n--- Resultado Requerimiento 3 ---")
        print(tb.tabulate(table_data, headers=["Concepto", "Valor"], tablefmt="fancy_grid"))
        print()
        if resultado['error'] is None and resultado['pedidos'] > 0:
            print(" Información adicional:")
            print(f"   - El domiciliario {resultado['domiciliario']} realizó {resultado['pedidos']} pedidos en este punto")
            print(f"   - Tipo de vehículo más común: {resultado['vehiculo']}")
            if 'total_domiciliarios_unicos' in resultado:
                print(f"   - Total de domiciliarios diferentes que operaron en este punto: {resultado['total_domiciliarios_unicos']}")
            print()
        elif resultado['error'] is not None:
            print(" Sugerencias:")
            print("   - Verifique que las coordenadas sean correctas")
            print("   - Asegúrese de que el punto exista en el dataset cargado")
            print("   - Intente con otros puntos geográficos")
            print("   - Verifique que los datos estén correctamente cargados")
            print()
    except Exception as e:
        print(f" Error en requerimiento 3: {e}")
        print("\n Información de depuración:")
        import traceback
        traceback.print_exc()
        print("\n Posibles soluciones:")
        print("   - Verifique que los datos estén cargados correctamente")
        print("   - Asegúrese de usar el formato correcto de coordenadas")
        print("   - Intente reiniciar el programa y cargar los datos nuevamente")
        print()



def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    origen = input("Ingrese Punto A (latitud_longitud): ").strip()
    destino = input("Ingrese Punto B (latitud_longitud): ").strip()
    tiempo_ms, path, comunes = logic.req_4(control, origen, destino)
    seq = [al.get_element(path, i) for i in range(al.size(path))]
    com = [al.get_element(comunes, i) for i in range(al.size(comunes))]
    print("Tiempo de ejecución (ms):", round(tiempo_ms, 3))
    print("Secuencia de ubicaciones:", " -> ".join(seq) if seq else "Ninguno")
    print("Domiciliarios en común:", ", ".join(com) if com else "Ninguno")



def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    print("\n--- Requerimiento 5 ---")
    print(" Por implementar")
    print()



def print_req_6(control):
    """
    Función que imprime la solución del Requerimiento 6 en consola
    """
    print("\n" + "="*60)
    print("REQUERIMIENTO 6: CAMINOS DE COSTO MÍNIMO DESDE UN PUNTO")
    print("="*60)
    try:
        print("Ingrese el ID del punto geográfico de origen:")
        print("Formato esperado: 22.7446_75.8944")
        print("También puede usar coordenadas separadas como: 22.7446 75.8944")
        print()
        def process_input(user_input):
            user_input = user_input.strip()
            if '_' in user_input and len(user_input.split('_')) == 2:
                parts = user_input.split('_')
                try:
                    lat = float(parts[0])
                    lon = float(parts[1])
                    return f"{lat:.4f}_{lon:.4f}"
                except ValueError:
                    return user_input
            elif ' ' in user_input and len(user_input.split()) == 2:
                parts = user_input.split()
                try:
                    lat = float(parts[0])
                    lon = float(parts[1])
                    return f"{lat:.4f}_{lon:.4f}"
                except ValueError:
                    return user_input
            elif ',' in user_input and len(user_input.split(',')) == 2:
                parts = user_input.split(',')
                try:
                    lat = float(parts[0].strip())
                    lon = float(parts[1].strip())
                    return f"{lat:.4f}_{lon:.4f}"
                except ValueError:
                    return user_input
            return user_input
        origen_input = input(" Punto geográfico de origen: ").strip()
        if not origen_input:
            print(" El ID del punto no puede estar vacío")
            return
        origen = process_input(origen_input)
        print(f"\n Procesando entrada:")
        print(f"   Origen: '{origen_input}' → '{origen}'")
        print(f"\n Calculando caminos de costo mínimo desde '{origen}'...")
        resultado = logic.req_6(control, origen)
        table_data = []
        table_data.append(["Tiempo de Ejecución (ms)", resultado['tiempo_ms']])
        if resultado['error'] is None:
            table_data.append(["Estado", " Análisis completado"])
            table_data.append(["Punto de origen", resultado.get('punto_origen', origen)])
            table_data.append(["Ubicaciones alcanzables", resultado['cantidad_ubicaciones']])
            table_data.append(["Vértice más lejano", resultado.get('vertice_mas_lejano', 'N/A')])
            table_data.append(["Tiempo a vértice más lejano (min)", f"{resultado['tiempo_ruta_mas_larga']:.2f}"])
            table_data.append(["Longitud de ruta más larga", al.size(resultado['ruta_mas_larga'])])
        else:
            table_data.append(["Estado", " Error en el análisis"])
            table_data.append(["Motivo", resultado['error']])
            table_data.append(["Ubicaciones alcanzables", "N/A"])
            table_data.append(["Vértice más lejano", "N/A"])
            table_data.append(["Tiempo máximo", "N/A"])
        print("\n--- Resultado Requerimiento 6 ---")
        print(tb.tabulate(table_data, headers=["Concepto", "Valor"], tablefmt="fancy_grid"))
        if resultado['error'] is None and resultado['cantidad_ubicaciones'] > 0:
            print(f"\n UBICACIONES ALCANZABLES (ordenadas alfabéticamente):")
            alcanzables_list = []
            alcanzables = resultado['alcanzables']
            for i in range(al.size(alcanzables)):
                alcanzables_list.append(al.get_element(alcanzables, i))
            if alcanzables_list:
                print(f"   Total: {len(alcanzables_list)} ubicaciones")
                print()
                grupos = [alcanzables_list[i:i+5] for i in range(0, len(alcanzables_list), 5)]
                for i, grupo in enumerate(grupos):
                    print(f"   {i*5+1:3d}-{min((i+1)*5, len(alcanzables_list)):3d}: {', '.join(grupo)}")
            if al.size(resultado['ruta_mas_larga']) > 0:
                print(f"\n  RUTA DE MAYOR TIEMPO MÍNIMO:")
                print(f"   Destino: {resultado.get('vertice_mas_lejano', 'N/A')}")
                print(f"   Tiempo total: {resultado['tiempo_ruta_mas_larga']:.2f} minutos")
                ruta_list = []
                ruta_max = resultado['ruta_mas_larga']
                for i in range(al.size(ruta_max)):
                    ruta_list.append(al.get_element(ruta_max, i))
                if ruta_list:
                    if len(ruta_list) <= 10:
                        secuencia = ' → '.join(ruta_list)
                    else:
                        secuencia = f"{' → '.join(ruta_list[:5])} → ... → {' → '.join(ruta_list[-5:])}"
                    print(f"   Secuencia: {secuencia}")
                    print(f"   Longitud: {len(ruta_list)} puntos, {len(ruta_list)-1} aristas")
        elif resultado['error'] is not None:
            print("\n Sugerencias:")
            print("   - Verifique que las coordenadas sean correctas")
            print("   - Asegúrese de que el punto exista en el dataset cargado")
            print("   - Intente con otros puntos geográficos")
            print("   - Verifique que los datos estén correctamente cargados")
        print()
    except Exception as e:
        print(f" Error en requerimiento 6: {e}")
        print("\n Información de depuración:")
        import traceback
        traceback.print_exc()
        print("\n Posibles soluciones:")
        print("   - Verifique que los datos estén cargados correctamente")
        print("   - Asegúrese de usar el formato correcto de coordenadas")
        print("   - Intente reiniciar el programa y cargar los datos nuevamente")
        print()



def print_req_7(control):
    """
    Función que imprime la solución del Requerimiento 7 en consola
    """
    print("\n" + "="*60)
    print("REQUERIMIENTO 7: ÁRBOL DE RECUBRIMIENTO MÍNIMO PARA DOMICILIARIO")
    print("="*60)
    try:
        print("Ingrese los parámetros requeridos:")
        print("Formato de punto geográfico: 22.7446_75.8944")
        print("También puede usar coordenadas separadas como: 22.7446 75.8944")
        print()
        def process_input(user_input):
            user_input = user_input.strip()
            if '_' in user_input and len(user_input.split('_')) == 2:
                parts = user_input.split('_')
                try:
                    lat = float(parts[0])
                    lon = float(parts[1])
                    return f"{lat:.4f}_{lon:.4f}"
                except ValueError:
                    return user_input
            elif ' ' in user_input and len(user_input.split()) == 2:
                parts = user_input.split()
                try:
                    lat = float(parts[0])
                    lon = float(parts[1])
                    return f"{lat:.4f}_{lon:.4f}"
                except ValueError:
                    return user_input
            elif ',' in user_input and len(user_input.split(',')) == 2:
                parts = user_input.split(',')
                try:
                    lat = float(parts[0].strip())
                    lon = float(parts[1].strip())
                    return f"{lat:.4f}_{lon:.4f}"
                except ValueError:
                    return user_input
            return user_input
        origen_input = input(" Punto geográfico de origen: ").strip()
        courier_id = input(" ID del domiciliario: ").strip()
        if not origen_input or not courier_id:
            print(" Ambos parámetros son requeridos")
            return
        origen = process_input(origen_input)
        print(f"\n Procesando entradas:")
        print(f"   Origen: '{origen_input}' → '{origen}'")
        print(f"   Domiciliario: '{courier_id}'")
        print(f"\n Calculando árbol de recubrimiento mínimo...")
        resultado = logic.req_7(control, origen, courier_id)
        table_data = []
        table_data.append(["Tiempo de Ejecución (ms)", resultado['tiempo_ms']])
        if resultado['error'] is None:
            table_data.append(["Estado", " Análisis completado"])
            table_data.append(["Domiciliario analizado", resultado.get('domiciliario_analizado', courier_id)])
            table_data.append(["Punto de origen", resultado.get('punto_origen', origen)])
            table_data.append(["Ubicaciones en sub-red", resultado['cantidad_ubicaciones']])
            table_data.append(["Tiempo total del MST (min)", f"{resultado['tiempo_total_mst']:.2f}"])
            if 'aristas_en_subgrafo' in resultado:
                table_data.append(["Aristas en el subgrafo", resultado['aristas_en_subgrafo']])
        else:
            table_data.append(["Estado", " Error en el análisis"])
            table_data.append(["Motivo", resultado['error']])
            table_data.append(["Domiciliario analizado", resultado.get('domiciliario_analizado', courier_id)])
            table_data.append(["Punto de origen", resultado.get('punto_origen', origen)])
            table_data.append(["Ubicaciones en sub-red", resultado['cantidad_ubicaciones']])
            table_data.append(["Tiempo total del MST", "N/A"])
        print("\n--- Resultado Requerimiento 7 ---")
        print(tb.tabulate(table_data, headers=["Concepto", "Valor"], tablefmt="fancy_grid"))
        if resultado['cantidad_ubicaciones'] > 0:
            print(f"\n UBICACIONES EN LA SUB-RED (ordenadas alfabéticamente):")
            ubicaciones_list = []
            ubicaciones = resultado['ubicaciones']
            for i in range(al.size(ubicaciones)):
                ubicaciones_list.append(al.get_element(ubicaciones, i))
            if ubicaciones_list:
                print(f"   Total: {len(ubicaciones_list)} ubicaciones")
                print()
                grupos = [ubicaciones_list[i:i+4] for i in range(0, len(ubicaciones_list), 4)]
                for i, grupo in enumerate(grupos):
                    print(f"   {i*4+1:3d}-{min((i+1)*4, len(ubicaciones_list)):3d}: {', '.join(grupo)}")
        if resultado['error'] is None:
            if resultado['cantidad_ubicaciones'] >= 2:
                print(f"\n INFORMACIÓN DEL MST:")
                print(f"   - Tiempo total mínimo para conectar todas las ubicaciones: {resultado['tiempo_total_mst']:.2f} minutos")
                print(f"   - Domiciliario: {resultado.get('domiciliario_analizado', courier_id)}")
                print(f"   - Punto de partida: {resultado.get('punto_origen', origen)}")
                if 'aristas_en_subgrafo' in resultado:
                    print(f"   - Conexiones encontradas en el subgrafo: {resultado['aristas_en_subgrafo']}")
            elif resultado['cantidad_ubicaciones'] == 1:
                print(f"\n INFORMACIÓN:")
                print(f"   - El domiciliario {courier_id} solo tiene una ubicación registrada")
                print(f"   - No es posible calcular un MST con una sola ubicación")
        elif "no se encontró" in resultado['error'].lower():
            print(f"\n Sugerencias para el domiciliario:")
            print(f"   - Verifique que el ID '{courier_id}' sea correcto")
            print(f"   - Asegúrese de que el domiciliario esté registrado en el dataset")
            print(f"   - Intente con otros IDs de domiciliarios")
        elif "no existe" in resultado['error'].lower():
            print(f"\n Sugerencias para el punto origen:")
            print(f"   - Verifique que las coordenadas '{origen}' sean correctas")
            print(f"   - Asegúrese de que el punto exista en el dataset cargado")
            print(f"   - Intente con otros puntos geográficos")
        elif "no están conectadas" in resultado['error'].lower():
            print(f"\n Información sobre conectividad:")
            print(f"   - Las ubicaciones del domiciliario {courier_id} no están conectadas entre sí")
            print(f"   - Esto puede deberse a la estructura de los datos de entrega")
            print(f"   - Intente con otro domiciliario que tenga más actividad")
        print()
    except Exception as e:
        print(f" Error en requerimiento 7: {e}")
        print("\n Información de depuración:")
        import traceback
        traceback.print_exc()
        print("\n Posibles soluciones:")
        print("   - Verifique que los datos estén cargados correctamente")
        print("   - Asegúrese de usar el formato correcto de coordenadas")
        print("   - Verifique que el ID del domiciliario sea válido")
        print("   - Intente reiniciar el programa y cargar los datos nuevamente")
        print()



def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    print("\n--- Requerimiento 8 (Bono) ---")
    print("🚧 Por implementar")
    print()


control = new_logic()


def main():
    """
    Menu principal
    """
    working = True
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