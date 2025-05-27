import time
import csv
import os
from DataStructures.Graph import digraph as dg
from DataStructures.Map import map_linear_probing as mp  
from DataStructures.List import array_list as lt

def new_logic():
    # Crear catálogo principal usando mapa
    catalog = mp.new_map(20, 0.7)
    
    # Crear grafo principal no dirigido
    mp.put(catalog, 'graph', dg.new_graph(10000))
    
    # Crear mapas para almacenar información
    mp.put(catalog, 'deliveries', mp.new_map(5000, 0.7))
    mp.put(catalog, 'delivery_persons', mp.new_map(1000, 0.7))
    mp.put(catalog, 'restaurants', mp.new_map(2000, 0.7))
    mp.put(catalog, 'delivery_locations', mp.new_map(3000, 0.7))
    mp.put(catalog, 'node_deliverers', mp.new_map(5000, 0.7))
    mp.put(catalog, 'edge_times', mp.new_map(10000, 0.7))
    mp.put(catalog, 'deliverer_last_delivery', mp.new_map(1000, 0.7))
    
    # Crear mapa de estadísticas usando tus mapas
    stats = mp.new_map(15, 0.7)
    mp.put(stats, 'total_deliveries', 0)
    mp.put(stats, 'total_delivery_persons', 0)
    mp.put(stats, 'total_nodes', 0)
    mp.put(stats, 'total_edges', 0)
    mp.put(stats, 'total_restaurants', 0)
    mp.put(stats, 'total_delivery_locations', 0)
    mp.put(stats, 'total_delivery_time', 0.0)
    mp.put(stats, 'avg_delivery_time', 0.0)
    
    mp.put(catalog, 'stats', stats)
    
    return catalog

def load_data(catalog, filename):
    """
    Carga los datos del reto
    """
    # Si no se proporciona filename, permitir selección
    if filename is None:
        print("\nArchivos disponibles:")
        print("1. Data/deliverytime_20.csv")
        print("2. Data/deliverytime_40.csv") 
        print("3. Data/deliverytime_60.csv")
        print("4. Data/deliverytime_80.csv")
        print("5. Data/deliverytime_100.csv")
        
        choice = input("Selecciona archivo (1-5): ").strip()
        
        # Crear mapa de archivos usando tus mapas
        files = mp.new_map(10, 0.7)
        mp.put(files, '1', 'Data/deliverytime_20.csv')
        mp.put(files, '2', 'Data/deliverytime_40.csv')
        mp.put(files, '3', 'Data/deliverytime_60.csv')
        mp.put(files, '4', 'Data/deliverytime_80.csv')
        mp.put(files, '5', 'Data/deliverytime_100.csv')
        
        if mp.contains(files, choice):
            filename = mp.get(files, choice)
        else:
            filename = mp.get(files, '1')  # Por defecto el primero
    
    print(f"Cargando datos desde: {filename}")
    start_time = time.time()
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # Obtener referencias a los mapas
            graph = mp.get(catalog, 'graph')
            deliveries = mp.get(catalog, 'deliveries')
            delivery_persons = mp.get(catalog, 'delivery_persons')
            restaurants = mp.get(catalog, 'restaurants')
            delivery_locations = mp.get(catalog, 'delivery_locations')
            edge_times = mp.get(catalog, 'edge_times')
            deliverer_last_delivery = mp.get(catalog, 'deliverer_last_delivery')
            stats = mp.get(catalog, 'stats')
            
            for row in reader:
                # Procesar cada registro
                delivery_id = row.get('ID', 'Unknown').strip()
                delivery_person_id = row.get('Delivery_person_ID', 'Unknown').strip()
                
                # Coordenadas formateadas a 4 decimales
                try:
                    rest_lat = f"{float(row.get('Restaurant_latitude', '0')):.4f}"
                    rest_lon = f"{float(row.get('Restaurant_longitude', '0')):.4f}"
                    dest_lat = f"{float(row.get('Delivery_location_latitude', '0')):.4f}"
                    dest_lon = f"{float(row.get('Delivery_location_longitude', '0')):.4f}"
                except (ValueError, TypeError):
                    continue
                
                # CORREGIDO: Usar el nombre correcto de la columna
                time_taken = 0.0
                try:
                    time_field = row.get('Time_taken(min)', '0').strip()
                    time_taken = float(time_field)
                    
                    # Validar que el tiempo sea razonable
                    if time_taken < 0 or time_taken > 180:
                        time_taken = 0.0
                        
                except (ValueError, TypeError):
                    time_taken = 0.0
                
                # Crear identificadores de nodos
                origin_node = f"{rest_lat}_{rest_lon}"
                dest_node = f"{dest_lat}_{dest_lon}"
                
                # Agregar nodos si no existen
                if not dg.contains_vertex(graph, origin_node):
                    # Crear información del nodo usando mapa
                    node_info = mp.new_map(10, 0.7)
                    mp.put(node_info, 'latitude', rest_lat)
                    mp.put(node_info, 'longitude', rest_lon)
                    mp.put(node_info, 'type', 'restaurant')
                    mp.put(node_info, 'deliverers', lt.new_list())
                    
                    dg.insert_vertex(graph, origin_node, node_info)
                    mp.put(restaurants, origin_node, True)
                    
                    # Incrementar contador
                    current_count = mp.get(stats, 'total_restaurants')
                    mp.put(stats, 'total_restaurants', current_count + 1)
                
                if not dg.contains_vertex(graph, dest_node):
                    # Crear información del nodo usando mapa
                    node_info = mp.new_map(10, 0.7)
                    mp.put(node_info, 'latitude', dest_lat)
                    mp.put(node_info, 'longitude', dest_lon)
                    mp.put(node_info, 'type', 'delivery')
                    mp.put(node_info, 'deliverers', lt.new_list())
                    
                    dg.insert_vertex(graph, dest_node, node_info)
                    mp.put(delivery_locations, dest_node, True)
                    
                    # Incrementar contador
                    current_count = mp.get(stats, 'total_delivery_locations')
                    mp.put(stats, 'total_delivery_locations', current_count + 1)
                
                # Agregar/actualizar arco entre origen y destino
                edge_key = f"{min(origin_node, dest_node)}_{max(origin_node, dest_node)}"
                if mp.contains(edge_times, edge_key):
                    # Actualizar promedio usando mapa
                    edge_data = mp.get(edge_times, edge_key)
                    current_count = mp.get(edge_data, 'count')
                    current_total = mp.get(edge_data, 'total_time')
                    
                    new_count = current_count + 1
                    new_total_time = current_total + time_taken
                    new_avg_time = new_total_time / new_count
                    
                    mp.put(edge_data, 'count', new_count)
                    mp.put(edge_data, 'total_time', new_total_time)
                    mp.put(edge_data, 'avg_time', new_avg_time)
                    
                    dg.add_edge(graph, origin_node, dest_node, new_avg_time)
                else:
                    # Nuevo arco usando mapa
                    edge_data = mp.new_map(5, 0.7)
                    mp.put(edge_data, 'count', 1)
                    mp.put(edge_data, 'total_time', time_taken)
                    mp.put(edge_data, 'avg_time', time_taken)
                    
                    mp.put(edge_times, edge_key, edge_data)
                    dg.add_edge(graph, origin_node, dest_node, time_taken)
                
                # Arco secuencial por domiciliario
                if mp.contains(deliverer_last_delivery, delivery_person_id):
                    last_dest = mp.get(deliverer_last_delivery, delivery_person_id)
                    if last_dest != dest_node:
                        seq_edge_key = f"{min(last_dest, dest_node)}_{max(last_dest, dest_node)}"
                        if mp.contains(edge_times, seq_edge_key):
                            edge_data = mp.get(edge_times, seq_edge_key)
                            current_count = mp.get(edge_data, 'count')
                            current_total = mp.get(edge_data, 'total_time')
                            
                            new_count = current_count + 1
                            new_total_time = current_total + time_taken
                            new_avg_time = new_total_time / new_count
                            
                            mp.put(edge_data, 'count', new_count)
                            mp.put(edge_data, 'total_time', new_total_time)
                            mp.put(edge_data, 'avg_time', new_avg_time)
                            
                            dg.add_edge(graph, last_dest, dest_node, new_avg_time)
                        else:
                            edge_data = mp.new_map(5, 0.7)
                            mp.put(edge_data, 'count', 1)
                            mp.put(edge_data, 'total_time', time_taken)
                            mp.put(edge_data, 'avg_time', time_taken)
                            
                            mp.put(edge_times, seq_edge_key, edge_data)
                            dg.add_edge(graph, last_dest, dest_node, time_taken)
                
                mp.put(deliverer_last_delivery, delivery_person_id, dest_node)
                
                # Agregar domiciliario si es nuevo
                if not mp.contains(delivery_persons, delivery_person_id):
                    # Crear información del domiciliario usando mapa
                    person_info = mp.new_map(10, 0.7)
                    mp.put(person_info, 'age', row.get('Delivery_person_Age', 'Unknown'))
                    mp.put(person_info, 'ratings', row.get('Delivery_person_Ratings', 'Unknown'))
                    mp.put(person_info, 'vehicle', row.get('Type_of_vehicle', 'Unknown'))
                    mp.put(person_info, 'delivery_count', 1)
                    
                    mp.put(delivery_persons, delivery_person_id, person_info)
                    
                    # Incrementar contador
                    current_count = mp.get(stats, 'total_delivery_persons')
                    mp.put(stats, 'total_delivery_persons', current_count + 1)
                else:
                    # Actualizar contador de domicilios
                    person_info = mp.get(delivery_persons, delivery_person_id)
                    current_deliveries = mp.get(person_info, 'delivery_count')
                    mp.put(person_info, 'delivery_count', current_deliveries + 1)
                
                # Guardar domicilio usando mapa
                delivery_info = mp.new_map(10, 0.7)
                mp.put(delivery_info, 'delivery_person_id', delivery_person_id)
                mp.put(delivery_info, 'origin', origin_node)
                mp.put(delivery_info, 'destination', dest_node)
                mp.put(delivery_info, 'time_taken', time_taken)
                mp.put(delivery_info, 'order_type', row.get('Type_of_order', 'Unknown'))
                
                mp.put(deliveries, delivery_id, delivery_info)
                
                # Actualizar estadísticas
                current_total_deliveries = mp.get(stats, 'total_deliveries')
                current_total_time = mp.get(stats, 'total_delivery_time')
                
                mp.put(stats, 'total_deliveries', current_total_deliveries + 1)
                mp.put(stats, 'total_delivery_time', current_total_time + time_taken)
        
        # Calcular estadísticas finales
        mp.put(stats, 'total_nodes', dg.order(graph))
        mp.put(stats, 'total_edges', dg.size(graph))
        
        total_deliveries = mp.get(stats, 'total_deliveries')
        total_time = mp.get(stats, 'total_delivery_time')
        
        if total_deliveries > 0:
            avg_time = total_time / total_deliveries
            mp.put(stats, 'avg_delivery_time', avg_time)
        
        end_time = time.time()
        
        # Mostrar resumen
        print(f"\nCarga completada en {end_time - start_time:.2f} segundos")
        print("="*60)
        print("RESUMEN DE CARGA DE DATOS")
        print("="*60)
        print(f"Número total de domicilios procesados: {mp.get(stats, 'total_deliveries'):,}")
        print(f"Número total de domiciliarios identificados: {mp.get(stats, 'total_delivery_persons'):,}")
        print(f"Número total de nodos en el grafo: {mp.get(stats, 'total_nodes'):,}")
        print(f"Número de arcos en el grafo: {mp.get(stats, 'total_edges'):,}")
        print(f"Número de restaurantes identificados: {mp.get(stats, 'total_restaurants'):,}")
        print(f"Número de ubicaciones de entrega: {mp.get(stats, 'total_delivery_locations'):,}")
        print(f"Promedio de tiempo de entrega: {mp.get(stats, 'avg_delivery_time'):.2f} minutos")
        print("="*60)
        
        return catalog
        
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {filename}")
        return None
    except Exception as e:
        print(f"Error al cargar datos: {str(e)}")
        return None
# Funciones de consulta sobre el catálogo

def get_data(catalog, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Consulta en las Llamar la función del modelo para obtener un dato
    pass


def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


def req_7(catalog):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    pass


def req_8(catalog):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
