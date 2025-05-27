import time
import csv
import os
from DataStructures.Graph import digraph as dg
from DataStructures.Map import map_linear_probing as mp  
from DataStructures.List import array_list as lt

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    catalog = {
        # Grafo principal no dirigido
        'graph': dg.new_graph(10000),
        
        # Mapas para almacenar información
        'deliveries': mp.new_map(5000, 0.7),
        'delivery_persons': mp.new_map(1000, 0.7),
        'restaurants': mp.new_map(2000, 0.7),
        'delivery_locations': mp.new_map(3000, 0.7),
        'node_deliverers': mp.new_map(5000, 0.7),
        'edge_times': mp.new_map(10000, 0.7),
        'deliverer_last_delivery': mp.new_map(1000, 0.7),
        
        # Estadísticas
        'stats': {
            'total_deliveries': 0,
            'total_delivery_persons': 0,
            'total_nodes': 0,
            'total_edges': 0,
            'total_restaurants': 0,
            'total_delivery_locations': 0,
            'total_delivery_time': 0.0,
            'avg_delivery_time': 0.0
        }
    }
    return catalog

def load_data(catalog, filename):
    # Si no se proporciona filename, permitir selección
    if filename is None:
        print("\nArchivos disponibles:")
        print("1. Data/deliverytime_20.csv")
        print("2. Data/deliverytime_40.csv") 
        print("3. Data/deliverytime_60.csv")
        print("4. Data/deliverytime_80.csv")
        print("5. Data/deliverytime_100.csv")
        
        choice = input("Selecciona archivo (1-5): ").strip()
        files = {
            '1': 'Data/deliverytime_20.csv',
            '2': 'Data/deliverytime_40.csv',
            '3': 'Data/deliverytime_60.csv', 
            '4': 'Data/deliverytime_80.csv',
            '5': 'Data/deliverytime_100.csv'
        }
        filename = files.get(choice, 'Data/deliverytime_20.csv')
    
    print(f"Cargando datos desde: {filename}")
    start_time = time.time()
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # Procesar cada registro
                delivery_id = row.get('ID', 'Unknown').strip()
                delivery_person_id = row.get('Delivery_person_ID', 'Unknown').strip()
                
                # Coordenadas formateadas a 4 decimales
                rest_lat = f"{float(row.get('Restaurant_latitude', '0')):.4f}"
                rest_lon = f"{float(row.get('Restaurant_longitude', '0')):.4f}"
                dest_lat = f"{float(row.get('Delivery_location_latitude', '0')):.4f}"
                dest_lon = f"{float(row.get('Delivery_location_longitude', '0')):.4f}"
                
                time_taken = float(row.get('Time_taken', '0'))
                
                # Crear identificadores de nodos
                origin_node = f"{rest_lat}_{rest_lon}"
                dest_node = f"{dest_lat}_{dest_lon}"
                
                # Agregar nodos si no existen
                if not dg.contains_vertex(catalog['graph'], origin_node):
                    dg.insert_vertex(catalog['graph'], origin_node, {
                        'latitude': rest_lat, 'longitude': rest_lon, 'type': 'restaurant'
                    })
                    mp.put(catalog['restaurants'], origin_node, True)
                    catalog['stats']['total_restaurants'] += 1
                
                if not dg.contains_vertex(catalog['graph'], dest_node):
                    dg.insert_vertex(catalog['graph'], dest_node, {
                        'latitude': dest_lat, 'longitude': dest_lon, 'type': 'delivery'
                    })
                    mp.put(catalog['delivery_locations'], dest_node, True)
                    catalog['stats']['total_delivery_locations'] += 1
                
                # Agregar/actualizar arco entre origen y destino
                edge_key = f"{min(origin_node, dest_node)}_{max(origin_node, dest_node)}"
                if mp.contains(catalog['edge_times'], edge_key):
                    # Actualizar promedio
                    edge_data = mp.get(catalog['edge_times'], edge_key)
                    edge_data['count'] += 1
                    edge_data['total_time'] += time_taken
                    edge_data['avg_time'] = edge_data['total_time'] / edge_data['count']
                    dg.add_edge(catalog['graph'], origin_node, dest_node, edge_data['avg_time'])
                else:
                    # Nuevo arco
                    mp.put(catalog['edge_times'], edge_key, {
                        'count': 1, 'total_time': time_taken, 'avg_time': time_taken
                    })
                    dg.add_edge(catalog['graph'], origin_node, dest_node, time_taken)
                
                # Arco secuencial por domiciliario
                if mp.contains(catalog['deliverer_last_delivery'], delivery_person_id):
                    last_dest = mp.get(catalog['deliverer_last_delivery'], delivery_person_id)
                    if last_dest != dest_node:
                        seq_edge_key = f"{min(last_dest, dest_node)}_{max(last_dest, dest_node)}"
                        if mp.contains(catalog['edge_times'], seq_edge_key):
                            edge_data = mp.get(catalog['edge_times'], seq_edge_key)
                            edge_data['count'] += 1
                            edge_data['total_time'] += time_taken
                            edge_data['avg_time'] = edge_data['total_time'] / edge_data['count']
                            dg.add_edge(catalog['graph'], last_dest, dest_node, edge_data['avg_time'])
                        else:
                            mp.put(catalog['edge_times'], seq_edge_key, {
                                'count': 1, 'total_time': time_taken, 'avg_time': time_taken
                            })
                            dg.add_edge(catalog['graph'], last_dest, dest_node, time_taken)
                
                mp.put(catalog['deliverer_last_delivery'], delivery_person_id, dest_node)
                
                # Agregar domiciliario si es nuevo
                if not mp.contains(catalog['delivery_persons'], delivery_person_id):
                    mp.put(catalog['delivery_persons'], delivery_person_id, {
                        'age': row.get('Delivery_person_Age', 'Unknown'),
                        'ratings': row.get('Delivery_person_Ratings', 'Unknown'),
                        'vehicle': row.get('Type_of_vehicle', 'Unknown')
                    })
                    catalog['stats']['total_delivery_persons'] += 1
                
                # Guardar domicilio
                mp.put(catalog['deliveries'], delivery_id, {
                    'delivery_person_id': delivery_person_id,
                    'origin': origin_node,
                    'destination': dest_node,
                    'time_taken': time_taken,
                    'order_type': row.get('Type_of_order', 'Unknown')
                })
                
                # Actualizar estadísticas
                catalog['stats']['total_deliveries'] += 1
                catalog['stats']['total_delivery_time'] += time_taken
        
        # Calcular estadísticas finales
        catalog['stats']['total_nodes'] = dg.order(catalog['graph'])
        catalog['stats']['total_edges'] = dg.size(catalog['graph'])
        
        if catalog['stats']['total_deliveries'] > 0:
            catalog['stats']['avg_delivery_time'] = (
                catalog['stats']['total_delivery_time'] / catalog['stats']['total_deliveries']
            )
        
        end_time = time.time()
        
        # Mostrar resumen
        print(f"\nCarga completada en {end_time - start_time:.2f} segundos")
        print("="*60)
        print("RESUMEN DE CARGA DE DATOS")
        print("="*60)
        print(f"Número total de domicilios procesados: {catalog['stats']['total_deliveries']:,}")
        print(f"Número total de domiciliarios identificados: {catalog['stats']['total_delivery_persons']:,}")
        print(f"Número total de nodos en el grafo: {catalog['stats']['total_nodes']:,}")
        print(f"Número de arcos en el grafo: {catalog['stats']['total_edges']:,}")
        print(f"Número de restaurantes identificados: {catalog['stats']['total_restaurants']:,}")
        print(f"Número de ubicaciones de entrega: {catalog['stats']['total_delivery_locations']:,}")
        print(f"Promedio de tiempo de entrega: {catalog['stats']['avg_delivery_time']:.2f} minutos")
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
