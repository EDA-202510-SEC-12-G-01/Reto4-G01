import time
import csv
import os
from DataStructures.Graph import digraph as dg
from DataStructures.Map import map_linear_probing as mp  
from DataStructures.List import array_list as lt
from DataStructures.Graph import bfs as bfs_alg
from DataStructures.Stack import stack as st

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
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
    Carga los datos del reto - VERSIÓN CORREGIDA PARA IDs PROBLEMÁTICOS
    """
    if filename is None:
        print("\nArchivos disponibles:")
        print("1. Data/deliverytime_20.csv")
        print("2. Data/deliverytime_40.csv") 
        print("3. Data/deliverytime_60.csv")
        print("4. Data/deliverytime_80.csv")
        print("5. Data/deliverytime_100.csv")
        
        choice = input("Selecciona archivo (1-5): ").strip()
        
        files = mp.new_map(10, 0.7)
        mp.put(files, '1', 'Data/deliverytime_20.csv')
        mp.put(files, '2', 'Data/deliverytime_40.csv')
        mp.put(files, '3', 'Data/deliverytime_60.csv')
        mp.put(files, '4', 'Data/deliverytime_80.csv')
        mp.put(files, '5', 'Data/deliverytime_100.csv')
        
        if mp.contains(files, choice):
            filename = mp.get(files, choice)
        else:
            filename = mp.get(files, '1')
    
    print(f"Cargando datos desde: {filename}")
    start_time = time.time()
    
    # Contadores detallados
    error_stats = {
        'invalid_ids': 0,
        'coordinate_errors': 0,
        'parsing_errors': 0,
        'encoding_errors': 0,
        'other_errors': 0
    }
    
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
            node_deliverers = mp.get(catalog, 'node_deliverers')
            stats = mp.get(catalog, 'stats')
            
            processed_count = 0
            
            for row_num, row in enumerate(reader, 1):
                try:
                    # 1. LIMPIAR Y VALIDAR IDs - MANEJO ESPECIAL
                    raw_delivery_id = row.get('ID', '').strip()
                    raw_person_id = row.get('Delivery_person_ID', '').strip()
                    
                    # ✅ LIMPIAR IDs PROBLEMÁTICOS
                    delivery_id = clean_id(raw_delivery_id)
                    delivery_person_id = clean_id(raw_person_id)
                    
                    if not delivery_id or not delivery_person_id:
                        error_stats['invalid_ids'] += 1
                        if error_stats['invalid_ids'] <= 3:
                            print(f"Fila {row_num}: IDs problemáticos - Original: '{raw_delivery_id}' -> '{delivery_id}', Person: '{raw_person_id}' -> '{delivery_person_id}'")
                        continue
                    
                    # 2. COORDENADAS - SIN RESTRICCIONES INNECESARIAS
                    try:
                        rest_lat_str = row.get('Restaurant_latitude', '0').strip()
                        rest_lon_str = row.get('Restaurant_longitude', '0').strip()
                        dest_lat_str = row.get('Delivery_location_latitude', '0').strip()
                        dest_lon_str = row.get('Delivery_location_longitude', '0').strip()
                        
                        rest_lat = float(rest_lat_str)
                        rest_lon = float(rest_lon_str)
                        dest_lat = float(dest_lat_str)  
                        dest_lon = float(dest_lon_str)
                        
                        # ✅ VALIDACIÓN SOLO PARA RANGOS GEOGRÁFICOS REALES
                        # Latitud: -90 a 90, Longitud: -180 a 180
                        if (abs(rest_lat) > 90 or abs(rest_lon) > 180 or 
                            abs(dest_lat) > 90 or abs(dest_lon) > 180):
                            error_stats['coordinate_errors'] += 1
                            if error_stats['coordinate_errors'] <= 3:
                                print(f"Fila {row_num}: Coordenadas fuera de rango - Rest({rest_lat},{rest_lon}) Dest({dest_lat},{dest_lon})")
                            continue
                        
                        # Formatear a 4 decimales
                        rest_lat = f"{rest_lat:.4f}"
                        rest_lon = f"{rest_lon:.4f}"
                        dest_lat = f"{dest_lat:.4f}"
                        dest_lon = f"{dest_lon:.4f}"
                        
                    except (ValueError, TypeError) as e:
                        error_stats['parsing_errors'] += 1
                        if error_stats['parsing_errors'] <= 3:
                            print(f"Fila {row_num}: Error parsing coordenadas - {e}")
                        continue
                    
                    # 3. TIEMPO - MANEJO ROBUSTO
                    time_taken = 0.0
                    try:
                        time_field = row.get('Time_taken(min)', '0').strip()
                        if time_field:
                            time_taken = float(time_field)
                            if time_taken < 0:
                                time_taken = 0.0
                    except (ValueError, TypeError):
                        time_taken = 0.0
                    
                    # 4. PROCESAR NORMALMENTE (resto del código igual)
                    origin_node = f"{rest_lat}_{rest_lon}"
                    dest_node = f"{dest_lat}_{dest_lon}"
                    
                    # Agregar nodos si no existen
                    if not dg.contains_vertex(graph, origin_node):
                        node_info = mp.new_map(10, 0.7)
                        mp.put(node_info, 'latitude', rest_lat)
                        mp.put(node_info, 'longitude', rest_lon)
                        mp.put(node_info, 'type', 'restaurant')
                        mp.put(node_info, 'deliverers', lt.new_list())
                        
                        dg.insert_vertex(graph, origin_node, node_info)
                        mp.put(restaurants, origin_node, True)
                        
                        current_count = mp.get(stats, 'total_restaurants')
                        mp.put(stats, 'total_restaurants', current_count + 1)
                    
                    if not dg.contains_vertex(graph, dest_node):
                        node_info = mp.new_map(10, 0.7)
                        mp.put(node_info, 'latitude', dest_lat)
                        mp.put(node_info, 'longitude', dest_lon)
                        mp.put(node_info, 'type', 'delivery')
                        mp.put(node_info, 'deliverers', lt.new_list())
                        
                        dg.insert_vertex(graph, dest_node, node_info)
                        mp.put(delivery_locations, dest_node, True)
                        
                        current_count = mp.get(stats, 'total_delivery_locations')
                        mp.put(stats, 'total_delivery_locations', current_count + 1)
                    
                    # Agregar domiciliario a ambos nodos
                    _add_deliverer_to_node(graph, node_deliverers, origin_node, delivery_person_id)
                    _add_deliverer_to_node(graph, node_deliverers, dest_node, delivery_person_id)
                    
                    # Agregar/actualizar arco entre origen y destino
                    edge_key = f"{min(origin_node, dest_node)}_{max(origin_node, dest_node)}"
                    if mp.contains(edge_times, edge_key):
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
                        person_info = mp.new_map(10, 0.7)
                        
                        age_str = row.get('Delivery_person_Age', 'Unknown').strip()
                        ratings_str = row.get('Delivery_person_Ratings', 'Unknown').strip()
                        vehicle_str = row.get('Type_of_vehicle', 'Unknown').strip()
                        
                        mp.put(person_info, 'age', age_str)
                        mp.put(person_info, 'ratings', ratings_str)
                        mp.put(person_info, 'vehicle', vehicle_str)
                        mp.put(person_info, 'delivery_count', 1)
                        
                        mp.put(delivery_persons, delivery_person_id, person_info)
                        
                        current_count = mp.get(stats, 'total_delivery_persons')
                        mp.put(stats, 'total_delivery_persons', current_count + 1)
                    else:
                        person_info = mp.get(delivery_persons, delivery_person_id)
                        current_deliveries = mp.get(person_info, 'delivery_count')
                        mp.put(person_info, 'delivery_count', current_deliveries + 1)
                    
                    # Guardar domicilio
                    delivery_info = mp.new_map(10, 0.7)
                    order_type = row.get('Type_of_order', 'Unknown').strip()
                    
                    mp.put(delivery_info, 'delivery_person_id', delivery_person_id)
                    mp.put(delivery_info, 'origin', origin_node)
                    mp.put(delivery_info, 'destination', dest_node)
                    mp.put(delivery_info, 'time_taken', time_taken)
                    mp.put(delivery_info, 'order_type', order_type)
                    
                    mp.put(deliveries, delivery_id, delivery_info)
                    
                    # Actualizar estadísticas
                    current_total_deliveries = mp.get(stats, 'total_deliveries')
                    current_total_time = mp.get(stats, 'total_delivery_time')
                    
                    mp.put(stats, 'total_deliveries', current_total_deliveries + 1)
                    mp.put(stats, 'total_delivery_time', current_total_time + time_taken)
                    
                    processed_count += 1
                    
                except UnicodeDecodeError:
                    error_stats['encoding_errors'] += 1
                except Exception as e:
                    error_stats['other_errors'] += 1
                    if error_stats['other_errors'] <= 3:
                        print(f"Error en fila {row_num}: {e}")
        
        # Calcular estadísticas finales
        mp.put(stats, 'total_nodes', dg.order(graph))
        mp.put(stats, 'total_edges', dg.size(graph))
        
        total_deliveries = mp.get(stats, 'total_deliveries')
        total_time = mp.get(stats, 'total_delivery_time')
        
        if total_deliveries > 0:
            avg_time = total_time / total_deliveries
            mp.put(stats, 'avg_delivery_time', avg_time)
        
        end_time = time.time()
        total_errors = sum(error_stats.values())
        
        # Mostrar resumen detallado
        print(f"\nCarga completada en {end_time - start_time:.2f} segundos")
        print("="*60)
        print("RESUMEN DE CARGA CON ANÁLISIS DE ERRORES")
        print("="*60)
        print(f"✅ Filas procesadas exitosamente: {processed_count:,}")
        print(f"❌ Total de errores: {total_errors:,}")
        print()
        print("🔍 DESGLOSE DE ERRORES:")
        print(f"   • IDs problemáticos (notación científica): {error_stats['invalid_ids']:,}")
        print(f"   • Errores de coordenadas: {error_stats['coordinate_errors']:,}")
        print(f"   • Errores de parsing: {error_stats['parsing_errors']:,}")
        print(f"   • Errores de codificación: {error_stats['encoding_errors']:,}")
        print(f"   • Otros errores: {error_stats['other_errors']:,}")
        print()
        print("📊 ESTADÍSTICAS FINALES:")
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

def clean_id(raw_id):
    """
    Limpia IDs problemáticos con notación científica y caracteres especiales
    """
    if not raw_id:
        return ""
    
    # Limpiar espacios y caracteres especiales
    cleaned = raw_id.strip()
    
    # Manejar notación científica convirtiéndola a string válido
    try:
        # Si es notación científica (contiene E+ o E-), convertir a número y luego a string
        if 'E+' in cleaned.upper() or 'E-' in cleaned.upper():
            # Convertir a float y luego a string sin notación científica
            num_value = float(cleaned)
            # Si es un entero, convertir a int para evitar .0
            if num_value == int(num_value):
                cleaned = str(int(num_value))
            else:
                cleaned = f"{num_value:.0f}"  # Sin decimales para IDs
    except (ValueError, TypeError):
        # Si no se puede convertir, limpiar caracteres problemáticos
        cleaned = ''.join(c for c in cleaned if c.isalnum() or c in ['_', '-'])
    
    # Eliminar caracteres especiales problemáticos como Â
    cleaned = ''.join(c for c in cleaned if ord(c) < 128)  # Solo ASCII
    
    return cleaned if len(cleaned) > 0 else ""

def _add_deliverer_to_node(graph, node_deliverers, node_id, delivery_person_id):
    """
    Agrega un domiciliario a la lista de un nodo - FUNCIÓN HELPER MEJORADA
    """
    deliverer_key = f"{node_id}_{delivery_person_id}"
    
    # Verificar si ya se agregó este domiciliario a este nodo
    if not mp.contains(node_deliverers, deliverer_key):
        mp.put(node_deliverers, deliverer_key, True)
        
        # Obtener información del nodo y agregar domiciliario a su lista
        try:
            node_info = dg.get_vertex_information(graph, node_id)
            if node_info and mp.contains(node_info, 'deliverers'):
                deliverers_list = mp.get(node_info, 'deliverers')
                
                # Verificar si ya está en la lista
                found = False
                for i in range(lt.size(deliverers_list)):
                    if lt.get_element(deliverers_list, i) == delivery_person_id:
                        found = True
                        break
                
                if not found:
                    lt.add_last(deliverers_list, delivery_person_id)
        except (KeyError, AttributeError, TypeError):
            # Solo errores específicos esperados
            pass

# Funciones de consulta sobre el catálogo
def get_data(catalog, id):
    """
    Retorna un dato por su ID.
    """
    deliveries = mp.get(catalog, 'deliveries')
    if mp.contains(deliveries, id):
        return mp.get(deliveries, id)
    return None

def req_1(catalog, origin_id, dest_id):
    """Encuentra la ruta más corta entre dos nodos"""
    # TODO: Implementar usando Dijkstra o BFS
    pass

# Funciones de requerimientos restantes (placeholder)
def req_2(catalog):
    """Retorna el resultado del requerimiento 2"""
    pass

def req_3(catalog):
    """Retorna el resultado del requerimiento 3"""
    pass

def req_4(catalog):
    """Retorna el resultado del requerimiento 4"""
    pass

def req_5(catalog):
    """Retorna el resultado del requerimiento 5"""
    pass

def req_6(catalog):
    """Retorna el resultado del requerimiento 6"""
    pass

def req_7(catalog):
    """Retorna el resultado del requerimiento 7"""
    pass

def req_8(catalog):
    """Retorna el resultado del requerimiento 8"""
    pass

# Funciones para medir tiempos de ejecucion
def get_time():
    """devuelve el instante tiempo de procesamiento en milisegundos"""
    return float(time.perf_counter()*1000)

def delta_time(start, end):
    """devuelve la diferencia entre tiempos de procesamiento muestreados"""
    elapsed = float(end - start)
    return elapsed